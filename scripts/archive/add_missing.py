import json
import uuid
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='sydney_missing_1')

activities = [
    {
        "name": "Sakura House",
        "location": "Sydney CBD",
        "price": "$$",
        "vibes": ["🤫 Hidden Gem", "🍷 Date Night"],
        "description": "Late-night basement Izakaya",
        "url": "",
        "website": "https://www.sakurahousesydney.com/"
    },
    {
        "name": "The Gidley",
        "location": "161 King St, Sydney CBD",
        "price": "$$$$",
        "vibes": ["🤫 Hidden Gem", "🍷 Date Night"],
        "description": "Plush speakeasy steakhouse",
        "url": "",
        "website": "https://www.thegidley.com.au/"
    }
]

processed_file = 'web/processed_places.json'
with open(processed_file, 'r', encoding='utf-8') as f:
    places = json.load(f)

for act in activities:
    p_id = 'place_' + str(uuid.uuid4())[:8]
    
    search_query = f"{act['name']} {act['location']} Australia"
    coords = None
    try:
        loc = geolocator.geocode(search_query, timeout=10)
        time.sleep(1)
        if loc:
            coords = {'lat': loc.latitude, 'lng': loc.longitude}
        else:
            loc2 = geolocator.geocode(f"{act['name']} Sydney Australia", timeout=10)
            time.sleep(1)
            if loc2:
                coords = {'lat': loc2.latitude, 'lng': loc2.longitude}
    except:
        pass
        
    formatted_place = {
        'id': p_id,
        'name': act['name'],
        'location': act['location'],
        'price': act['price'],
        'vibes': act['vibes'],
        'description': act['description'],
        'url': act['url'],
        'website': act['website'],
        'coordinates': coords,
        'imageUrl': ''
    }
    places.append(formatted_place)

with open(processed_file, 'w', encoding='utf-8') as f:
    json.dump(places, f, indent=4, ensure_ascii=False)
    
with open('web/data.js', 'w', encoding='utf-8') as f:
    f.write('const processedPlacesData = ' + json.dumps(places, ensure_ascii=False) + ';')

print(f"Successfully added missing places!")
