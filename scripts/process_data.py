import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable not set.")
    exit(1)

client = genai.Client(api_key=api_key)

class Coordinate(BaseModel):
    lat: float = Field(description="Latitude")
    lng: float = Field(description="Longitude")

class Place(BaseModel):
    id: str = Field(description="Unique ID for this place, e.g., slugified name")
    name: str = Field(description="Name of the restaurant or bar")
    location: str = Field(description="General location or neighborhood, e.g., 'CBD, Sydney' or specific address if available")
    price: str = Field(description="Price range string: '$', '$$', or '$$$'")
    vibes: List[str] = Field(description="List of 2-4 tags describing the vibe, e.g., 'Romantic', 'Casual', 'Cocktails'")
    description: str = Field(description="A short, catchy 1-2 sentence description based on the post.")
    url: str = Field(description="The Instagram URL of the post")
    coordinates: Optional[Coordinate] = Field(description="Approximate lat/lng coordinates if known. Leave null if unsure.")

class PlacesList(BaseModel):
    places: List[Place]

def process_posts():
    input_file = os.path.join(os.path.dirname(__file__), "..", "data", "raw_instagram_data.json")
    output_file = os.path.join(os.path.dirname(__file__), "..", "data", "processed_places.json")

    with open(input_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    batch_size = 50
    all_places = []
    
    # Process in batches to avoid token limits / JSON cutoff
    for i in range(0, len(raw_data), batch_size):
        batch = raw_data[i:i+batch_size]
        posts_text = ""
        for idx, post in enumerate(batch):
            url = post.get("url", "")
            caption = post.get("caption", "No caption")
            caption = caption[:1000] 
            posts_text += f"--- POST {i+idx} ---\nURL: {url}\nCaption: {caption}\n\n"

        print(f"Processing batch {i//batch_size + 1} (Posts {i} to {i+len(batch)-1})...")

        prompt = f"""
        You are an expert food and lifestyle curator in Sydney. 
        Extract all the bars and places to eat mentioned in these Instagram posts.

        Rules:
        1. Extract Name, Location, Price ($, $$, or $$$), Vibes (tags), Description, and Instagram URL.
        2. Approximate the coordinates (lat/lng) if known.
        3. Do NOT output duplicate places. Merge information if necessary.
        4. Make the description short and catchy.

        Here are the posts:
        {posts_text}
        """

        try:
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=PlacesList,
                    temperature=0.1
                ),
            )
            result_json = json.loads(response.text)
            all_places.extend(result_json.get("places", []))
            print(f"Extracted {len(result_json.get('places', []))} places from batch.")
        except Exception as e:
            print(f"Error during Gemini processing for batch {i//batch_size + 1}: {e}")

    # Remove overall duplicates by ID
    unique_places = {}
    for place in all_places:
        unique_places[place["id"]] = place

    final_places = list(unique_places.values())

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_places, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully processed and saved {len(final_places)} unique places to {output_file}")

if __name__ == "__main__":
    process_posts()
