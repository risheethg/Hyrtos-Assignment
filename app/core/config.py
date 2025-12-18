"""Core configuration module."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""
    
    # API Keys
    LTA_API_KEY: str = os.getenv("LTA_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # LTA DataMall API Configuration
    LTA_BASE_URL: str = "http://datamall2.mytransport.sg/ltaodataservice"
    
    # API Endpoints
    BUS_ARRIVAL_ENDPOINT: str = f"{LTA_BASE_URL}/BusArrivalv2"
    BUS_SERVICES_ENDPOINT: str = f"{LTA_BASE_URL}/BusServices"
    BUS_ROUTES_ENDPOINT: str = f"{LTA_BASE_URL}/BusRoutes"
    BUS_STOPS_ENDPOINT: str = f"{LTA_BASE_URL}/BusStops"
    TRAFFIC_INCIDENTS_ENDPOINT: str = f"{LTA_BASE_URL}/TrafficIncidents"
    TRAFFIC_SPEED_BANDS_ENDPOINT: str = f"{LTA_BASE_URL}/TrafficSpeedBandsv2"
    
    # Agent Configuration
    MODEL_NAME: str = "gemini-pro"
    MODEL_TEMPERATURE: float = 0.0
    MAX_ITERATIONS: int = 5
    
    # Application Settings
    APP_NAME: str = "Singapore Transport Query Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True


settings = Settings()
