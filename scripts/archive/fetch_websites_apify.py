import json
import time
import os
import requests

# Load token
token = ''
with open('.env') as f:
    for line in f:
        if line.startswith('APIFY_API_TOKEN='):
            token = line.split('=')[1].strip()

processed_file = 'web/processed_places.json'
with open(processed_file, 'r', encoding='utf-8') as f:
    places = json.load(f)

# Find places that need websites
places_to_search = [p for p in places if not p.get('website')]
if not places_to_search:
    print("All places already have websites!")
    exit(0)

# We can't do all 150 in one query easily without hitting limits/costs, but let's try
# Actually Apify charges per SERP. 160 queries = 160 SERPs = very cheap (a few cents).
queries = []
query_to_place = {}
for p in places_to_search:
    q = f"{p['name']} {p['location']} Sydney official website"
    queries.append(q)
    query_to_place[q] = p['id']

print(f"Submitting {len(queries)} queries to Apify Google Search Scraper...")

run_url = f"https://api.apify.com/v2/acts/apify~google-search-scraper/runs?token={token}"
input_data = {
    "queries": "\n".join(queries),
    "maxPagesPerQuery": 1,
    "resultsPerPage": 3,
    "countryCode": "au"
}
res = requests.post(run_url, json=input_data)
if not res.ok:
    print("Error submitting run:", res.text)
    exit(1)

run_info = res.json()['data']
run_id = run_info['id']
dataset_id = run_info['defaultDatasetId']

print(f"Run started with ID: {run_id}. Waiting for completion...")

while True:
    status_url = f"https://api.apify.com/v2/acts/apify~google-search-scraper/runs/{run_id}?token={token}"
    status_res = requests.get(status_url).json()['data']
    status = status_res['status']
    print(f"Status: {status}")
    if status == 'SUCCEEDED':
        break
    if status in ['FAILED', 'ABORTED', 'TIMED-OUT']:
        print("Run did not succeed.")
        exit(1)
    time.sleep(10)

print("Fetching results...")
data_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={token}"
items = requests.get(data_url).json()

updated = 0
for item in items:
    q = item.get('searchQuery', {}).get('term')
    if not q or q not in query_to_place:
        continue
    
    p_id = query_to_place[q]
    
    # find the place
    place = next((p for p in places if p['id'] == p_id), None)
    if not place: continue
    
    # find first non-aggregator url
    organic = item.get('organicResults', [])
    for result in organic:
        url = result.get('url', '')
        if url and not any(blocked in url.lower() for blocked in ['yelp.', 'tripadvisor.', 'facebook.', 'instagram.', 'tiktok.', 'broadsheet.', 'timeout.', 'concreteplayground.', 'wikipedia.']):
            place['website'] = url
            updated += 1
            print(f"Mapped {url} to {place['name']}")
            break

with open(processed_file, 'w', encoding='utf-8') as f:
    json.dump(places, f, indent=4, ensure_ascii=False)
    
with open('web/data.js', 'w', encoding='utf-8') as f:
    f.write('const processedPlacesData = ' + json.dumps(places, ensure_ascii=False) + ';')

print(f"Successfully added {updated} actual websites via Apify!")
