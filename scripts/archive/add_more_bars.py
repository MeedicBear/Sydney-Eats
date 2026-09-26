import json
import uuid
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='sydney_bars_2')

new_bars = [
    {
        "name": "Earl's Juke Joint",
        "location": "Newtown",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🎵 Live Music"],
        "description": "New Orleans-inspired cocktail bar hidden behind an old butcher shop facade.",
    },
    {
        "name": "Jacoby's Tiki Bar",
        "location": "Enmore",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🌺 Tiki"],
        "description": "Twin Peaks themed tiki bar with flaming cocktails.",
    },
    {
        "name": "The Courtyard",
        "location": "Newtown",
        "price": "$",
        "vibes": ["🍸 Drinks & Bar", "🍻 Pub"],
        "description": "Classic Newtown pub with a massive beer garden.",
    },
    {
        "name": "The Rover",
        "location": "Surry Hills",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🦪 Seafood"],
        "description": "Chic neighborhood bar serving great wine and fresh oysters.",
    },
    {
        "name": "Goros",
        "location": "Surry Hills",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🎤 Karaoke"],
        "description": "Late-night Japanese bar with free karaoke rooms and arcade games.",
    },
    {
        "name": "Icebergs Club Bar",
        "location": "Bondi Beach",
        "price": "$$$",
        "vibes": ["🍸 Drinks & Bar", "🌅 Great Views"],
        "description": "Iconic bar overlooking the Bondi baths and the ocean.",
    },
    {
        "name": "Hotel Ravesis",
        "location": "Bondi Beach",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🏖️ Beach"],
        "description": "Pastel-pink boutique hotel and bar with wrap-around terraces.",
    },
    {
        "name": "4 Pines BrewPub",
        "location": "Manly",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🍻 Brewery"],
        "description": "Famous craft brewery right near the Manly ferry wharf.",
    },
    {
        "name": "The Corso Bar",
        "location": "Manly",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🏖️ Beach"],
        "description": "Vibrant local spot in the heart of Manly.",
    },
    {
        "name": "The Henson",
        "location": "Marrickville",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🍻 Pub"],
        "description": "Community-focused pub with great craft beer and an old-school vibe.",
    },
    {
        "name": "Vic On The Park",
        "location": "Marrickville",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🐕 Dog Friendly", "🎵 Live Music"],
        "description": "Sprawling inner-west pub with a basketball court and live bands.",
    },
    {
        "name": "Mary's",
        "location": "Newtown",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🍔 Burgers", "🤘 Rock"],
        "description": "Dark, loud, heavy metal bar famous for its incredible burgers.",
    },
    {
        "name": "The Glenmore",
        "location": "The Rocks",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🌅 Great Views"],
        "description": "Historic pub with one of the best rooftop views of the Sydney Opera House.",
    },
    {
        "name": "Lord Nelson Brewery",
        "location": "The Rocks",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🍻 Brewery"],
        "description": "Sydney's oldest continually licensed hotel, brewing their own ales.",
    },
    {
        "name": "Green Moustache",
        "location": "North Sydney",
        "price": "$$$",
        "vibes": ["🍸 Drinks & Bar", "🌿 Botanical"],
        "description": "Lush rooftop oasis filled with plants in the heart of North Sydney.",
    }
]

processed_file = 'web/processed_places.json'
with open(processed_file, 'r', encoding='utf-8') as f:
    places = json.load(f)
    
existing_names = [p['name'].lower() for p in places]

added = 0
for act in new_bars:
    if act['name'].lower() in existing_names:
        continue
        
    p_id = 'place_' + str(uuid.uuid4())[:8]
    
    search_query = f"{act['name']} {act['location']} Sydney Australia"
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
        'url': '',
        'website': '',
        'coordinates': coords,
        'imageUrl': ''
    }
    places.append(formatted_place)
    added += 1

with open(processed_file, 'w', encoding='utf-8') as f:
    json.dump(places, f, indent=4, ensure_ascii=False)
    
with open('web/data.js', 'w', encoding='utf-8') as f:
    f.write('const processedPlacesData = ' + json.dumps(places, ensure_ascii=False) + ';')

print(f"Successfully added {added} new bars!")
