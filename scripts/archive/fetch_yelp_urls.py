import json
import time
import os
import requests

YELP_API_KEY = os.environ.get('YELP_API_KEY')
headers = {'Authorization': f'Bearer {YELP_API_KEY}'}

processed_file = 'web/processed_places.json'
with open(processed_file, 'r', encoding='utf-8') as f:
    places = json.load(f)

updated = 0
for i, place in enumerate(places):
    # Only try if website is empty
    if not place.get('website'):
        name = place['name']
        location = place['location']
        
        search_url = f"https://api.yelp.com/v3/businesses/search?term={name}&location={location} Sydney&limit=1"
        try:
            res = requests.get(search_url, headers=headers)
            data = res.json()
            if data.get('businesses'):
                b_id = data['businesses'][0]['id']
                detail_url = f"https://api.yelp.com/v3/businesses/{b_id}"
                det_res = requests.get(detail_url, headers=headers)
                det_data = det_res.json()
                
                website = det_data.get('url') # Yelp's business url
                if website:
                    place['website'] = website
                    updated += 1
                    print(f"[{i+1}/{len(places)}] Found Yelp URL for {name}")
                else:
                    print(f"[{i+1}/{len(places)}] No URL for {name}")
            else:
                print(f"[{i+1}/{len(places)}] Not found on Yelp: {name}")
        except Exception as e:
            print(f"[{i+1}/{len(places)}] Error for {name}")
        time.sleep(0.3)
    else:
        pass

with open(processed_file, 'w', encoding='utf-8') as f:
    json.dump(places, f, indent=4, ensure_ascii=False)
    
with open('web/data.js', 'w', encoding='utf-8') as f:
    f.write('const processedPlacesData = ' + json.dumps(places, ensure_ascii=False) + ';')

print(f"Added {updated} Yelp URLs as websites!")
