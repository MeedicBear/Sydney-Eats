import json
import uuid
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='sydney_innerwest_3')

new_places = [
    {
        "name": "Bar Italia",
        "location": "Leichhardt",
        "price": "$",
        "vibes": ["🍝 Good Food", "💸 Cheap Eats"],
        "description": "Iconic old-school Italian joint famous for its authentic gelato and espresso.",
    },
    {
        "name": "Capriccio Osteria",
        "location": "Leichhardt",
        "price": "$$",
        "vibes": ["🍝 Good Food", "🍷 Date Night"],
        "description": "Modern Italian dining with a beautiful sunny courtyard.",
    },
    {
        "name": "Taste of Shanghai",
        "location": "Burwood",
        "price": "$$",
        "vibes": ["🍝 Good Food", "🥢 Asian Eats"],
        "description": "Bustling institution serving up incredible xiao long bao and pan-fried dumplings.",
    },
    {
        "name": "Mr Stonebowl",
        "location": "Burwood",
        "price": "$$",
        "vibes": ["🍝 Good Food", "🥢 Asian Eats"],
        "description": "Hugely popular spot known for its creative presentation and stonebowl dishes.",
    },
    {
        "name": "Red Pepper",
        "location": "Strathfield",
        "price": "$$",
        "vibes": ["🍗 Korean Fried Chicken", "🍻 Pub"],
        "description": "Hidden inside the Strathfield Sports Club, serving arguably Sydney's best Korean fried chicken.",
    },
    {
        "name": "Hansang",
        "location": "Strathfield",
        "price": "$$",
        "vibes": ["🍖 Korean BBQ", "🍝 Good Food"],
        "description": "Authentic and hearty Korean banquets and stews with endless side dishes.",
    },
    {
        "name": "Tan Viet Noodle House",
        "location": "Cabramatta",
        "price": "$",
        "vibes": ["💸 Cheap Eats", "🥢 Asian Eats"],
        "description": "Legendary Vietnamese institution famous for its shattering crispy skin chicken.",
    },
    {
        "name": "Phu Quoc",
        "location": "Cabramatta",
        "price": "$",
        "vibes": ["💸 Cheap Eats", "🥢 Asian Eats"],
        "description": "No-frills Vietnamese dining offering massive portions of incredible pho and sugar cane prawn.",
    },
    {
        "name": "Frango Charcoal Chicken",
        "location": "Petersham",
        "price": "$",
        "vibes": ["💸 Cheap Eats", "🍔 Burgers"],
        "description": "The undisputed king of Portuguese charcoal chicken and chilli sauce in Sydney.",
    },
    {
        "name": "Baba's Place",
        "location": "Marrickville",
        "price": "$$",
        "vibes": ["🤫 Hidden Gem", "🍝 Good Food"],
        "description": "Set in a warehouse, serving food inspired by suburban immigrant nostalgia (think Lebanese meets modern Australian).",
    },
    {
        "name": "Shanghai Night",
        "location": "Ashfield",
        "price": "$",
        "vibes": ["💸 Cheap Eats", "🥢 Asian Eats"],
        "description": "A staple of Ashfield's 'Little Shanghai' strip, churning out incredible handmade dumplings.",
    },
    {
        "name": "Abhi's Indian",
        "location": "North Strathfield",
        "price": "$$",
        "vibes": ["🍝 Good Food", "🍷 Date Night"],
        "description": "Long-standing, highly awarded Indian restaurant blending traditional flavors with modern techniques.",
    },
    {
        "name": "Where's Nick",
        "location": "Marrickville",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🍷 Date Night"],
        "description": "Cozy, unpretentious neighborhood wine bar focusing on natural and minimal intervention wines.",
    },
    {
        "name": "The Royal",
        "location": "Leichhardt",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🍻 Pub"],
        "description": "Historic pub with a beautiful botanical balcony overlooking Norton Street.",
    }
]

processed_file = 'web/processed_places.json'
with open(processed_file, 'r', encoding='utf-8') as f:
    places = json.load(f)
    
existing_names = [p['name'].lower() for p in places]

added = 0
for act in new_places:
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

print(f"Successfully added {added} new inner west places!")
