# Singapore Transport Query Agent

**Agentic Workflow for Singapore Public Transport Queries using LangGraph**

This project implements an intelligent agent that answers natural language queries about Singapore public transport using real-time data from LTA DataMall APIs. The agent is built with LangGraph for workflow orchestration and uses a clean layered backend architecture with FastAPI.

## Project Overview

### What Does This Do?

The agent can handle various transport-related queries with contextual awareness:

- **Bus Arrivals**: "When is the next bus 190 arriving at Clementi MRT?"
- **Stop Search**: "Where can I find bus stops near Marina Bay Sands?"
- **Traffic Info**: "What's the traffic like on Orchard Road right now?"
- **Route Planning**: "How do I get from Punggol to NUS?"

### Key Features

- **Contextual Intelligence**: Considers weather, time of day, traffic conditions, and special events
- **Multi-Step Reasoning**: LangGraph workflow with intent classification → parameter extraction → API calls → response generation
- **Production-Ready**: Clean layered architecture suitable for deployment
- **Real-Time Data**: Integrates with LTA DataMall APIs for live transport information

## Architecture

### Layered Backend Structure

```
app/
├── core/           # Configuration, utilities, and shared logic
├── models/         # Pydantic schemas for data validation
├── repositories/   # External API integrations (LTA DataMall)
├── services/       # Business logic and agent orchestration
└── routes/         # FastAPI endpoints
```

### LangGraph Agent Workflow

```
User Query
    ↓
[Intent Understanding] → Classify query type
    ↓
[Parameter Extraction] → Extract bus stops, service numbers, etc.
    ↓
[API Execution] → Call relevant LTA DataMall APIs
    ↓
[Response Generation] → Create natural language response
    ↓
Final Answer
```

### Technology Stack

- **Framework**: FastAPI for REST API
- **Agent Orchestration**: LangGraph for multi-step workflows
- **LLM**: Google Gemini Pro (configurable for other providers)
- **APIs**: LTA DataMall for real-time transport data
- **Validation**: Pydantic for request/response schemas
- **Async**: httpx for asynchronous API calls

## Quick Start

### Prerequisites

- Python 3.10+
- LTA DataMall API Key ([Get it here](https://datamall.lta.gov.sg/content/datamall/en/request-for-api.html))
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone and navigate to the project**:
```powershell
cd "c:\Dev\Hyrtos Assignment"
```

2. **Create virtual environment**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies**:
```powershell
pip install -r requirements.txt
```

4. **Configure environment variables**:
```powershell
# Copy example env file
cp .env.example .env

# Edit .env and add your API keys:
# LTA_API_KEY=your_lta_api_key_here
# GEMINI_API_KEY=your_gemini_api_key_here
```

### Running the Application

#### Option 1: Jupyter Notebook (Recommended for Demo)

```powershell
jupyter notebook transport_agent_demo.ipynb
```

The notebook contains:
- Complete implementation walkthrough
- 10 diverse user query simulations
- Results analysis and visualization
- Inline documentation and explanations

#### Option 2: FastAPI Server

```powershell
python main.py
```

Then access:
- API Docs: http://localhost:8000/docs
- Swagger UI: http://localhost:8000/redoc

#### Option 3: Using uvicorn

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Usage Examples

### Using the Jupyter Notebook

Open `transport_agent_demo.ipynb` and run all cells. The notebook includes:

1. **Setup**: Initialize the agent and dependencies
2. **10 User Simulations**: Diverse queries with various contexts
3. **Results Analysis**: Intent distribution, context variety
4. **Documentation**: Design decisions and deployment strategy

### Using the API

```python
import httpx

# Query the agent
response = httpx.post(
    "http://localhost:8000/api/v1/query",
    json={
        "query": "When is the next bus arriving at Bishan?",
        "context": {
            "time_of_day": "morning",
            "weather": "rainy",
            "traffic_condition": "heavy"
        }
    }
)

print(response.json()["answer"])
```

### Programmatic Usage

```python
from app.services.agent_service import TransportAgent

agent = TransportAgent()

result = await agent.query(
    user_query="What's the traffic like on PIE?",
    context={
        "time_of_day": "evening",
        "hour": 18,
        "day_of_week": "Friday"
    }
)

print(result["answer"])
```

## Testing

The Jupyter notebook includes comprehensive testing with 10 diverse scenarios covering:

1. **Morning rush hour** with heavy rain
2. **Evening with special events** (National Day)
3. **Late night** bus availability
4. **Weekend with weather impacts** (thunderstorm)
5. **Public holidays** (Chinese New Year)
6. **Traffic incidents** in CBD
7. **Location-based queries** (Marina Bay)
8. **Peak hour with road works**
9. **Off-peak with good weather**
10. **Complex multi-leg routes**

Each test includes:
- Contextual information (weather, time, events, traffic)
- Intent classification results
- Extracted parameters
- API responses
- Natural language answers

## Design Decisions

### 1. Workflow Design

**Why LangGraph?**
- Provides clear state management for multi-step reasoning
- Enables easy visualization of agent decision flow
- Supports conditional branching and loops
- Makes debugging agent behavior straightforward

**Node Responsibilities**:
- `understand_intent`: Classify user query into action categories
- `extract_parameters`: Pull out entities like bus stops, service numbers
- `call_api`: Execute appropriate LTA API calls based on intent
- `generate_response`: Create contextually-aware natural language response

### 2. Context Handling

The agent considers multiple contextual factors:

- **Weather**: Impacts delays and passenger volumes
- **Time of Day**: Affects service frequency
- **Day of Week**: Different schedules for weekdays/weekends
- **Special Events**: Major events affecting transport
- **Traffic Conditions**: Real-time traffic impacts

This allows responses like:
> "Due to the heavy rain and rush hour traffic, buses may be delayed by 5-10 minutes. The next bus 190 is expected at 8:15 AM."

### 3. Layered Architecture

**Repository Pattern**:
- Abstracts LTA API interactions
- Easy to mock for testing
- Centralized error handling

**Service Layer**:
- Contains business logic
- Orchestrates multiple operations
- Manages state transitions

**Route Layer**:
- Thin controllers
- Input validation
- Response formatting

### 4. Error Handling

- Graceful degradation when APIs are unavailable
- Informative error messages to users
- Comprehensive logging for debugging
- Fallback responses when LLM fails

## Deployment Strategy

### Production Deployment

#### 1. Containerization

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LTA_API_KEY=${LTA_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    deploy:
      replicas: 3
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

#### 2. Cloud Deployment Options

**AWS**:
- ECS/EKS for container orchestration
- API Gateway for request routing
- ElastiCache (Redis) for caching
- CloudWatch for monitoring

**Azure**:
- AKS for Kubernetes
- Azure API Management
- Azure Cache for Redis
- Application Insights

**GCP**:
- GKE for container management
- Cloud Load Balancing
- Memorystore for Redis
- Cloud Monitoring

#### 3. Scalability

**Horizontal Scaling**:
- Deploy multiple API instances
- Load balancer distributes traffic
- Stateless design allows easy scaling

**Caching Strategy**:
```python
# Cache TTLs
- Bus stops: 24 hours (rarely change)
- Bus arrivals: 30 seconds (real-time data)
- Traffic info: 5 minutes
- Common queries: 1 minute
```

**Async Processing**:
- Use message queues for heavy operations
- Background workers for batch processing
- WebSocket for real-time updates

#### 4. Monitoring

**Metrics to Track**:
- API response time (p50, p95, p99)
- Request rate and error rate
- LLM token usage and costs
- LTA API response times
- Cache hit rates

**Tools**:
- Prometheus + Grafana for metrics
- ELK Stack for logs
- OpenTelemetry for tracing
- Sentry for error tracking

#### 5. Security

- API key authentication
- Rate limiting (100 req/min per user)
- HTTPS only (TLS 1.3)
- Input sanitization
- Secrets management (AWS Secrets Manager)
- Regular security audits

#### 6. Cost Optimization

**LLM Costs**:
- Cache common queries
- Use smaller models for classification
- Implement query deduplication
- Monitor token usage

**Infrastructure**:
- Auto-scaling based on traffic
- Spot instances for non-critical workloads
- Reserved instances for baseline

#### 7. CI/CD Pipeline

```yaml
# GitHub Actions example
name: Deploy
on: [push]

jobs:
  test:
    - Run unit tests
    - Run integration tests
    - Check coverage (>80%)
  
  build:
    - Build Docker image
    - Security scan
    - Push to registry
  
  deploy:
    - Deploy to staging
    - Smoke tests
    - Deploy to production
```

#### 8. Performance Targets

- **Response Time**: < 2 seconds (p95)
- **Availability**: 99.9% uptime
- **Throughput**: 1000 req/sec
- **Error Rate**: < 0.1%

## Evaluation Criteria Coverage

### 1. Agentic Workflow Design ✅

- Multi-step LangGraph workflow with clear node responsibilities
- State management between workflow steps
- Conditional logic based on intent classification
- Modular design allowing easy improvements

### 2. Variety of Inputs ✅

The simulation includes diverse contexts:
- **Weather**: Rain, thunderstorm, fog, clear, sunny
- **Traffic**: Rush hour, accidents, road works, smooth
- **Time**: Morning, afternoon, evening, night
- **Special Events**: National Day, F1, Chinese New Year, exams, school holidays
- **Days**: Weekdays, weekends, public holidays

### 3. Solution Structure ✅

- Clean layered architecture (routes, models, services, repos, core)
- Separation of concerns
- Async/await for performance
- Pydantic for type safety
- Comprehensive error handling

### 4. Documentation ✅

- Inline code comments
- Jupyter notebook with explanations
- Architecture diagrams and workflow visualization
- Usage examples
- Comprehensive README

### 5. Deployment Understanding ✅

- Containerization strategy
- Cloud deployment options
- Scalability considerations
- Monitoring and observability
- Security best practices
- Cost optimization strategies
- CI/CD pipeline design

## Troubleshooting

### Common Issues

**1. API Key Not Found**
```
Error: LTA_API_KEY not configured
Solution: Ensure .env file exists with valid API keys
```

**2. LLM Rate Limiting**
```
Error: Rate limit exceeded
Solution: Add delays between requests or upgrade API tier
```

**3. Import Errors**
```
Error: ModuleNotFoundError
Solution: Ensure virtual environment is activated and dependencies installed
```

### Debug Mode

Enable detailed logging:
```python
# In app/core/config.py
DEBUG = True
```

## Key Assumptions

1. **Valid API Access**: LTA DataMall API key is valid and active
2. **LLM Availability**: Google Gemini API (or alternative) is accessible
3. **Bus Stop Knowledge**: Users may not know exact bus stop codes
4. **Context Format**: Context is provided in structured format
5. **English Language**: Queries are in English

## Future Enhancements

1. **Multi-Modal Transport**: Add MRT, trains, taxis
2. **Route Optimization**: Implement shortest path algorithms
3. **Real-Time Location**: GPS integration for user location
4. **Auto-Context**: Fetch weather/traffic automatically
5. **User Preferences**: Learn user patterns
6. **Voice Interface**: Speech-to-text integration
7. **Mobile App**: Native iOS/Android apps
8. **Push Notifications**: Service alerts and delays

## License

This project is created as a take-home assessment and is for demonstration purposes.

## Contact

For questions or clarifications about this implementation, please reach out to the assessment coordinator.

---

**Note**: Remember to replace API keys in `.env` file with your actual credentials before running the application.
