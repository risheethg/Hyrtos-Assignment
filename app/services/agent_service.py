"""LangGraph-based agent workflow for transport queries."""
from typing import Dict, Any, TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain.tools import Tool
from app.services.transport_service import TransportService
from app.core.config import settings
from app.core.utils import logger
import json
from datetime import datetime


class AgentState(TypedDict):
    """State for the agent workflow."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    intent: str
    extracted_params: Dict[str, Any]
    api_results: Dict[str, Any]
    final_answer: str
    context: Dict[str, Any]
    iteration: int


class TransportAgent:
    """LangGraph-based agent for handling transport queries."""
    
    def __init__(self):
        """Initialize the transport agent."""
        self.transport_service = TransportService()
        self.llm = ChatGroq(
            model=settings.MODEL_NAME,
            temperature=settings.MODEL_TEMPERATURE,
            groq_api_key=settings.GROQ_API_KEY
        )
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("understand_intent", self.understand_intent)
        workflow.add_node("extract_parameters", self.extract_parameters)
        workflow.add_node("call_api", self.call_api)
        workflow.add_node("generate_response", self.generate_response)
        
        # Define edges
        workflow.set_entry_point("understand_intent")
        workflow.add_edge("understand_intent", "extract_parameters")
        workflow.add_edge("extract_parameters", "call_api")
        workflow.add_edge("call_api", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow.compile()
    
    async def understand_intent(self, state: AgentState) -> AgentState:
        """Understand the user's intent from the query."""
        query = state["query"]
        context = state.get("context", {})
        
        system_prompt = """You are an intent classifier for a Singapore public transport assistant.
        Classify the user's query into one of these intents:
        - bus_arrival: Query about when buses are arriving
        - bus_stop_search: Query about finding bus stops
        - route_planning: Query about how to get from A to B
        - traffic_info: Query about traffic conditions
        - service_info: Query about bus services/routes
        - general: General transport questions
        
        Consider context like time of day, weather, special events when available.
        
        Respond with ONLY the intent name."""
        
        context_info = f"\nContext: {json.dumps(context)}" if context else ""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Query: {query}{context_info}")
        ]
        
        response = await self.llm.ainvoke(messages)
        intent = response.content.strip().lower()
        
        logger.info(f"Classified intent: {intent} for query: {query}")
        
        return {
            **state,
            "intent": intent,
            "messages": state["messages"] + [response]
        }
    
    async def extract_parameters(self, state: AgentState) -> AgentState:
        """Extract relevant parameters from the query."""
        query = state["query"]
        intent = state["intent"]
        
        system_prompt = f"""Extract relevant parameters from the user query for intent: {intent}.
        
        For bus_arrival: Extract bus_stop_code, service_no, location_name
        For bus_stop_search: Extract location_name, road_name
        For traffic_info: Extract area, road_name
        For route_planning: Extract origin, destination, time
        
        Return a JSON object with the extracted parameters. If a parameter is not found, omit it.
        Example: {{"bus_stop_code": "83139", "service_no": "190"}}
        
        Respond with ONLY valid JSON."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Query: {query}")
        ]
        
        response = await self.llm.ainvoke(messages)
        
        try:
            extracted_params = json.loads(response.content.strip())
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse parameters: {response.content}")
            extracted_params = {}
        
        logger.info(f"Extracted parameters: {extracted_params}")
        
        return {
            **state,
            "extracted_params": extracted_params,
            "messages": state["messages"] + [response]
        }
    
    async def call_api(self, state: AgentState) -> AgentState:
        """Call appropriate APIs based on intent and parameters."""
        intent = state["intent"]
        params = state["extracted_params"]
        api_results = {}
        
        try:
            if intent == "bus_arrival":
                bus_stop_code = params.get("bus_stop_code")
                service_no = params.get("service_no")
                
                if bus_stop_code:
                    result = await self.transport_service.get_bus_arrival_info(
                        bus_stop_code, service_no
                    )
                    api_results["bus_arrival"] = result
                elif params.get("location_name"):
                    # Search for bus stop first
                    search_result = await self.transport_service.search_bus_stops(
                        params["location_name"]
                    )
                    api_results["bus_stop_search"] = search_result
                    
                    # Get arrival for first match
                    if search_result.get("success") and search_result.get("data"):
                        first_stop = search_result["data"][0]
                        bus_stop_code = first_stop.get("BusStopCode")
                        result = await self.transport_service.get_bus_arrival_info(
                            bus_stop_code, service_no
                        )
                        api_results["bus_arrival"] = result
            
            elif intent == "bus_stop_search":
                location = params.get("location_name") or params.get("road_name", "")
                if location:
                    result = await self.transport_service.search_bus_stops(location)
                    api_results["bus_stop_search"] = result
            
            elif intent == "traffic_info":
                incidents = await self.transport_service.get_traffic_info()
                speed_bands = await self.transport_service.get_traffic_speed_info()
                api_results["traffic_incidents"] = incidents
                api_results["traffic_speed"] = speed_bands
            
            logger.info(f"API calls completed for intent: {intent}")
            
        except Exception as e:
            logger.error(f"Error calling APIs: {e}")
            api_results["error"] = str(e)
        
        return {
            **state,
            "api_results": api_results
        }
    
    async def generate_response(self, state: AgentState) -> AgentState:
        """Generate final response based on API results."""
        query = state["query"]
        intent = state["intent"]
        api_results = state["api_results"]
        context = state.get("context", {})
        
        system_prompt = """You are a helpful Singapore public transport assistant.
        Generate a natural, conversational response to the user's query based on the API results.
        
        Consider the provided context (weather, time, traffic, events) when crafting your response.
        Be concise but informative. If there are issues or no data, explain helpfully.
        
        Format arrival times in a user-friendly way (e.g., "in 3 minutes", "arriving now").
        Include relevant warnings about traffic, weather impacts, or crowding when context suggests it."""
        
        context_str = json.dumps(context, indent=2) if context else "None"
        api_results_str = json.dumps(api_results, indent=2)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
Query: {query}
Intent: {intent}
Context: {context_str}
API Results: {api_results_str}

Generate a helpful response:""")
        ]
        
        response = await self.llm.ainvoke(messages)
        final_answer = response.content.strip()
        
        logger.info(f"Generated response for query: {query}")
        
        return {
            **state,
            "final_answer": final_answer,
            "messages": state["messages"] + [response]
        }
    
    async def query(
        self, 
        user_query: str, 
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process a user query through the agent workflow."""
        try:
            initial_state = {
                "messages": [HumanMessage(content=user_query)],
                "query": user_query,
                "intent": "",
                "extracted_params": {},
                "api_results": {},
                "final_answer": "",
                "context": context or {},
                "iteration": 0
            }
            
            final_state = await self.workflow.ainvoke(initial_state)
            
            return {
                "query": user_query,
                "answer": final_state["final_answer"],
                "intent": final_state["intent"],
                "extracted_params": final_state["extracted_params"],
                "api_results": final_state["api_results"],
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "query": user_query,
                "answer": f"I apologize, but I encountered an error: {str(e)}",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
