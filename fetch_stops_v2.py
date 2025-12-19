import os
import httpx
import asyncio
from dotenv import load_dotenv

# Force reload to ensure we get the latest env vars
load_dotenv(override=True)

async def get_stops():
    api_key = os.getenv("LTA_API_KEY")
    if not api_key:
        print("Error: LTA_API_KEY not found in environment variables.")
        return

    print(f"Using LTA_API_KEY: {api_key[:4]}...{api_key[-4:]}")
    
    headers = {
        "AccountKey": api_key,
        "accept": "application/json"
    }
    url = "https://datamall2.mytransport.sg/ltaodataservice/BusStops"
    
    print(f"Requesting: {url}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"Response Headers: {response.headers}")
                print(f"Response Text: {response.text[:500]}")
                return

            data = response.json()
            stops = data.get("value", [])
            print(f"Fetched {len(stops)} stops.")
            
            if stops:
                print("\nHere are 5 valid bus stops you can query:")
                for stop in stops[:5]:
                    print(f"- {stop['Description']} (Code: {stop['BusStopCode']}, Road: {stop['RoadName']})")
                print("\nTry searching for these names.")
            else:
                print("No stops found in the response.")
                
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(get_stops())
