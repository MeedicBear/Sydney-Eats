import json
import uuid
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='sydney_west_1')

new_places = [
    {
        "name": "LILYMU",
        "location": "Parramatta",
        "price": "$$$",
        "vibes": ["🍣 Asian Eats", "🍷 Date Night"],
        "description": "Contemporary pan-Asian dining in Parramatta Square, offering creative dishes and excellent cocktails.",
    },
    {
        "name": "Harvey's Hot Sandwiches",
        "location": "Parramatta",
        "price": "$",
        "vibes": ["🍔 Burgers & Fast Food"],
        "description": "Massive, American-style deli subs and sandwiches packed with thick-cut meats.",
    },
    {
        "name": "Butter",
        "location": "Parramatta",
        "price": "$$",
        "vibes": ["🍔 Burgers & Fast Food", "👟 Sneaker Culture"],
        "description": "Cult-favorite spot famous for its fried chicken, champagne, and sneaker store aesthetic.",
    },
    {
        "name": "Nick & Nora's",
        "location": "Parramatta",
        "price": "$$$",
        "vibes": ["🍸 Drinks & Bar", "🌅 Great Views"],
        "description": "Glamorous rooftop bar inspired by the post-prohibition era, offering incredible cocktails and views of the city skyline.",
    },
    {
        "name": "Chatkazz",
        "location": "Harris Park",
        "price": "$",
        "vibes": ["🍣 Asian Eats", "💸 Cheap Eats"],
        "description": "An absolute institution for authentic Indian vegetarian street food. Constantly packed and always delicious.",
    },
    {
        "name": "Temasek",
        "location": "Parramatta",
        "price": "$$",
        "vibes": ["🍣 Asian Eats", "🤫 Hidden Gem"],
        "description": "Unassuming Singaporean and Malaysian restaurant tucked in an alley, famous for its laksa and Hainanese chicken rice.",
    },
    {
        "name": "Circa Espresso",
        "location": "Parramatta",
        "price": "$$",
        "vibes": ["☕ Cafe & Bakery", "🍽️ Great Dining"],
        "description": "One of Western Sydney's best cafes, serving Middle Eastern-inspired breakfasts and top-tier coffee.",
    },
    {
        "name": "Kanzo",
        "location": "Parramatta",
        "price": "$",
        "vibes": ["🍣 Asian Eats", "🍔 Burgers & Fast Food"],
        "description": "Beloved local hole-in-the-wall serving massive, cheap, and delicious sushi rolls.",
    },
    {
        "name": "Holy Basil",
        "location": "Parramatta",
        "price": "$$",
        "vibes": ["🍣 Asian Eats", "🎉 Lively & Fun"],
        "description": "Lively Thai and Lao restaurant known for its massive portions and signature fried ice cream.",
    },
    {
        "name": "Mamak",
        "location": "Parramatta",
        "price": "$$",
        "vibes": ["🍣 Asian Eats", "💸 Cheap Eats"],
        "description": "Award-winning Malaysian street food, famous for its flaky roti canai and rich curries.",
    },
    {
        "name": "Kouzina Greco",
        "location": "Parramatta",
        "price": "$$",
        "vibes": ["🌍 Global Eats", "🍽️ Great Dining"],
        "description": "Cozy, traditional Greek taverna serving hearty moussaka and souvlaki.",
    },
    {
        "name": "Bay Vista Dessert Bar",
        "location": "Parramatta",
        "price": "$$",
        "vibes": ["☕ Cafe & Bakery", "🎉 Lively & Fun"],
        "description": "Massive late-night dessert bar serving ice cream bowls, crepes, and wild loaded shakes.",
    },
    {
        "name": "Taj Indian Sweets & Restaurant",
        "location": "Harris Park",
        "price": "$",
        "vibes": ["🍣 Asian Eats", "💸 Cheap Eats"],
        "description": "A Harris Park icon offering incredible vegetarian curries, dosas, and a massive display of colorful Indian sweets.",
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
        'imageUrl': '',
        'rating': None,
        'reviewCount': None
    }
    places.append(formatted_place)
    added += 1

with open(processed_file, 'w', encoding='utf-8') as f:
    json.dump(places, f, indent=4, ensure_ascii=False)
    
with open('web/data.js', 'w', encoding='utf-8') as f:
    f.write('const processedPlacesData = ' + json.dumps(places, ensure_ascii=False) + ';')

print(f"Successfully added {added} new western places!")
