import json
import uuid
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='sydney_activities_2')

activities = [
    {
        "name": "Bondi Beach",
        "location": "Bondi, Sydney",
        "price": "$",
        "vibes": ["🏖️ Beach", "☀️ Outdoor", "🚌 Bus Access"],
        "description": "Sydney's most famous and popular beach. Great for surfing and people-watching.",
    },
    {
        "name": "Manly Beach",
        "location": "Manly, Sydney",
        "price": "$",
        "vibes": ["🏖️ Beach", "☀️ Outdoor", "⛴️ Ferry Access"],
        "description": "A beautiful pine-tree-lined beach. Take the iconic Manly Ferry from Circular Quay to get there.",
    },
    {
        "name": "Bronte Beach",
        "location": "Bronte, Sydney",
        "price": "$",
        "vibes": ["🏖️ Beach", "☀️ Outdoor", "🚌 Bus Access"],
        "description": "A beautiful, family-friendly beach with a fantastic ocean pool and park.",
    },
    {
        "name": "Palm Beach",
        "location": "Palm Beach, Sydney",
        "price": "$",
        "vibes": ["🏖️ Beach", "☀️ Outdoor", "🚗 Far/Drive Recommended"],
        "description": "Sydney's northernmost stretch of sand. Famous as the setting for 'Home and Away'. Quite far from the CBD.",
    },
    {
        "name": "Balmoral Beach",
        "location": "Mosman, Sydney",
        "price": "$",
        "vibes": ["🏖️ Beach", "☀️ Outdoor", "🚌 Bus Access"],
        "description": "A calm, beautiful harbor beach on the North Shore. Perfect for a relaxing swim or paddleboarding.",
    },
    {
        "name": "Camp Cove",
        "location": "Watsons Bay, Sydney",
        "price": "$",
        "vibes": ["🏖️ Beach", "☀️ Outdoor", "⛴️ Ferry Access"],
        "description": "A small, sheltered, and incredibly scenic harbor beach near Watsons Bay.",
    },
    {
        "name": "Royal Botanic Garden Sydney",
        "location": "Sydney CBD",
        "price": "$",
        "vibes": ["🎡 Activity", "☀️ Outdoor", "🚆 Train Access"],
        "description": "Stunning harbor-side botanical gardens right next to the Opera House.",
    },
    {
        "name": "Sea Life Sydney Aquarium",
        "location": "Darling Harbour, Sydney",
        "price": "$$$",
        "vibes": ["🎡 Activity", "🚆 Train Access"],
        "description": "Massive indoor aquarium featuring dugongs, sharks, and penguins.",
    },
    {
        "name": "Queen Victoria Building (QVB)",
        "location": "Sydney CBD",
        "price": "$",
        "vibes": ["🎡 Activity", "🚆 Train Access"],
        "description": "A breathtaking 19th-century building now housing boutique shops and cafes.",
    },
    {
        "name": "Royal National Park",
        "location": "Sutherland Shire, NSW",
        "price": "$",
        "vibes": ["🎡 Activity", "☀️ Outdoor", "🚗 Far/Drive Recommended"],
        "description": "The world's second oldest national park! Incredible coastal walks and the famous Figure Eight Pools. Best by car.",
    },
    {
        "name": "Cockatoo Island",
        "location": "Sydney Harbour",
        "price": "$",
        "vibes": ["🎡 Activity", "☀️ Outdoor", "⛴️ Ferry Access"],
        "description": "A UNESCO World Heritage-listed island in the middle of the harbor with a rich convict and maritime history.",
    },
    {
        "name": "Sydney Tower Eye",
        "location": "Sydney CBD",
        "price": "$$$",
        "vibes": ["🎡 Activity", "🌅 Great Views", "🚆 Train Access"],
        "description": "The highest point in Sydney offering 360-degree views of the city.",
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
        'url': '',
        'coordinates': coords,
        'imageUrl': ''
    }
    places.append(formatted_place)

with open(processed_file, 'w', encoding='utf-8') as f:
    json.dump(places, f, indent=4, ensure_ascii=False)
    
with open('web/data.js', 'w', encoding='utf-8') as f:
    f.write('const processedPlacesData = ' + json.dumps(places, ensure_ascii=False) + ';')

print(f"Successfully added {len(activities)} beaches & activities!")
