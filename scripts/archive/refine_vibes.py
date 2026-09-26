import json
import os

processed_file = os.path.join(os.path.dirname(__file__), "..", "web", "processed_places.json")
data_js_file = os.path.join(os.path.dirname(__file__), "..", "web", "data.js")

with open(processed_file, "r", encoding="utf-8") as f:
    places = json.load(f)

# Define our refined taxonomy mapping
# We use lower case for matching
VIBE_MAP = {
    # Ambiance & Setting
    "romantic": "🍷 Date Night",
    "date night": "🍷 Date Night",
    "intimate": "🍷 Date Night",
    "moody": "🍷 Date Night",
    
    "casual": "👕 Casual & Chill",
    "relaxed": "👕 Casual & Chill",
    "homely": "👕 Casual & Chill",
    "friendly": "👕 Casual & Chill",
    "cosy": "👕 Casual & Chill",
    "cozy": "👕 Casual & Chill",
    "nostalgic": "👕 Casual & Chill",
    "retro": "👕 Casual & Chill",
    "1980s vibe": "👕 Casual & Chill",
    "homestyle": "👕 Casual & Chill",
    
    "fine dining": "🍾 Fancy",
    "elegant": "🍾 Fancy",
    "luxurious": "🍾 Fancy",
    "sophisticated": "🍾 Fancy",
    "luxe": "🍾 Fancy",
    "chic": "🍾 Fancy",
    "grand": "🍾 Fancy",
    "extravagant": "🍾 Fancy",
    "classic": "🍾 Fancy",
    "minimalist": "🍾 Fancy",

    "lively": "🎉 Lively & Fun",
    "bustling": "🎉 Lively & Fun",
    "vibrant": "🎉 Lively & Fun",
    "fun": "🎉 Lively & Fun",
    "interactive": "🎉 Lively & Fun",
    "quirky": "🎉 Lively & Fun",
    "artsy": "🎉 Lively & Fun",
    "people watching": "🎉 Lively & Fun",
    "beach club vibe": "🎉 Lively & Fun",

    "live music": "🎵 Music & Entertainment",
    "jazz bar": "🎵 Music & Entertainment",
    "dj": "🎵 Music & Entertainment",
    "vinyl": "🎵 Music & Entertainment",
    "music": "🎵 Music & Entertainment",
    "arcade": "🎵 Music & Entertainment",

    "views": "🌅 Great Views",
    "harbourside": "🌅 Great Views",
    "rooftop": "🌅 Great Views",
    "rooftop bar": "🌅 Great Views",
    "beachside": "🌅 Great Views",
    "poolside": "🌅 Great Views",
    "nature": "🌅 Great Views",
    "glamping": "🌅 Great Views",

    "hidden gem": "🤫 Hidden Gem",
    "hidden": "🤫 Hidden Gem",
    "speakeasy": "🤫 Hidden Gem",
    "underground": "🤫 Hidden Gem",
    "underground bar": "🤫 Hidden Gem",
    "basement bar": "🤫 Hidden Gem",
    
    # Food & Drink Categories
    "wine bar": "🍸 Drinks & Bar",
    "cocktails": "🍸 Drinks & Bar",
    "pub": "🍸 Drinks & Bar",
    "sports bar": "🍸 Drinks & Bar",
    "historic pub": "🍸 Drinks & Bar",
    "negroni bar": "🍸 Drinks & Bar",
    "mezcal bar": "🍸 Drinks & Bar",
    "distillery": "🍸 Drinks & Bar",
    "brewery": "🍸 Drinks & Bar",
    "happy hour": "🍸 Drinks & Bar",
    "late night": "🍸 Drinks & Bar",
    "wine": "🍸 Drinks & Bar",
    "limoncello": "🍸 Drinks & Bar",
    "margaritas": "🍸 Drinks & Bar",

    "cafe": "☕ Cafe & Bakery",
    "bakery": "☕ Cafe & Bakery",
    "dessert": "☕ Cafe & Bakery",
    "desserts": "☕ Cafe & Bakery",
    "pastries": "☕ Cafe & Bakery",
    "coffee": "☕ Cafe & Bakery",
    "specialty coffee": "☕ Cafe & Bakery",
    "chocolate": "☕ Cafe & Bakery",
    "brunch": "☕ Cafe & Bakery",
    "bottomless brunch": "☕ Cafe & Bakery",
    "bottomless lunch": "☕ Cafe & Bakery",
    "gelato tasting": "☕ Cafe & Bakery",
    "cookies": "☕ Cafe & Bakery",
    "focaccia": "☕ Cafe & Bakery",

    "italian": "🍕 Italian & Pizza",
    "pizzeria": "🍕 Italian & Pizza",
    "pizza": "🍕 Italian & Pizza",
    "woodfired pizza": "🍕 Italian & Pizza",
    "roman pizza": "🍕 Italian & Pizza",
    "sicilian": "🍕 Italian & Pizza",
    "osteria": "🍕 Italian & Pizza",

    "japanese": "🍣 Asian Eats",
    "izakaya": "🍣 Asian Eats",
    "chinese": "🍣 Asian Eats",
    "dumplings": "🍣 Asian Eats",
    "yum cha": "🍣 Asian Eats",
    "modern asian": "🍣 Asian Eats",
    "asian-italian": "🍣 Asian Eats",
    "robata grill": "🍣 Asian Eats",
    "indian": "🍣 Asian Eats",
    "bombay cafe": "🍣 Asian Eats",

    "mexican": "🌮 Mexican & Latin",
    "tacos": "🌮 Mexican & Latin",
    "spanish": "🌮 Mexican & Latin",
    "tapas": "🌮 Mexican & Latin",

    "french": "🌍 Global Eats",
    "french bistro": "🌍 Global Eats",
    "greek": "🌍 Global Eats",
    "lebanese": "🌍 Global Eats",
    "middle eastern": "🌍 Global Eats",
    "persian": "🌍 Global Eats",
    "jamaican": "🌍 Global Eats",
    "european": "🌍 Global Eats",
    "mediterranean": "🌍 Global Eats",

    "sandwiches": "🍔 Comfort & Quick",
    "pies": "🍔 Comfort & Quick",
    "pie tasting": "🍔 Comfort & Quick",
    "cheap eats": "🍔 Comfort & Quick",
    "falafel": "🍔 Comfort & Quick",
    "diner": "🍔 Comfort & Quick",
    "seafood boil": "🍔 Comfort & Quick",
    
    "seafood": "🦞 Seafood",
    "oyster bar": "🦞 Seafood",
    "steakhouse": "🥩 Steakhouse",
}

for place in places:
    old_vibes = place.get('vibes', [])
    new_vibes = set()
    for v in old_vibes:
        v_low = v.lower()
        if v_low in VIBE_MAP:
            new_vibes.add(VIBE_MAP[v_low])
        else:
            # If it's a completely unknown tag, maybe put it in 'Other' or ignore it to keep UI clean
            pass
            
    # Convert set back to list and sort
    place['vibes'] = sorted(list(new_vibes))

with open(processed_file, "w", encoding="utf-8") as f:
    json.dump(places, f, indent=4, ensure_ascii=False)
    
with open(data_js_file, "w", encoding="utf-8") as f:
    f.write('const processedPlacesData = ' + json.dumps(places, ensure_ascii=False) + ';')

print("Vibes successfully refined!")
