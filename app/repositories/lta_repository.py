"""Repository for LTA DataMall API interactions."""
import httpx
from typing import Dict, Any, Optional, List
from app.core.config import settings
from app.core.utils import logger


class LTARepository:
    """Repository for interacting with LTA DataMall APIs."""
    
    def __init__(self):
        """Initialize LTA repository with API credentials."""
        self.api_key = settings.LTA_API_KEY
        self.base_url = settings.LTA_BASE_URL
        self.headers = {
            "AccountKey": self.api_key,
            "accept": "application/json"
        }
    
    async def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to LTA API."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    endpoint,
                    headers=self.headers,
                    params=params or {},
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"Error making request to LTA API: {e}")
            raise
    
    async def get_bus_arrival(
        self, 
        bus_stop_code: str, 
        service_no: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get bus arrival information for a specific bus stop."""
        params = {"BusStopCode": bus_stop_code}
        if service_no:
            params["ServiceNo"] = service_no
        
        logger.info(f"Fetching bus arrival for stop {bus_stop_code}")
        return await self._make_request(settings.BUS_ARRIVAL_ENDPOINT, params)
    
    async def get_bus_services(self, skip: int = 0) -> Dict[str, Any]:
        """Get list of bus services."""
        params = {"$skip": skip}
        logger.info("Fetching bus services")
        return await self._make_request(settings.BUS_SERVICES_ENDPOINT, params)
    
    async def get_bus_routes(
        self, 
        skip: int = 0,
        service_no: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get bus route information."""
        params = {"$skip": skip}
        logger.info(f"Fetching bus routes for service {service_no or 'all'}")
        return await self._make_request(settings.BUS_ROUTES_ENDPOINT, params)
    
    async def get_bus_stops(self, skip: int = 0) -> Dict[str, Any]:
        """Get list of bus stops."""
        params = {"$skip": skip}
        logger.info("Fetching bus stops")
        return await self._make_request(settings.BUS_STOPS_ENDPOINT, params)
    
    async def get_traffic_incidents(self) -> Dict[str, Any]:
        """Get current traffic incidents."""
        logger.info("Fetching traffic incidents")
        return await self._make_request(settings.TRAFFIC_INCIDENTS_ENDPOINT)
    
    async def get_traffic_speed_bands(self) -> Dict[str, Any]:
        """Get traffic speed bands."""
        logger.info("Fetching traffic speed bands")
        return await self._make_request(settings.TRAFFIC_SPEED_BANDS_ENDPOINT)
    
    async def search_bus_stop(self, query: str) -> List[Dict[str, Any]]:
        """Search for bus stops by road name or description."""
        try:
            all_stops = []
            skip = 0
            batch_size = 500
            
            while True:
                # Fetch batch
                result = await self.get_bus_stops(skip=skip)
                stops = result.get("value", [])
                
                if not stops:
                    break
                    
                all_stops.extend(stops)
                
                # If we got fewer than batch_size, we've reached the end
                if len(stops) < batch_size:
                    break
                    
                skip += batch_size
            
            # Search in fetched stops
            query_lower = query.lower()
            matching_stops = [
                stop for stop in all_stops
                if query_lower in stop.get("Description", "").lower() 
                or query_lower in stop.get("RoadName", "").lower()
            ]
            
            return matching_stops[:10]  # Return top 10 matches
        except Exception as e:
            logger.error(f"Error searching bus stops: {e}")
            return []
