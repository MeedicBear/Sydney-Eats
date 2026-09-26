import json
import uuid
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='sydney_activities_1')

activities = [
    {
        "name": "Taronga Zoo",
        "location": "Mosman, Sydney",
        "price": "$$$",
        "vibes": ["🎡 Activity", "⛴️ Ferry Access", "☀️ Outdoor"],
        "description": "Incredible zoo with harbor views. Very accessible via a short scenic ferry ride from Circular Quay.",
    },
    {
        "name": "Luna Park",
        "location": "Milsons Point, Sydney",
        "price": "$$",
        "vibes": ["🎡 Activity", "🚆 Train Access", "⛴️ Ferry Access"],
        "description": "Historic amusement park on the harbor. Easy to reach via train to Milsons Point or ferry.",
    },
    {
        "name": "Bondi to Coogee Coastal Walk",
        "location": "Bondi Beach, Sydney",
        "price": "$",
        "vibes": ["🎡 Activity", "☀️ Outdoor", "🚌 Bus Access"],
        "description": "Stunning cliffside walk passing beaches and rock pools. Best reached by bus to Bondi.",
    },
    {
        "name": "Wendy Whiteley's Secret Garden",
        "location": "Lavender Bay, Sydney",
        "price": "$",
        "vibes": ["🎡 Activity", "🤫 Hidden Gem", "🚆 Train Access"],
        "description": "A magical, lush public garden with harbor views. Short walk from North Sydney station.",
    },
    {
        "name": "Holey Moley Golf Club",
        "location": "Newtown, Sydney",
        "price": "$$",
        "vibes": ["🎡 Activity", "🚆 Train Access", "🍸 Drinks & Bar"],
        "description": "Crazy indoor mini golf with cocktails and pop-culture themes. Right near Newtown station.",
    },
    {
        "name": "Sydney Observatory",
        "location": "Millers Point, Sydney",
        "price": "$$",
        "vibes": ["🎡 Activity", "🍷 Date Night", "🚆 Train Access"],
        "description": "Stargazing and astronomy tours at night. Walkable from Circular Quay or Wynyard.",
    },
    {
        "name": "Three Sisters Blue Mountains",
        "location": "Katoomba, NSW",
        "price": "$",
        "vibes": ["🎡 Activity", "☀️ Outdoor", "🚆 Train Access", "🚗 Far/Drive Recommended"],
        "description": "Iconic rock formation. About 2 hours away. Accessible by Blue Mountains train line or car.",
    },
    {
        "name": "Sydney Harbour Kayaks",
        "location": "The Spit Bridge, Mosman",
        "price": "$$$",
        "vibes": ["🎡 Activity", "☀️ Outdoor", "🚌 Bus Access"],
        "description": "Kayaking around Middle Harbour. Reached by bus from the CBD or North Sydney.",
    },
    {
        "name": "Archie Brothers Cirque Electriq",
        "location": "Alexandria, Sydney",
        "price": "$$$",
        "vibes": ["🎡 Activity", "🚆 Train Access"],
        "description": "Circus-themed arcade, bowling, and dodgems. 15 min walk from Green Square or Mascot stations.",
    },
    {
        "name": "BridgeClimb Sydney",
        "location": "The Rocks, Sydney",
        "price": "$$$$",
        "vibes": ["🎡 Activity", "☀️ Outdoor", "🚆 Train Access"],
        "description": "Climb the iconic Harbour Bridge. Easily walkable from Circular Quay.",
    },
    {
        "name": "Art Gallery of NSW",
        "location": "The Domain, Sydney",
        "price": "$",
        "vibes": ["🎡 Activity", "🚆 Train Access"],
        "description": "Classic and contemporary art collections, including the new Sydney Modern building. Walk from St James or Martin Place.",
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

print(f"Successfully added {len(activities)} activities!")
