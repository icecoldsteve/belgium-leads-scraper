# Belgium Leads Scraper PWA

A Progressive Web App dashboard that unifies the workflow of multiple Google Maps scrapers for finding small businesses (restaurants, cafés, shops) without websites across Belgium.

## Updated GUI (v2)
The dashboard is now a companion interface for the **Local Business Scraper** you run locally:

- Nice tabbed UI (Configure / Results)
- Drag-and-drop CSV upload from the scraper
- Filters for “No website” / “Social only”
- Clean export to CSV / Excel / JSON
- Demo generator for testing the UI

### Workflow
1. Run Local Business Scraper on your machine (keyword + “must not have a website” + Belgian postcodes)
2. Export the CSV
3. Open this PWA and drop the CSV in
4. Filter and re-export a clean list

The actual scraping cannot run inside the browser for security and ToS reasons — it stays on your computer. This PWA is the polished front-end for reviewing and exporting the results.

## Notes
- Real production scraping of Google Maps requires running the original tools locally + compliance with Google’s Terms of Service.
- Belgian postal codes based on open data (bpost / ODWB).

## Original tools referenced
- https://github.com/athm793/local-business-scraper
