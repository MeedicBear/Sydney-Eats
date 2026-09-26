import json
with open('web/processed_places.json', 'r', encoding='utf-8') as f:
    places = json.load(f)

for p in places:
    if 'nick' in p['name'].lower():
        print(f"{p['id']} - {p['name']} - {p['location']}")
