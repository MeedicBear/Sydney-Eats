# Sydney Eats & Itinerary Generator 🍸

A beautifully designed, client-side web application for discovering Sydney's best restaurants, bars, and activities. Features an interactive map, dynamic filtering by "vibes" and price, and an intelligent **Itinerary & Bar Crawl Generator** that algorithmically routes walkable dates and epic multi-stop crawls based on Haversine distance.

## 🚀 Features

- **Interactive UI & Map:** A responsive Tailwind CSS grid and Leaflet.js map integration that dynamically updates as you filter.
- **Vibe Filtering:** Filter 250+ highly curated locations across Sydney by custom tags like `🍷 Date Night`, `🍸 Drinks & Bar`, `🪩 Nightclub`, `💸 Cheap Eats`, and more.
- **Intelligent Itinerary Generator:** Generate 2-stop dates (Activity + Dinner), 3-stop nights (Activity + Dinner + Bar), or epic 3/4-stop Bar Crawls. The algorithm calculates the physical distance between venues to ensure your entire night is within a walkable radius!
- **Yelp Integration:** Real-time ratings and review counts pulled via the Yelp Fusion API ensure you're only seeing the best.
- **Save & Share:** Save your favorite spots to local storage and generate a shareable URL to send your curated list to friends.
- **Dark Mode:** Fully supported system and toggleable dark mode.

## 📁 File Structure

The project is structured to be completely serverless and highly performant on the client side:

```
fervent-newton/
│
├── web/                             # The Frontend Application
│   ├── index.html                   # Main application interface
│   ├── app.js                       # Core application logic, routing, and UI rendering
│   ├── data.js                      # Compiled JavaScript data object (loads instantly)
│   └── processed_places.json        # The raw JSON data lake of 250+ Sydney venues
│
├── scripts/                         # Python Backend Utilities
│   ├── fetch_yelp_photos.py         # Master script: Fetches missing photos & ratings from Yelp API
│   ├── process_data.py              # Initial data ingestion script
│   └── archive/                     # Archived scripts used for historical data injection, deduplication, and UI regex updates
│
└── README.md
```

## 🛠️ How it Works (No Backend Required!)

To maximize stability and minimize costs, the live application has **no backend server**. 

All heavy lifting—such as geocoding addresses to lat/long coordinates and hitting rate-limited APIs (like Yelp for photos and ratings)—is handled locally via the Python scripts in the `scripts/` directory.

1. **Add Data:** New venues are added to `web/processed_places.json`.
2. **Enrich Data:** Running `python scripts/fetch_yelp_photos.py` searches the Yelp API for any new venues, grabs their best cover photo and current star rating, and saves it to the JSON.
3. **Compile:** The script automatically compiles the JSON into `web/data.js`.
4. **Deploy:** The frontend (`web/`) can be hosted statically on GitHub Pages, Vercel, or Netlify and will load instantly for users without any API lag.

## 🏃‍♂️ Running Locally

Since it's a static site, you can run it simply by opening `web/index.html` in your browser. 

For the best experience (to avoid CORS issues with local modules or fonts), run a simple local server:

```bash
cd web
python -m http.server 8000
```
Then visit `http://localhost:8000` in your browser.

## 🔧 Managing Data

If you want to add new locations and fetch their Yelp data:
1. You will need a Yelp Fusion API key. Set it as an environment variable or place it in the `fetch_yelp_photos.py` script.
2. Run `python scripts/fetch_yelp_photos.py` to process any new entries in `processed_places.json`. 

---
*Built for the ultimate Sydney experience.* 🍻
