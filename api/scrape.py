from http.server import BaseHTTPRequestHandler
import json
import random
from datetime import datetime

POSTAL_LOOKUP = {
    "1000": "Brussels", "2000": "Antwerpen", "3000": "Leuven",
    "4000": "Liège", "5000": "Namur", "6000": "Charleroi",
    "7000": "Mons", "8000": "Brugge", "9000": "Gent",
    "2100": "Deurne", "2600": "Berchem", "2800": "Mechelen",
    "4020": "Liège", "4800": "Verviers", "9100": "Sint-Niklaas",
}

def resolve_location(loc: str) -> str:
    loc = loc.strip()
    if loc.isdigit() and loc in POSTAL_LOOKUP:
        return f"{loc} {POSTAL_LOOKUP[loc]}"
    return loc

def generate_realistic_leads(location: str, categories: list, sources: list, limit: int) -> list:
    name_pools = {
        "restaurant": ["La Belle Vue", "Chez Marie", "Bistro Central", "Le Petit Gourmet", "Taverne Royale", "Pasta & Vino", "Grill House", "Asian Fusion", "Frituur", "Brasserie"],
        "café": ["Café de la Place", "The Coffee Corner", "Brasserie du Centre", "Espresso Bar", "Café Central", "The Daily Grind", "Terrace Café", "Koffiehuis"],
        "shop": ["Mode Boutique", "Local Market", "Gift Shop", "Stationery Corner", "Fashion Outlet", "Home & Garden", "Bookshop", "Droguerie"],
        "bakery": ["Boulangerie Artisanale", "The Bread House", "Pâtisserie Fine", "Daily Bread", "Bakkerij"],
        "hairdresser": ["Salon Élégance", "Hair Studio", "Coiffure Moderne", "Barber Shop", "Kapsalon"],
    }
    streets = ["Rue de la Loi", "Avenue Louise", "Grand Place", "Meir", "Veldstraat", "Place Saint-Lambert", "Koningstraat", "Markt", "Rue Haute", "Kerkstraat"]

    leads = []
    for _ in range(min(limit, 40)):
        cat = random.choice(categories) if categories else "restaurant"
        pool = name_pools.get(cat.lower(), name_pools["shop"])
        name = random.choice(pool)
        if random.random() > 0.5:
            name += f" {random.randint(1, 25)}"

        has_real_website = random.random() < 0.18
        is_social = random.random() < 0.35 and not has_real_website
        website = ""
        if has_real_website:
            website = f"https://www.{name.lower().replace(' ', '').replace('&', '')}.be"
        elif is_social:
            website = f"https://facebook.com/{name.lower().replace(' ', '')}"

        phone = f"+32 {random.randint(1,9)}{random.randint(100,999)} {random.randint(10,99)} {random.randint(10,99)}" if random.random() > 0.25 else ""

        leads.append({
            "name": name,
            "category": cat.capitalize(),
            "address": f"{random.choice(streets)} {random.randint(1, 180)}, {location}",
            "phone": phone,
            "website": website,
            "source": random.choice(sources) if sources else "LocalBusinessScraper",
            "rating": round(3.4 + random.random() * 1.5, 1),
            "reviews": random.randint(2, 280),
            "has_website": bool(website and not is_social),
            "is_social_only": is_social,
        })

    no_web = [l for l in leads if not l["has_website"]]
    return (no_web or leads)[:limit]

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body.decode('utf-8')) if body else {}
        except:
            data = {}

        location = resolve_location(data.get('location', ''))
        if not location:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "location required"}).encode())
            return

        categories = data.get('categories', ["restaurant", "café", "shop"])
        scrapers = data.get('scrapers', ["GeoLeadScraper"])
        limit = int(data.get('limit', 20))

        leads = generate_realistic_leads(location, categories, scrapers, limit)

        response = {
            "success": True,
            "location": location,
            "count": len(leads),
            "scrapers_used": scrapers,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "leads": leads,
            "note": "Demo data with strong no-website bias. Real Google Maps scrapers cannot run on Vercel (browser automation + ToS). Plug a backend with Local Business Scraper or a legal API for production."
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
