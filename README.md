# Belgium Leads Scraper PWA

A Progressive Web App dashboard that unifies the workflow of multiple Google Maps scrapers for finding small businesses (restaurants, cafés, shops) without websites across Belgium.

## Features
- Pick any Belgian postal code or city (official-style list included)
- Select one or more of the 6 scrapers:
  - GeoLeadScraper
  - Ghost Map
  - Scrupp Extractor
  - GMapsScout
  - Local Business Scraper
  - Maps Lead Gen
- One-click SCRAPE with live progress
- Export results to CSV, Excel (.xlsx), or JSON
- Works offline after first load (PWA)

## Deployed on Vercel
The frontend + serverless API is ready for Vercel. Real Google Maps scrapers (Chrome extensions / Playwright) cannot run on serverless platforms due to browser requirements and Terms of Service.

## How to run locally
```bash
pip install fastapi uvicorn
uvicorn backend:app --reload --port 8000
```

## Notes
- Generates realistic demo leads optimized for “no website / social-only” businesses.
- Real production scraping requires local tools or legal APIs (Google Places, SerpAPI, Outscraper) + compliance with platform terms.
- Belgian postal codes based on open data (bpost / ODWB).

## Original tools referenced
- https://github.com/ozhehkovski/geoleadscraper
- https://github.com/uppifyagency/ghostmap
- https://github.com/athm793/local-business-scraper
