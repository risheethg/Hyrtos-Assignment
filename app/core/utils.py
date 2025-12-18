"""Core utilities module."""
import logging
from typing import Any, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def format_bus_arrival(arrival_data: Dict[str, Any]) -> str:
    """Format bus arrival data into readable text."""
    try:
        services = arrival_data.get("Services", [])
        if not services:
            return "No bus services found at this stop."
        
        result = []
        for service in services:
            service_no = service.get("ServiceNo", "Unknown")
            next_bus = service.get("NextBus", {})
            next_bus_2 = service.get("NextBus2", {})
            
            est_arrival = next_bus.get("EstimatedArrival", "N/A")
            load = next_bus.get("Load", "N/A")
            
            result.append(
                f"Bus {service_no}: Next arrival in {est_arrival} (Load: {load})"
            )
            
            if next_bus_2.get("EstimatedArrival"):
                est_arrival_2 = next_bus_2.get("EstimatedArrival", "N/A")
                result.append(f"  Following bus in {est_arrival_2}")
        
        return "\n".join(result)
    except Exception as e:
        logger.error(f"Error formatting bus arrival data: {e}")
        return "Error formatting bus arrival information."


def format_traffic_incidents(incidents: list) -> str:
    """Format traffic incidents into readable text."""
    if not incidents:
        return "No traffic incidents reported."
    
    result = []
    for incident in incidents[:5]:  # Limit to 5 incidents
        incident_type = incident.get("Type", "Unknown")
        message = incident.get("Message", "No details")
        result.append(f"- {incident_type}: {message}")
    
    return "\n".join(result)
