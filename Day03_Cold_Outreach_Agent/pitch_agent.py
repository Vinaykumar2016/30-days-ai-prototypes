"""
================================================================================
AUTONOMOUS B2B COLD OUTREACH & CLIENT ACQUISITION AGENT
Day 03 / 30-Day Engineering Challenge
Engineered by Vinaykumar Mathad (@Vinaykumar2016 / @poweredbyvinay)
================================================================================
Takes raw lead spreadsheets (e.g. from Day 02 Google Maps Scraper), performs
digital gap analysis (missing website, rating bottlenecks, scale potential),
and synthesizes bespoke high-conversion cold emails & 1-click WhatsApp pitches.
================================================================================
"""

import os
import sys
import csv
import re
import urllib.parse

def clean_phone_for_whatsapp(phone_str):
    """Formats Indian and international phone numbers for direct wa.me links."""
    if not phone_str or phone_str == "N/A":
        return None
    # Strip all non-digit characters
    digits = re.sub(r'\D', '', phone_str)
    # Handle Indian 10-digit mobile numbers (starting with 6,7,8,9)
    if len(digits) == 10 and digits[0] in '6789':
        return f"91{digits}"
    # Handle numbers with leading 0
    if len(digits) == 11 and digits.startswith('0'):
        return f"91{digits[1:]}"
    # Already has country code 91
    if len(digits) == 12 and digits.startswith('91'):
        return digits
    return digits if len(digits) >= 10 else None

def generate_bespoke_pitch(lead):
    """
    Analyzes digital footprint and generates hyper-targeted outreach angles.
    Zero robotic spam. Short, high-status, consultative problem-solving.
    """
    name = lead.get('business_name') or lead.get('name') or "Business Owner"
    category = lead.get('category') or "Local Business"
    rating_str = lead.get('rating') or "0"
    reviews_str = lead.get('reviews_count') or lead.get('reviews') or "0"
    address = lead.get('address') or "Bengaluru"
    website = lead.get('website') or "N/A"
    phone = lead.get('phone_number') or lead.get('phone') or "N/A"
    email = lead.get('email') or "N/A"

    # Extract locality snippet (e.g. Indiranagar, Koramangala)
    locality = "your area"
    for part in address.split(','):
        p = part.strip()
        if any(known in p.lower() for known in ['indiranagar', 'koramangala', 'hsr', 'whitefield', 'jayanagar', 'mysore', 'hubli', 'bangalore', 'bengaluru']):
            locality = p
            break

    try:
        rating = float(rating_str)
    except ValueError:
        rating = 4.5

    has_no_website = not website or website == "N/A" or "no website" in website.lower() or "not listed" in website.lower()

    # --- STRATEGY 1: Missing Website Angle (High-Value Web Dev Pitch) ---
    if has_no_website:
        subject = f"Quick observation on {name} mobile customer flow in {locality}"
        email_body = f"""Hi Team {name},

I was looking up top-rated {category.lower()} options around {locality} and noticed your Google profile has strong community traction ({rating}★ across {reviews_str} reviews).

However, I noticed you don't have a direct mobile website or digital menu linked. When local customers search on Google Maps, many end up bouncing to nearby competitors who offer instant online menus and booking.

We build ultra-fast, modern mobile web landing pages for local {category.lower()} businesses that convert profile visitors into paying customers.

Would you be open to a quick 3-minute visual mockup of how a modern site would look for {name} this week?

Best regards,
Vinaykumar Mathad
Software Engineer & Agency Founder | PlainLogics
hello@poweredbyvinay.com"""

        whatsapp_body = f"Hi Team *{name}*, noticed your listing in {locality} with great reviews ({rating}★). I saw you don't have a direct mobile website linked on Google Maps yet. We help local businesses set up fast mobile menus & booking pages to capture walk-ins. Can I share a quick 2-minute visual mockup with your team today?"

    # --- STRATEGY 2: Reputation Recovery Angle (Review Filter & Automation) ---
    elif rating < 4.2:
        subject = f"Reputation automation idea for {name} ({locality})"
        email_body = f"""Hi Team {name},

I came across {name} while researching local {category.lower()} providers in {locality}. 

Your business has solid review volume ({reviews_str} reviews), but the overall score currently sits at {rating}★. A small sub-4.2 rating on Google Maps often diverts 40%+ of potential high-ticket clients to neighboring competitors.

We implement lightweight WhatsApp review automation engines that automatically route satisfied customers to leave 5-star Google reviews while directing private feedback directly to your management before it hits public pages.

Could I send over a quick 2-minute Loom/breakdown showing how this works for local businesses?

Best regards,
Vinaykumar Mathad
PlainLogics | hello@poweredbyvinay.com"""

        whatsapp_body = f"Hi Team *{name}*, noticed your {category.lower()} presence in {locality}. We specialize in automated Google review funnel systems that help local businesses systematically recover their rating to 4.8★+ and boost customer trust. Open to a brief 2-minute walkthrough?"

    # --- STRATEGY 3: High-Performing Scale Angle (24/7 WhatsApp AI Booking) ---
    else:
        subject = f"Automated customer booking pipeline for {name}"
        email_body = f"""Hi Team {name},

Congratulations on building such a strong reputation in {locality} ({rating}★ across {reviews_str} verified clients).

Given your current customer volume, our team specializes in setting up 24/7 automated WhatsApp inquiry & appointment confirmation bots that handle incoming customer queries instantly, without requiring manual staff time.

We recently helped a business in your space cut booking drop-off by 35% with zero extra marketing spend.

Are you open to reviewing a short 3-minute architecture overview on Tuesday?

Best regards,
Vinaykumar Mathad
PlainLogics | hello@poweredbyvinay.com"""

        whatsapp_body = f"Hi Team *{name}*, congratulations on the strong {rating}★ reputation in {locality}! We build 24/7 automated WhatsApp appointment and inquiry systems for busy {category.lower()} teams to capture bookings on autopilot. Open to a quick 2-minute overview?"

    # WhatsApp Link
    clean_phone = clean_phone_for_whatsapp(phone)
    if clean_phone:
        wa_link = f"https://wa.me/{clean_phone}?text={urllib.parse.quote(whatsapp_body)}"
    else:
        wa_link = "No Valid Phone Listed"

    # Mailto Link
    if email and email != "N/A" and "@" in email:
        mailto_link = f"mailto:{email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(email_body)}"
    else:
        mailto_link = "No Email Found"

    return {
        "business_name": name,
        "category": category,
        "rating": rating_str,
        "reviews": reviews_str,
        "phone": phone,
        "email": email,
        "website": website,
        "outreach_strategy": "Missing Website / Web Dev" if has_no_website else ("Reputation Recovery" if rating < 4.2 else "WhatsApp AI Automation"),
        "subject_line": subject,
        "email_pitch": email_body,
        "whatsapp_pitch": whatsapp_body,
        "whatsapp_link": wa_link,
        "mailto_link": mailto_link
    }

def run_outreach_agent(csv_input_path=None):
    print("\n" + "=" * 80)
    print(" [*] AUTONOMOUS B2B COLD OUTREACH & CLIENT ACQUISITION AGENT")
    print(" [*] Engineered by Vinaykumar Mathad (@Vinaykumar2016 / @poweredbyvinay)")
    print("=" * 80 + "\n")

    # Locate default input if not specified
    if not csv_input_path:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        day2_dir = os.path.abspath(os.path.join(base_dir, "..", "Day02_Maps_Lead_Scraper"))
        candidates = [
            os.path.join(day2_dir, "latest_leads.csv"),
            os.path.join(day2_dir, "leads.csv"),
            os.path.join(base_dir, "sample_leads.csv")
        ]
        for c in candidates:
            if os.path.exists(c):
                csv_input_path = c
                break

    if not csv_input_path or not os.path.exists(csv_input_path):
        print("[!] No leads CSV detected. Creating sample leads dataset for demonstration...")
        csv_input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_leads.csv")
        sample_data = [
            {"business_name": "Third Wave Coffee Roasters", "category": "Cafe", "rating": "4.6", "reviews_count": "1420", "phone_number": "+91 98451 22334", "email": "contact@thirdwavecoffee.in", "website": "https://thirdwavecoffee.in", "address": "Koramangala, Bengaluru"},
            {"business_name": "Corner House Ice Cream", "category": "Dessert Shop", "rating": "4.8", "reviews_count": "3890", "phone_number": "+91 97310 88991", "email": "info@cornerhouse.in", "website": "N/A", "address": "Indiranagar, Bengaluru"},
            {"business_name": "The Roastery Artisan Cafe", "category": "Artisan Coffee", "rating": "3.9", "reviews_count": "180", "phone_number": "+91 99002 44556", "email": "N/A", "website": "N/A", "address": "Koramangala 4th Block, Bengaluru"}
        ]
        with open(csv_input_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["business_name", "category", "rating", "reviews_count", "phone_number", "email", "website", "address"])
            writer.writeheader()
            writer.writerows(sample_data)

    print(f"[*] Reading source lead database: {csv_input_path}")
    raw_leads = []
    with open(csv_input_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_leads.append(row)

    print(f"[+] Loaded {len(raw_leads)} candidate businesses. Executing digital footprint analysis...\n")

    campaign = []
    for idx, lead in enumerate(raw_leads):
        pitch = generate_bespoke_pitch(lead)
        campaign.append(pitch)
        
        name = pitch['business_name']
        strategy = pitch['outreach_strategy']
        phone = pitch['phone']
        email = pitch['email']
        
        print(f"  [+] [{idx+1:02d}/{len(raw_leads):02d}] {name[:28]:<28} | Strategy: {strategy:<26}")
        print(f"       -> WhatsApp: {phone} (1-Click Ready)")
        print(f"       -> Email   : {email}\n")

    # Save to Campaign CSV
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_csv = os.path.join(output_dir, "outreach_campaign_ready.csv")

    fieldnames = [
        "business_name", "category", "rating", "reviews", "phone", "email", 
        "website", "outreach_strategy", "subject_line", "email_pitch", 
        "whatsapp_pitch", "whatsapp_link", "mailto_link"
    ]

    with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(campaign)

    print("=" * 80)
    print(f"[✓] CAMPAIGN GENERATION COMPLETE: Processed {len(campaign)} businesses!")
    print(f"[✓] Master Outreach Sheet: {output_csv}")
    print("=" * 80 + "\n")

    return campaign

if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else None
    run_outreach_agent(csv_file)
