"""Core configuration module."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""
    
    # API Keys
    LTA_API_KEY: str = os.getenv("LTA_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # LTA DataMall API Configuration
    LTA_BASE_URL: str = "https://datamall2.mytransport.sg/ltaodataservice"
    
    # API Endpoints
    BUS_ARRIVAL_ENDPOINT: str = f"{LTA_BASE_URL}/v3/BusArrival"
    BUS_SERVICES_ENDPOINT: str = f"{LTA_BASE_URL}/BusServices"
    BUS_ROUTES_ENDPOINT: str = f"{LTA_BASE_URL}/BusRoutes"
    BUS_STOPS_ENDPOINT: str = f"{LTA_BASE_URL}/BusStops"
    TRAFFIC_INCIDENTS_ENDPOINT: str = f"{LTA_BASE_URL}/TrafficIncidents"
    TRAFFIC_SPEED_BANDS_ENDPOINT: str = f"{LTA_BASE_URL}/TrafficSpeedBandsv2"
    
    # Agent Configuration
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    MODEL_TEMPERATURE: float = 0.0
    MAX_ITERATIONS: int = 5
    
    # Application Settings
    APP_NAME: str = "Singapore Transport Query Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True


settings = Settings()
