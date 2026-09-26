import json

with open('web/processed_places.json', 'r', encoding='utf-8') as f:
    places = json.load(f)

# The mappings to clean up the tags
mappings = {
    "🥢 Asian Eats": "🍣 Asian Eats",
    "🦪 Seafood": "🦞 Seafood",
    "🍔 Comfort & Quick": "🍔 Burgers & Fast Food",
    "🍔 Burgers": "🍔 Burgers & Fast Food",
    "🎵 Live Music": "🎵 Music & Entertainment",
    "🎤 Karaoke": "🎵 Music & Entertainment",
    "🤘 Rock": "🎵 Music & Entertainment",
    "🍻 Pub": "🍻 Pubs & Breweries",
    "🍻 Brewery": "🍻 Pubs & Breweries",
    "🍝 Good Food": "🍽️ Great Dining",
    "🍗 Korean Fried Chicken": "🍣 Asian Eats",
    "🍖 Korean BBQ": "🍣 Asian Eats",
    "🌿 Botanical": "☀️ Outdoor",
    "🌺 Tiki": "🍸 Drinks & Bar",
    "🥩 Steakhouse": "🌍 Global Eats",
}

for place in places:
    new_vibes = []
    for vibe in place.get('vibes', []):
        mapped_vibe = mappings.get(vibe, vibe)
        if mapped_vibe not in new_vibes:
            new_vibes.append(mapped_vibe)
    place['vibes'] = new_vibes

with open('web/processed_places.json', 'w', encoding='utf-8') as f:
    json.dump(places, f, indent=4, ensure_ascii=False)

with open('web/data.js', 'w', encoding='utf-8') as f:
    f.write('const processedPlacesData = ' + json.dumps(places, ensure_ascii=False) + ';')

print("Refined vibes in processed_places.json")
