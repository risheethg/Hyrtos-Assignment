import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def get_stops():
    api_key = os.getenv("LTA_API_KEY")
    headers = {"AccountKey": api_key, "accept": "application/json"}
    url = "http://datamall2.mytransport.sg/ltaodataservice/BusStops"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        data = response.json()
        stops = data.get("value", [])
        print(f"Fetched {len(stops)} stops.")
        print("Here are 5 valid bus stops you can query:")
        for stop in stops[:5]:
            print(f"- {stop['Description']} (Code: {stop['BusStopCode']}, Road: {stop['RoadName']})")
            
        print("\nTry searching for these names.")

if __name__ == "__main__":
    asyncio.run(get_stops())
