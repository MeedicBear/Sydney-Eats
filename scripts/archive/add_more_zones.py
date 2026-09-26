import json
import uuid
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='sydney_burwood_marrick_moore_1')

new_places = [
    # Burwood
    {
        "name": "Burwood Chinatown",
        "location": "Burwood",
        "price": "$",
        "vibes": ["🍣 Asian Eats", "💸 Cheap Eats"],
        "description": "A bustling, vibrant laneway precinct packed with incredibly authentic regional Chinese street food and bubble tea.",
    },
    {
        "name": "Xi'an Eatery",
        "location": "Burwood",
        "price": "$",
        "vibes": ["🍣 Asian Eats", "💸 Cheap Eats"],
        "description": "Famous for their massive, hand-pulled Biang Biang noodles and intensely flavorful cumin lamb burgers.",
    },
    {
        "name": "Sydney Dumpling King",
        "location": "Burwood",
        "price": "$",
        "vibes": ["🍣 Asian Eats", "💸 Cheap Eats"],
        "description": "An absolute institution for cheap, cheerful, and insanely delicious pan-fried pork dumplings.",
    },
    {
        "name": "The Rusty Rabbit",
        "location": "Burwood",
        "price": "$$",
        "vibes": ["☕ Cafe & Bakery", "👕 Casual & Chill"],
        "description": "A brilliant local cafe pouring great coffee alongside massive all-day breakfast plates.",
    },

    # Marrickville
    {
        "name": "Marrickville Pork Roll",
        "location": "Marrickville",
        "price": "$",
        "vibes": ["🍣 Asian Eats", "💸 Cheap Eats"],
        "description": "The undisputed king of banh mi in Sydney. Expect a fast-moving queue down the street.",
    },
    {
        "name": "Two Chaps",
        "location": "Marrickville",
        "price": "$$",
        "vibes": ["☕ Cafe & Bakery", "🍽️ Great Dining"],
        "description": "A sustainable, vegetarian cafe housed in an old welding workshop, famous for its handmade pasta nights.",
    },
    {
        "name": "Lazybones Lounge",
        "location": "Marrickville",
        "price": "$$",
        "vibes": ["🎵 Music & Entertainment", "🍸 Drinks & Bar"],
        "description": "Eclectic, velvet-draped live music venue featuring live bands every night of the week and fantastic pizzas.",
    },
    {
        "name": "Hello Auntie",
        "location": "Marrickville",
        "price": "$$$",
        "vibes": ["🍣 Asian Eats", "🍷 Date Night"],
        "description": "Modern Vietnamese dining with incredibly creative dishes and a sleek, low-lit atmosphere.",
    },
    {
        "name": "Kurmac",
        "location": "Marrickville",
        "price": "$$",
        "vibes": ["☕ Cafe & Bakery", "🍽️ Great Dining"],
        "description": "Tucked away in the industrial backstreets, offering a Japanese-inspired brunch menu.",
    },

    # Moore Park
    {
        "name": "Hordern Pavilion",
        "location": "Moore Park",
        "price": "$$$",
        "vibes": ["🎵 Music & Entertainment", "🎉 Lively & Fun"],
        "description": "One of Sydney's most iconic live music and concert venues, hosting major international and local acts.",
    },
    {
        "name": "Sydney Cricket Ground (SCG)",
        "location": "Moore Park",
        "price": "$$$",
        "vibes": ["🎡 Activity", "🎉 Lively & Fun"],
        "description": "Historic sports stadium hosting epic cricket matches in summer and AFL in winter.",
    },
    {
        "name": "The Entertainment Quarter",
        "location": "Moore Park",
        "price": "$$",
        "vibes": ["🎡 Activity", "👕 Casual & Chill"],
        "description": "A massive leisure precinct featuring cinemas, bowling, restaurants, and regular outdoor markets.",
    },
    {
        "name": "El Camino Cantina",
        "location": "Moore Park",
        "price": "$$",
        "vibes": ["🌮 Mexican & Latin", "🎉 Lively & Fun"],
        "description": "Wild, neon-lit Tex-Mex restaurant in the EQ famous for massive frozen margaritas and endless complimentary chips and salsa.",
    },
    {
        "name": "Fratelli Fresh",
        "location": "Moore Park",
        "price": "$$$",
        "vibes": ["🍕 Italian & Pizza", "🍽️ Great Dining"],
        "description": "A huge, family-friendly Italian dining hall perfect for a massive pizza or pasta before a game at the SCG.",
    },
    {
        "name": "Centennial Park",
        "location": "Moore Park",
        "price": "$",
        "vibes": ["☀️ Outdoor", "🎡 Activity"],
        "description": "Sydney's biggest and most beautiful park. Perfect for cycling, picnics, or long walks around the lakes.",
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

print(f"Successfully added {added} new spots!")
