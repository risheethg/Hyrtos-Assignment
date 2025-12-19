import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv(override=True)

async def test_bus_arrival():
    api_key = os.getenv("LTA_API_KEY")
    headers = {
        "AccountKey": api_key,
        "accept": "application/json"
    }
    
    # Test the v3 endpoint with HTTPS
    bus_stop = "09047"
    url = f"https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival?BusStopCode={bus_stop}"
    
    print(f"\nTesting: {url}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Success! Got bus arrival data")
                print(f"Services available: {len(data.get('Services', []))}")
            else:
                print(f"Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_bus_arrival())
