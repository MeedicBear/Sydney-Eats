import json
import uuid
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='sydney_innerwest_more')

new_places = [
    {
        "name": "Bloodwood",
        "location": "Newtown",
        "price": "$$$",
        "vibes": ["🍝 Good Food", "🍷 Date Night"],
        "description": "A Newtown staple serving brilliant sharing plates and natural wines in an eclectic space.",
    },
    {
        "name": "Continental Deli Bar Bistro",
        "location": "Newtown",
        "price": "$$$",
        "vibes": ["🍝 Good Food", "🍸 Drinks & Bar"],
        "description": "Famous for their canned cocktails ('Mar-tinny') and incredibly high-quality deli goods.",
    },
    {
        "name": "Cow and the Moon",
        "location": "Enmore",
        "price": "$",
        "vibes": ["💸 Cheap Eats", "🍝 Good Food"],
        "description": "World-award-winning gelato shop. Expect a line out the door on a warm night.",
    },
    {
        "name": "Bar Louise",
        "location": "Enmore",
        "price": "$$",
        "vibes": ["🍷 Date Night", "🍸 Drinks & Bar"],
        "description": "Vibrant Spanish tapas bar housed in a beautiful heritage-listed pink building.",
    },
    {
        "name": "Cairo Takeaway",
        "location": "Enmore",
        "price": "$",
        "vibes": ["💸 Cheap Eats", "🍝 Good Food"],
        "description": "Delicious, authentic Egyptian street food with a buzzing, casual atmosphere.",
    },
    {
        "name": "Colombo Social",
        "location": "Enmore",
        "price": "$$",
        "vibes": ["🍝 Good Food", "🍸 Drinks & Bar"],
        "description": "Incredible Sri Lankan food with a social mission, supporting asylum seekers.",
    },
    {
        "name": "The Grifter Brewing Co.",
        "location": "Marrickville",
        "price": "$$",
        "vibes": ["🍻 Pub", "🍸 Drinks & Bar"],
        "description": "One of the Inner West's most beloved craft breweries, famous for its Serpent's Kiss watermelon pilsner.",
    },
    {
        "name": "Wildflower Brewing & Blending",
        "location": "Marrickville",
        "price": "$$",
        "vibes": ["🍻 Pub", "🍸 Drinks & Bar"],
        "description": "Unique brewery focusing on wild-fermented and blended ales using native yeast.",
    },
    {
        "name": "One Penny Red",
        "location": "Summer Hill",
        "price": "$$$",
        "vibes": ["🍷 Date Night", "🍝 Good Food"],
        "description": "Elevated dining inside a beautifully restored former post office building.",
    },
    {
        "name": "The Temperance Society",
        "location": "Summer Hill",
        "price": "$$",
        "vibes": ["🍸 Drinks & Bar", "🤫 Hidden Gem"],
        "description": "A cozy, welcoming neighborhood small bar hidden away in Summer Hill.",
    },
    {
        "name": "Happyfield",
        "location": "Haberfield",
        "price": "$$",
        "vibes": ["🍝 Good Food", "💸 Cheap Eats"],
        "description": "Pancake heaven. A retro-diner style cafe serving arguably the best breakfast in the Inner West.",
    },
    {
        "name": "The Balmain Hotel",
        "location": "Balmain",
        "price": "$$",
        "vibes": ["🍻 Pub", "🍸 Drinks & Bar"],
        "description": "Eclectic pub with a massive tropical beer garden and great Asian-fusion pub grub.",
    },
    {
        "name": "Wayward Brewing Co.",
        "location": "Camperdown",
        "price": "$$",
        "vibes": ["🍻 Pub", "🍸 Drinks & Bar"],
        "description": "Awesome underground brewery tucked away in a former wine cellar.",
    },
    {
        "name": "Ester",
        "location": "Chippendale",
        "price": "$$$$",
        "vibes": ["🍝 Good Food", "🍷 Date Night"],
        "description": "A multi-award-winning dining destination famous for its wood-fired oven and blood sausage sanga.",
    },
    {
        "name": "LP's Quality Meats",
        "location": "Chippendale",
        "price": "$$$",
        "vibes": ["🍖 BBQ", "🍝 Good Food"],
        "description": "Meat lovers' paradise, serving house-cured and smoked meats in an industrial setting.",
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

print(f"Successfully added {added} more inner west places!")
