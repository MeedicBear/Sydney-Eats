import json
import uuid
import time
from geopy.geocoders import Nominatim
import os

geolocator = Nominatim(user_agent="sydney_eats_app")

with open('data/new_html_places.json', 'r') as f:
    new_places = json.load(f)

processed_file = os.path.join(os.path.dirname(__file__), "..", "web", "processed_places.json")
with open(processed_file, "r", encoding="utf-8") as f:
    existing_places = json.load(f)

def assign_vibes(desc):
    desc_low = desc.lower()
    vibes = []
    if "bar" in desc_low or "cocktail" in desc_low or "lounge" in desc_low or "wine" in desc_low:
        vibes.append("🍸 Drinks & Bar")
    if "speakeasy" in desc_low or "underground" in desc_low or "hidden" in desc_low or "basement" in desc_low or "subterranean" in desc_low:
        vibes.append("🤫 Hidden Gem")
    if "izakaya" in desc_low or "asian" in desc_low or "cantonese" in desc_low:
        vibes.append("🍣 Asian Eats")
    if "italian" in desc_low or "sicilian" in desc_low:
        vibes.append("🍕 Italian & Pizza")
    if "french" in desc_low:
        vibes.append("🌍 Global Eats")
    if "steakhouse" in desc_low:
        vibes.append("🥩 Steakhouse")
    if "intimate" in desc_low or "moody" in desc_low:
        vibes.append("🍷 Date Night")
    if "opulent" in desc_low or "chic" in desc_low or "plush" in desc_low:
        vibes.append("🍾 Fancy")
    if "retro" in desc_low or "1920s" in desc_low or "1890s" in desc_low:
        vibes.append("👕 Casual & Chill")
    if "jazz" in desc_low or "vinyl" in desc_low:
        vibes.append("🎵 Music & Entertainment")
        
    if not vibes:
        vibes.append("👕 Casual & Chill")
    
    return list(set(vibes))

added = 0
for p in new_places:
    # 1. Generate ID
    p_id = "place_" + str(uuid.uuid4())[:8]
    
    # 2. Description
    desc = p['vibe']
    
    # 3. Vibes
    vibes = assign_vibes(desc)
    
    # 4. Geocode
    search_query = f"{p['name']} {p['location']} Sydney, Australia"
    try:
        location = geolocator.geocode(search_query, timeout=10)
        time.sleep(1) # Nominatim policy
        if location:
            coords = {"lat": location.latitude, "lng": location.longitude}
        else:
            # Fallback geocode just by name + Sydney
            location2 = geolocator.geocode(f"{p['name']} Sydney, Australia", timeout=10)
            time.sleep(1)
            if location2:
                coords = {"lat": location2.latitude, "lng": location2.longitude}
            else:
                coords = None
    except Exception as e:
        print(f"Geocode error for {p['name']}: {e}")
        coords = None
        
    if not coords:
        print(f"Could not find coordinates for {p['name']}. Skipping for now.")
        continue
        
    formatted_place = {
        "id": p_id,
        "name": p['name'],
        "location": p['location'],
        "price": p['price'].split(" ")[0] if " " in p['price'] else p['price'], # Get first price if range
        "vibes": vibes,
        "description": desc,
        "url": p['url'],
        "coordinates": coords,
        "imageUrl": "" # will fetch next
    }
    existing_places.append(formatted_place)
    added += 1
    print(f"Added {p['name']}")

with open(processed_file, "w", encoding="utf-8") as f:
    json.dump(existing_places, f, indent=4, ensure_ascii=False)
    
with open(os.path.join(os.path.dirname(__file__), "..", "web", "data.js"), "w", encoding="utf-8") as f:
    f.write('const processedPlacesData = ' + json.dumps(existing_places, ensure_ascii=False) + ';')
    
print(f"Successfully processed and added {added} places!")
