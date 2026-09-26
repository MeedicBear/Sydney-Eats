import os
import json
import time
import requests
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
import tempfile

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
    location: str = Field(description="General location or neighborhood, e.g., 'CBD, Sydney'")
    price: str = Field(description="Price range string: '$', '$$', or '$$$'")
    vibes: List[str] = Field(description="List of 2-4 tags describing the vibe")
    description: str = Field(description="A short, catchy 1-2 sentence description based on the video.")
    url: str = Field(description="The Instagram URL of the post")
    coordinates: Optional[Coordinate] = Field(description="Approximate lat/lng coordinates if known. Leave null if unsure.")

class PlacesList(BaseModel):
    places: List[Place]

def download_video(url, temp_file_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(temp_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        return True
    return False

def analyze_missing_videos():
    raw_file = os.path.join(os.path.dirname(__file__), "..", "data", "raw_instagram_data.json")
    processed_file = os.path.join(os.path.dirname(__file__), "..", "data", "processed_places.json")

    with open(raw_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    with open(processed_file, "r", encoding="utf-8") as f:
        processed_data = json.load(f)

    processed_urls = set(p.get("url") for p in processed_data if p.get("url"))
    missing_posts = [p for p in raw_data if p.get("url") not in processed_urls and p.get("videoUrl")]

    print(f"Found {len(missing_posts)} posts with missing locations that have a video URL.")
    
    # LIMIT to 5 for now to test and avoid hitting quotas immediately
    limit = 5
    print(f"Testing with first {limit} videos...")
    missing_posts = missing_posts[:limit]

    new_places = []
    
    for idx, post in enumerate(missing_posts):
        video_url = post["videoUrl"]
        post_url = post.get("url", "")
        caption = post.get("caption", "")
        
        print(f"\n[{idx+1}/{len(missing_posts)}] Analyzing video for post: {post_url}")
        
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_vid:
            temp_path = temp_vid.name
            
        try:
            print("Downloading video...")
            if not download_video(video_url, temp_path):
                print("Failed to download.")
                continue
                
            print("Uploading to Gemini...")
            video_file = client.files.upload(file=temp_path)
            
            # Wait for processing if needed (videos need to be ACTIVE)
            while video_file.state.name == "PROCESSING":
                print(".", end="", flush=True)
                time.sleep(2)
                video_file = client.files.get(name=video_file.name)
            print()
                
            if video_file.state.name == "FAILED":
                print("Video processing failed in Gemini.")
                continue
                
            print("Analyzing video content...")
            prompt = f"""
            Watch this video and read its caption to extract the restaurant or bar being featured in Sydney.
            Pay attention to text overlays on the video, storefront signs, or audio mentions to figure out the Name and Location.
            
            Caption text for context: {caption}
            """
            
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=[video_file, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=PlacesList,
                    temperature=0.1
                )
            )
            
            result = json.loads(response.text)
            places_found = result.get("places", [])
            
            for p in places_found:
                p["url"] = post_url # ensure url matches
                new_places.append(p)
                print(f"✅ Found: {p['name']} - {p['location']}")
            
            if not places_found:
                 print("❌ No place found in this video.")
                
        except Exception as e:
            print(f"Error analyzing video: {e}")
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
            try:
                client.files.delete(name=video_file.name)
            except:
                pass

    if new_places:
        processed_data.extend(new_places)
        with open(processed_file, "w", encoding="utf-8") as f:
            json.dump(processed_data, f, indent=4, ensure_ascii=False)
        print(f"\nSuccessfully added {len(new_places)} new places from video analysis!")

if __name__ == "__main__":
    analyze_missing_videos()
