"""Service layer for transport query agent."""
import json
from typing import Dict, Any, List
from datetime import datetime
from app.repositories.lta_repository import LTARepository
from app.core.utils import logger


class TransportService:
    """Service for handling transport-related operations."""
    
    def __init__(self):
        """Initialize transport service."""
        self.lta_repo = LTARepository()
    
    async def get_bus_arrival_info(
        self, 
        bus_stop_code: str, 
        service_no: str = None
    ) -> Dict[str, Any]:
        """Get formatted bus arrival information."""
        try:
            result = await self.lta_repo.get_bus_arrival(bus_stop_code, service_no)
            return {
                "success": True,
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting bus arrival info: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def search_bus_stops(self, query: str) -> Dict[str, Any]:
        """Search for bus stops."""
        try:
            stops = await self.lta_repo.search_bus_stop(query)
            return {
                "success": True,
                "data": stops,
                "count": len(stops)
            }
        except Exception as e:
            logger.error(f"Error searching bus stops: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_traffic_info(self) -> Dict[str, Any]:
        """Get current traffic information."""
        try:
            incidents = await self.lta_repo.get_traffic_incidents()
            return {
                "success": True,
                "data": incidents,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting traffic info: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_traffic_speed_info(self) -> Dict[str, Any]:
        """Get traffic speed band information."""
        try:
            speed_bands = await self.lta_repo.get_traffic_speed_bands()
            return {
                "success": True,
                "data": speed_bands,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting traffic speed info: {e}")
            return {
                "success": False,
                "error": str(e)
            }
