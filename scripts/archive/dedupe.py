import json
import re

with open('web/processed_places.json', 'r', encoding='utf-8') as f:
    places = json.load(f)

def simplify(name):
    s = name.lower()
    s = re.sub(r'[^a-z0-9]', '', s)
    # common suffixes
    s = s.replace('winebar', '').replace('restaurant', '').replace('bar', '').replace('the', '')
    return s

seen = {}
duplicates = []
unique_places = []

for p in places:
    # Explicitly drop the known duplicate
    if p['id'] == 'place_3852e441':
        duplicates.append(p)
        continue
        
    s = simplify(p['name'])
    if s in seen:
        print(f"DUPLICATE FOUND: {p['name']} ({p['location']}) matches {seen[s]['name']} ({seen[s]['location']})")
        duplicates.append(p)
    else:
        seen[s] = p
        unique_places.append(p)

with open('web/processed_places.json', 'w', encoding='utf-8') as f:
    json.dump(unique_places, f, indent=4, ensure_ascii=False)

with open('web/data.js', 'w', encoding='utf-8') as f:
    f.write('const processedPlacesData = ' + json.dumps(unique_places, ensure_ascii=False) + ';')

print(f"Removed {len(duplicates)} duplicates. Remaining unique places: {len(unique_places)}")
