"""FastAPI routes for transport query agent."""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.models.schemas import TransportQueryRequest, TransportQueryResponse
from app.services.agent_service import TransportAgent
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["transport"])

# Dependency to get agent instance
def get_agent() -> TransportAgent:
    """Get transport agent instance."""
    return TransportAgent()


@router.post("/query", response_model=Dict[str, Any])
async def query_transport(
    request: TransportQueryRequest,
    agent: TransportAgent = Depends(get_agent)
) -> Dict[str, Any]:
    """
    Query the transport agent with a natural language question.
    
    The agent will:
    1. Understand the intent of the query
    2. Extract relevant parameters
    3. Call appropriate LTA APIs
    4. Generate a natural language response
    
    Context can include:
    - weather: Current weather conditions
    - time_of_day: morning/afternoon/evening/night
    - day_of_week: monday/tuesday/etc
    - special_event: Any ongoing events
    - traffic_condition: Current traffic status
    """
    try:
        result = await agent.query(request.query, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
