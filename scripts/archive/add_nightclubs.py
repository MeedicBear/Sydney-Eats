import json
import uuid
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='sydney_clubs_1')

new_places = [
    {
        "name": "ivy",
        "location": "Sydney CBD",
        "price": "$$$",
        "vibes": ["🪩 Nightclub", "🎉 Lively & Fun"],
        "description": "Sydney's mega-club complex featuring multiple dance floors, rooftop pool parties, and massive weekend events.",
    },
    {
        "name": "Home The Venue",
        "location": "Darling Harbour",
        "price": "$$$",
        "vibes": ["🪩 Nightclub", "🎉 Lively & Fun"],
        "description": "Massive multi-level superclub right on the water at Darling Harbour, known for massive house and techno nights.",
    },
    {
        "name": "Chinese Laundry",
        "location": "Sydney CBD",
        "price": "$$",
        "vibes": ["🪩 Nightclub", "🎵 Music & Entertainment"],
        "description": "Underground institution for bass, electro, and techno, featuring one of the best sound systems in the city.",
    },
    {
        "name": "The Argyle",
        "location": "The Rocks",
        "price": "$$$",
        "vibes": ["🪩 Nightclub", "🍸 Drinks & Bar"],
        "description": "Sprawling historic venue with a massive cobbled courtyard that turns into a massive party on weekends.",
    },
    {
        "name": "Oxford Art Factory",
        "location": "Darlinghurst",
        "price": "$$",
        "vibes": ["🪩 Nightclub", "🎵 Music & Entertainment"],
        "description": "Legendary live music venue and late-night club space inspired by Andy Warhol's Factory.",
    },
    {
        "name": "Club 77",
        "location": "Darlinghurst",
        "price": "$$",
        "vibes": ["🪩 Nightclub", "🤫 Hidden Gem"],
        "description": "Intimate, sweaty underground bunker that is the beating heart of Sydney's late-night techno and house scene.",
    },
    {
        "name": "The Cliff Dive",
        "location": "Darlinghurst",
        "price": "$$",
        "vibes": ["🪩 Nightclub", "🎉 Lively & Fun"],
        "description": "Subterranean tiki-themed dance club playing mostly hip-hop and R&B.",
    },
    {
        "name": "ARQ Sydney",
        "location": "Darlinghurst",
        "price": "$$",
        "vibes": ["🪩 Nightclub", "🎉 Lively & Fun"],
        "description": "Iconic, high-energy LGBTQI+ nightclub with incredible drag shows and massive dance floors.",
    },
    {
        "name": "The Beresford",
        "location": "Surry Hills",
        "price": "$$$",
        "vibes": ["🍻 Pubs & Breweries", "🎉 Lively & Fun"],
        "description": "Famous for its massive sunny courtyard and wildly popular Sunday sessions that stretch into the night.",
    },
    {
        "name": "Cargo Bar",
        "location": "Darling Harbour",
        "price": "$$",
        "vibes": ["🪩 Nightclub", "🎉 Lively & Fun"],
        "description": "Classic Darling Harbour party spot with waterfront views and packed weekend dance floors.",
    },
    {
        "name": "Bungalow 8",
        "location": "Darling Harbour",
        "price": "$$$",
        "vibes": ["🪩 Nightclub", "🌅 Great Views"],
        "description": "Tropical-themed waterfront club next to Cargo, perfect for sunset drinks that turn into all-night dancing.",
    },
    {
        "name": "Flamingo Lounge",
        "location": "Potts Point",
        "price": "$$$",
        "vibes": ["🪩 Nightclub", "🍾 Fancy"],
        "description": "Chic, Miami-inspired nightclub and lounge in the heart of Kings Cross.",
    },
    {
        "name": "Kings Cross Hotel",
        "location": "Potts Point",
        "price": "$$",
        "vibes": ["🪩 Nightclub", "🍻 Pubs & Breweries"],
        "description": "Multi-level party destination with a different vibe on every floor, crowned with a rooftop bar.",
    },
    {
        "name": "Greenwood Hotel",
        "location": "North Sydney",
        "price": "$$",
        "vibes": ["🪩 Nightclub", "☀️ Outdoor"],
        "description": "Huge historic schoolhouse converted into a massive pub, known for massive outdoor day parties and festivals.",
    },
    {
        "name": "Universal Sydney",
        "location": "Darlinghurst",
        "price": "$$",
        "vibes": ["🪩 Nightclub", "🎉 Lively & Fun"],
        "description": "Massive two-level LGBTQI+ superclub featuring incredible lighting, sound, and spectacular drag performances.",
    },
    {
        "name": "Burdekin Hotel",
        "location": "Darlinghurst",
        "price": "$$",
        "vibes": ["🪩 Nightclub", "🍻 Pubs & Breweries"],
        "description": "Five levels of parties on Oxford Street, from underground techno to rooftop drinks.",
    },
    {
        "name": "The Carter",
        "location": "Sydney CBD",
        "price": "$$$",
        "vibes": ["🪩 Nightclub", "🎉 Lively & Fun"],
        "description": "Beyoncé and Jay-Z inspired subterranean lounge and club with heavily hip-hop focused nights.",
    },
    {
        "name": "Mary's Underground",
        "location": "Sydney CBD",
        "price": "$$$",
        "vibes": ["🎵 Music & Entertainment", "🍷 Date Night"],
        "description": "Late-night live music venue (formerly The Basement) serving up jazz, incredible food, and cocktails until the early hours.",
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

print(f"Successfully added {added} new nightclubs!")
