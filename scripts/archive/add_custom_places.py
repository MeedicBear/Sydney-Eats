import json
import uuid
import time
from geopy.geocoders import Nominatim
import os

geolocator = Nominatim(user_agent="sydney_eats_custom")

new_places = [
    {
        "name": "Shady Pines Saloon",
        "location": "Darlinghurst",
        "price": "$$",
        "vibe": "hidden honky-tonk speakeasy",
        "url": "https://shadypinessaloon.com/"
    },
    {
        "name": "Uncle Ming's",
        "location": "Sydney CBD",
        "price": "$$",
        "vibe": "subterranean dumpling and cocktail bar",
        "url": "https://www.unclemings.com.au/"
    },
    {
        "name": "Papa Gede's",
        "location": "Sydney CBD",
        "price": "$$",
        "vibe": "voodoo-themed hidden cocktail bar",
        "url": "https://www.papagedes.com/"
    },
    {
        "name": "Double Deuce Lounge",
        "location": "Sydney CBD",
        "price": "$$",
        "vibe": "70s chic basement bar",
        "url": "https://doubledeucelounge.com/"
    },
    {
        "name": "Alberto's Lounge",
        "location": "Sydney CBD",
        "price": "$$$",
        "vibe": "intimate hidden italian date night",
        "url": "https://swillhouse.com/venues/albertos-lounge/"
    },
    {
        "name": "Firedoor",
        "location": "Surry Hills",
        "price": "$$$$",
        "vibe": "unique fine dining cooked over fire",
        "url": "https://firedoor.com.au/"
    },
    {
        "name": "Big Poppa's",
        "location": "Darlinghurst",
        "price": "$$$",
        "vibe": "late-night italian and hip hop romantic",
        "url": "https://www.bigpoppa.com.au/"
    },
    {
        "name": "Mimi's",
        "location": "Coogee",
        "price": "$$$$",
        "vibe": "luxurious beachside fine dining views",
        "url": "https://merivale.com/venues/mimis/"
    }
]

def assign_vibes(desc):
    desc_low = desc.lower()
    vibes = []
    if "bar" in desc_low or "cocktail" in desc_low or "saloon" in desc_low:
        vibes.append("🍸 Drinks & Bar")
    if "speakeasy" in desc_low or "underground" in desc_low or "hidden" in desc_low or "subterranean" in desc_low or "basement" in desc_low:
        vibes.append("🤫 Hidden Gem")
    if "italian" in desc_low:
        vibes.append("🍕 Italian & Pizza")
    if "dumpling" in desc_low:
        vibes.append("🍣 Asian Eats")
    if "date night" in desc_low or "romantic" in desc_low or "intimate" in desc_low:
        vibes.append("🍷 Date Night")
    if "fine dining" in desc_low or "luxurious" in desc_low or "chic" in desc_low:
        vibes.append("🍾 Fancy")
    if "views" in desc_low or "beachside" in desc_low:
        vibes.append("🌅 Great Views")
        
    if not vibes:
        vibes.append("👕 Casual & Chill")
    return list(set(vibes))

processed_file = os.path.join(os.path.dirname(__file__), "..", "web", "processed_places.json")
with open(processed_file, "r", encoding="utf-8") as f:
    existing_places = json.load(f)
    
existing_names = set(p['name'].lower() for p in existing_places)

added = 0
for p in new_places:
    if p['name'].lower() in existing_names:
        continue
        
    p_id = "place_" + str(uuid.uuid4())[:8]
    vibes = assign_vibes(p['vibe'])
    
    # Geocode
    search_query = f"{p['name']} {p['location']} Sydney, Australia"
    coords = None
    try:
        location = geolocator.geocode(search_query, timeout=10)
        time.sleep(1)
        if location:
            coords = {"lat": location.latitude, "lng": location.longitude}
        else:
            location2 = geolocator.geocode(f"{p['name']} Sydney, Australia", timeout=10)
            time.sleep(1)
            if location2:
                coords = {"lat": location2.latitude, "lng": location2.longitude}
    except Exception as e:
        pass
        
    formatted_place = {
        "id": p_id,
        "name": p['name'],
        "location": p['location'],
        "price": p['price'],
        "vibes": vibes,
        "description": p['vibe'].capitalize() + ".",
        "url": p['url'],
        "coordinates": coords,
        "imageUrl": ""
    }
    existing_places.append(formatted_place)
    added += 1

with open(processed_file, "w", encoding="utf-8") as f:
    json.dump(existing_places, f, indent=4, ensure_ascii=False)
    
with open(os.path.join(os.path.dirname(__file__), "..", "web", "data.js"), "w", encoding="utf-8") as f:
    f.write('const processedPlacesData = ' + json.dumps(existing_places, ensure_ascii=False) + ';')
    
print(f"Added {added} custom places!")
