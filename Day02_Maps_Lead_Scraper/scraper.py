"""
================================================================================
AUTONOMOUS B2B LEAD EXTRACTOR & EMAIL/PHONE ENRICHMENT ENGINE
Day 02 / 30-Day Engineering Challenge
Engineered by Vinaykumar Mathad (@Vinaykumar2016 / @poweredbyvinay)
================================================================================
Data Fields Extracted:
1. Business Name & Category
2. Google Rating & Review Count
3. Verified Phone Number (Direct from profile)
4. Full Street Address
5. Official Website URL
6. Direct Business Contact Email (Scraped autonomously from website)
7. Google Maps Profile Link
================================================================================
"""

import os
import sys
import time
import re
import csv
import json
import urllib.parse
import requests
from playwright.sync_api import sync_playwright

def clean_str(s):
    if not s:
        return ""
    # Strip non-printable unicode icons and normalize spaces
    cleaned = re.sub(r'[\uE000-\uF8FF]', '', s)
    return re.sub(r'\s+', ' ', cleaned).strip()

def scrape_email_from_website(website_url):
    """Visits the business website homepage and extracts contact email."""
    if not website_url or website_url == "N/A" or "google.com" in website_url:
        return "N/A"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        r = requests.get(website_url, headers=headers, timeout=6)
        if r.status_code == 200:
            found_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r.text)
            valid_emails = [
                e.lower() for e in set(found_emails) 
                if not any(e.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif', '.css', '.js'])
                and not any(domain in e.lower() for domain in ['sentry', 'wixpress', 'schema.org'])
            ]
            if valid_emails:
                for priority in ['contact', 'info', 'support', 'hello', 'admin']:
                    for e in valid_emails:
                        if priority in e:
                            return e
                return valid_emails[0]
    except Exception:
        pass
    return "Not Listed on Website"

def run_deep_lead_scraper(query, max_leads=15, headless=False):
    print("\n" + "=" * 80)
    print(f"[*] AUTONOMOUS B2B LEAD EXTRACTOR & ENRICHMENT ENGINE")
    print(f"[*] Target Query  : {query}")
    print(f"[*] Target Volume : {max_leads} leads")
    print(f"[*] Browser Mode  : {'Headless' if headless else 'Visible Chrome'}")
    print("=" * 80 + "\n")

    encoded_query = urllib.parse.quote(query)
    target_url = f"https://www.google.com/maps/search/{encoded_query}"

    extracted_leads = []
    seen_names = set()

    with sync_playwright() as p:
        print("[*] Launching Chromium Engine...")
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print(f"[*] Opening Google Maps: {target_url}")
        page.goto(target_url, timeout=60000)
        page.wait_for_timeout(3000)

        # Handle cookie consent if visible
        try:
            consent_btn = page.locator('button[aria-label*="Accept"], button:has-text("Accept all"), button:has-text("I agree")').first
            if consent_btn.is_visible(timeout=3000):
                consent_btn.click()
                page.wait_for_timeout(2000)
        except Exception:
            pass

        feed_selector = 'div[role="feed"]'
        try:
            page.wait_for_selector(feed_selector, timeout=12000)
            print("[+] Feed detected. Commencing autonomous scroll and deep profile extraction...\n")
        except Exception:
            print("[!] Scanning discovered elements directly...\n")

        scroll_attempts = 0
        while len(extracted_leads) < max_leads and scroll_attempts < 8:
            cards = page.locator('a[href*="/maps/place/"]').all()
            
            for card in cards:
                if len(extracted_leads) >= max_leads:
                    break

                try:
                    raw_label = card.get_attribute("aria-label") or card.inner_text().split('\n')[0]
                    name = clean_str(raw_label.split('·')[0].split('\n')[0])

                    if not name or name in seen_names or len(name) < 2:
                        continue

                    seen_names.add(name)
                    maps_url = card.get_attribute("href") or ""

                    parent = card.locator('xpath=..')
                    card_text = parent.inner_text() if parent else ""

                    rating = "N/A"
                    rating_match = re.search(r'([1-5]\.[0-9])', card_text)
                    if rating_match:
                        rating = rating_match.group(1)

                    reviews_count = "0"
                    reviews_match = re.search(r'\(([0-9,]+)\)', card_text)
                    if reviews_match:
                        reviews_count = reviews_match.group(1).replace(',', '')

                    lines = [clean_str(l) for l in card_text.split('\n') if clean_str(l)]
                    category = lines[1] if len(lines) > 1 and not re.search(r'^[1-5]\.', lines[1]) else "Local Business"

                    # CLICK INTO LISTING FOR REAL PHONE, ADDRESS & WEBSITE
                    card.click()
                    page.wait_for_timeout(2000)

                    # Extract Phone from detail panel
                    phone_el = page.locator('button[data-item-id*="phone:tel:"]').first
                    if phone_el.count() > 0:
                        phone = clean_str(phone_el.inner_text())
                    else:
                        pm = re.search(r'(\+?91[\-\s]?)?[6789]\d{9}|\b0\d{2,4}[-\s]?\d{6,8}\b', card_text)
                        phone = pm.group(0).strip() if pm else "N/A"

                    # Extract Address from detail panel
                    addr_el = page.locator('button[data-item-id="address"]').first
                    if addr_el.count() > 0:
                        address = clean_str(addr_el.inner_text())
                    else:
                        address = lines[2] if len(lines) > 2 else query

                    # Extract Website from detail panel
                    web_el = page.locator('a[data-item-id="authority"]').first
                    if web_el.count() > 0:
                        website = web_el.get_attribute("href") or "N/A"
                    else:
                        website = "N/A"

                    # SCRAPE EMAIL FROM WEBSITE
                    email = "N/A"
                    if website != "N/A":
                        email = scrape_email_from_website(website)

                    lead = {
                        "id": len(extracted_leads) + 1,
                        "business_name": name,
                        "category": category,
                        "rating": rating,
                        "reviews_count": reviews_count,
                        "phone_number": phone,
                        "email": email,
                        "website": website,
                        "address": address,
                        "maps_url": maps_url
                    }

                    extracted_leads.append(lead)
                    print(f"  [+] [{len(extracted_leads):02d}/{max_leads:02d}] {name[:26]:<26} | {rating}★ | Phone: {phone:<15} | Email: {email}")

                except Exception:
                    continue

            if len(extracted_leads) >= max_leads:
                break

            scroll_attempts += 1
            page.evaluate('''() => {
                const feed = document.querySelector('div[role="feed"]');
                if (feed) {
                    feed.scrollTop += 1400;
                } else {
                    window.scrollBy(0, 1000);
                }
            }''')
            page.wait_for_timeout(2000)

        browser.close()

    # Save to CSV and JSON
    output_dir = os.path.dirname(os.path.abspath(__file__))
    clean_filename = re.sub(r'[^a-zA-Z0-9]', '_', query).strip('_')
    csv_file = os.path.join(output_dir, f"leads_{clean_filename}.csv")
    latest_csv = os.path.join(output_dir, "latest_leads.csv")

    if extracted_leads:
        fieldnames = ["id", "business_name", "category", "rating", "reviews_count", "phone_number", "email", "website", "address", "maps_url"]
        
        for path in [csv_file, latest_csv]:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(extracted_leads)

        print("\n" + "=" * 80)
        print(f"[✓] SUCCESS: Extracted {len(extracted_leads)} verified B2B leads!")
        print(f"[✓] Fields: Name, Rating, Reviews, Verified Phone, Contact Email, Website, Full Address")
        print(f"[✓] Exported File: {csv_file}")
        print("=" * 80 + "\n")
    else:
        print("\n[!] Zero leads extracted. Try checking your search term or internet connection.")

    return extracted_leads

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query_input = sys.argv[1]
    else:
        query_input = input("Enter target niche & city (e.g. Dental Clinics in Indiranagar Bangalore): ").strip()
        if not query_input:
            query_input = "Dental Clinics in Indiranagar Bangalore"

    if len(sys.argv) > 2:
        try:
            count = int(sys.argv[2])
        except ValueError:
            count = 10
    else:
        count_input = input("Enter number of leads to extract (default 10): ").strip()
        count = int(count_input) if count_input.isdigit() else 10

    run_deep_lead_scraper(query_input, max_leads=count, headless=False)
