# 📍 Day 2: Autonomous Google Maps B2B Lead Extractor (Python + Playwright)

> Built by **Vinaykumar Mathad** ([@Vinaykumar2016](https://github.com/Vinaykumar2016) / [@poweredbyvinay](https://instagram.com/poweredbyvinay))  
> Part of the **30 Days / 30 AI Prototypes Challenge**

---

## 🎯 What it Does
Tools like **Apify**, **PhantomBuster**, or **Outscraper** charge upwards of **₹4,200/month** to scrape local Google Maps business directories.

This is a **100% free, local, open-source Python automation tool** that runs directly on your machine:
1. **Autonomous Browser Automation:** Launches Playwright Chromium, navigates to Google Maps, and queries any local niche and city (e.g., *"Gyms in Indiranagar Bangalore"*, *"Interior Designers in Mysore"*, *"Dental Clinics in Hubli"*).
2. **Infinite Feed Traversal:** Smoothly scrolls through the Google Maps results feed and extracts real business data.
3. **Verified Data Points Extracted:**
   - Business Name
   - Category / Sector
   - Rating (e.g. 4.8★)
   - Total Review Count
   - Phone Number (Verified Indian mobile / landline contact)
   - Address / Locality
   - Direct Google Maps Link
4. **Instant Spreadsheet Export:** Exports directly to clean `leads_<query>.csv` and auto-opens in Excel on completion.

---

## 🚀 Quick Start (1-Click on Windows)

1. Clone or download this repository.
2. Double-click **`run_scraper.bat`**.  
   *(It automatically verifies Python, installs Playwright if missing, and starts the scraper!)*
3. Enter your target niche and city, hit Enter, and watch Chrome extract live leads in seconds!

---

## 💻 Manual Setup (macOS / Linux / Windows CLI)

```bash
# 1. Clone repository
git clone https://github.com/Vinaykumar2016/30-days-ai-prototypes.git
cd 30-days-ai-prototypes/Day02_Maps_Lead_Scraper

# 2. Install dependencies (using python -m guarantees correct path)
python -m pip install playwright requests
python -m playwright install chromium

# 3. Run the extractor (or just double click run_scraper.bat!)
python scraper.py
```

---

## 🛠️ Tech Stack
- **Python 3.9+**
- **Playwright (Chromium)** — Headless / Visible browser automation
- **Standard Library:** `csv`, `re`, `urllib.parse` (Zero bloated external packages)

---

## 📬 Connect with Vinay
- **Instagram:** [@poweredbyvinay](https://instagram.com/poweredbyvinay)
- **YouTube:** [@poweredbyvinay](https://youtube.com/@poweredbyvinay)
- **GitHub:** [@Vinaykumar2016](https://github.com/Vinaykumar2016)
