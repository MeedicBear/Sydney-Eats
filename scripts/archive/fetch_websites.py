import json
import time
from googlesearch import search

processed_file = 'web/processed_places.json'
with open(processed_file, 'r', encoding='utf-8') as f:
    places = json.load(f)

updated = 0
for i, place in enumerate(places):
    # Only try if website is empty
    if not place.get('website'):
        name = place['name']
        location = place['location']
        
        query = f"{name} {location} Sydney official website"
        print(f"[{i+1}/{len(places)}] Searching for {name}...")
        try:
            # We want to skip yelp, tripadvisor, facebook, instagram, tiktok
            found = False
            for url in search(query, num_results=5, lang="en"):
                if not any(blocked in url.lower() for blocked in ['yelp.', 'tripadvisor.', 'facebook.', 'instagram.', 'tiktok.', 'broadsheet.', 'timeout.', 'concreteplayground.']):
                    place['website'] = url
                    updated += 1
                    found = True
                    print(f"    -> Found: {url}")
                    break
            
            if not found:
                print("    -> No official website found.")
        except Exception as e:
            print(f"    -> Error: {e}")
        time.sleep(2) # be nice to google
    else:
        print(f"[{i+1}/{len(places)}] Skipping {place['name']}, already has website")

with open(processed_file, 'w', encoding='utf-8') as f:
    json.dump(places, f, indent=4, ensure_ascii=False)
    
with open('web/data.js', 'w', encoding='utf-8') as f:
    f.write('const processedPlacesData = ' + json.dumps(places, ensure_ascii=False) + ';')

print(f"Added {updated} actual websites!")
