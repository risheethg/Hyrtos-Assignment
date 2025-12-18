"""Pydantic models for API request/response validation."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class BusArrivalRequest(BaseModel):
    """Request model for bus arrival queries."""
    bus_stop_code: str = Field(..., description="Bus stop code")
    service_no: Optional[str] = Field(None, description="Specific bus service number")


class BusArrivalResponse(BaseModel):
    """Response model for bus arrival data."""
    bus_stop_code: str
    services: List[Dict[str, Any]]
    timestamp: datetime


class TransportQueryRequest(BaseModel):
    """Request model for general transport queries."""
    query: str = Field(..., description="User query about Singapore transport")
    context: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Additional context like weather, time, location"
    )


class TransportQueryResponse(BaseModel):
    """Response model for transport queries."""
    query: str
    answer: str
    sources: Optional[List[str]] = None
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


class AgentState(BaseModel):
    """State model for the agent workflow."""
    query: str
    context: Dict[str, Any] = Field(default_factory=dict)
    intent: Optional[str] = None
    api_calls: List[str] = Field(default_factory=list)
    api_results: Dict[str, Any] = Field(default_factory=dict)
    answer: Optional[str] = None
    error: Optional[str] = None
    iteration: int = 0


class BusStop(BaseModel):
    """Model for bus stop information."""
    bus_stop_code: str
    road_name: str
    description: str
    latitude: float
    longitude: float


class BusService(BaseModel):
    """Model for bus service information."""
    service_no: str
    operator: str
    direction: int
    category: str
    origin_code: str
    destination_code: str


class TrafficIncident(BaseModel):
    """Model for traffic incident."""
    type: str
    latitude: float
    longitude: float
    message: str
