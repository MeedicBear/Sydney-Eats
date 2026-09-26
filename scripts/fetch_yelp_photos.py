import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()
YELP_API_KEY = os.getenv("YELP_API_KEY")

if not YELP_API_KEY:
    print("Error: YELP_API_KEY not found in .env")
    exit(1)

def fetch_yelp_photos():
    processed_file = os.path.join(os.path.dirname(__file__), "..", "web", "processed_places.json")
    data_js_file = os.path.join(os.path.dirname(__file__), "..", "web", "data.js")

    with open(processed_file, "r", encoding="utf-8") as f:
        places = json.load(f)

    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}",
        "accept": "application/json"
    }

    url = "https://api.yelp.com/v3/businesses/search"

    success_count = 0
    
    print(f"Fetching photos and ratings for {len(places)} places from Yelp...")

    for i, place in enumerate(places):
        # Even if we have an image, we might not have a rating. Let's fetch if rating is missing!
        if place.get('imageUrl') and place['imageUrl'].strip() != '' and 'rating' in place and place['rating'] is not None:
            print(f"[{i+1}/{len(places)}] Skipping {place['name']} (Already has photo and rating)")
            success_count += 1
            continue
            
        time.sleep(0.2)
        
        term = place['name']
        location = place['location']
        if "sydney" not in location.lower():
            location += ", Sydney"
            
        params = {
            "term": term,
            "location": location,
            "limit": 1
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                results = response.json().get("businesses", [])
                if results and len(results) > 0:
                    biz = results[0]
                    
                    if not place.get('imageUrl'):
                        image_url = biz.get("image_url")
                        place['imageUrl'] = image_url or ''
                        
                    place['rating'] = biz.get("rating")
                    place['reviewCount'] = biz.get("review_count")
                    
                    success_count += 1
                    print(f"[{i+1}/{len(places)}] Found data for: {term} (Rating: {place['rating']})")
                    continue
            
            print(f"[{i+1}/{len(places)}] No data found for: {term} (Status: {response.status_code})")
            if not place.get('imageUrl'):
                place['imageUrl'] = ''
            place['rating'] = None
            place['reviewCount'] = None
            
        except Exception as e:
            print(f"Error on {term}: {e}")
            if not place.get('imageUrl'):
                place['imageUrl'] = ''
            place['rating'] = None
            place['reviewCount'] = None

    # Save back to JSON
    with open(processed_file, "w", encoding="utf-8") as f:
        json.dump(places, f, indent=4, ensure_ascii=False)
        
    # Save back to JS variable
    with open(data_js_file, "w", encoding="utf-8") as f:
        f.write('const processedPlacesData = ' + json.dumps(places, ensure_ascii=False) + ';')

    print(f"Finished! Successfully found Yelp data for {success_count}/{len(places)} places.")

if __name__ == "__main__":
    fetch_yelp_photos()
