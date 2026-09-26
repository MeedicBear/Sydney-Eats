import os
import json
from apify_client import ApifyClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the ApifyClient with your API token
apify_token = os.getenv("APIFY_API_TOKEN")
if not apify_token:
    print("Error: APIFY_API_TOKEN environment variable not set.")
    print("Please set it in your .env file.")
    exit(1)

client = ApifyClient(apify_token)

# Prepare the Actor input using directUrls
run_input = {
    "directUrls": ["https://www.instagram.com/sydneyonourplate/"],
    "resultsType": "posts",
    "resultsLimit": 200, 
}

print("Starting Apify Instagram Scraper...")

# Run the Actor and wait for it to finish
run = client.actor("apify/instagram-scraper").call(run_input=run_input)

print("Scraping completed. Fetching results from dataset...")

# Fetch and print Actor results from the run's dataset
items = []
dataset_id = run.default_dataset_id
for item in client.dataset(dataset_id).iterate_items():
    items.append(item)

# Save to data directory
output_file = os.path.join(os.path.dirname(__file__), "..", "data", "raw_instagram_data.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(items, f, indent=4, ensure_ascii=False)

print(f"Successfully saved {len(items)} posts to {output_file}")
