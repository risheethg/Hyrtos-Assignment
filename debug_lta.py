import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv(override=True)

async def check_api_and_count():
    api_key = os.getenv("LTA_API_KEY")
    print(f"Checking API Key: {api_key[:4]}...{api_key[-4:] if api_key else 'None'}")
    
    headers = {
        "AccountKey": api_key,
        "accept": "application/json"
    }
    # Use the HTTPS url
    url = "https://datamall2.mytransport.sg/ltaodataservice/BusStops"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                stops = data.get("value", [])
                print(f"Success! Fetched {len(stops)} stops in first batch.")
                
                # Check if Orchard is in this batch
                orchard = [s for s in stops if "Orchard" in s.get("Description", "")]
                print(f"Found {len(orchard)} stops with 'Orchard' in this batch.")
            else:
                print(f"Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(check_api_and_count())
