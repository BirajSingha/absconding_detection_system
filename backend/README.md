# Absconding Detection System - Backend Documentation

## Overview

The Absconding Detection System is an AI-powered backend application designed to detect early signs of employee attrition through behavioral anomaly detection, sentiment analysis, and predictive analytics. The system uses three integrated AI tools: **RAG (Retrieval Augmented Generation)**, **n8n (Workflow Automation)**, and **MCP (Model Context Protocol)**.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (copy .env.example to .env)
# Add your API keys: ANTHROPIC_API_KEY, CHROMA_API_KEY, etc.

# Run the application
python run.py
```

Server will start on: **http://localhost:5000**

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────┐
│              AI Tools Layer                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │   RAG    │  │   n8n    │  │   MCP    │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
└───────┼─────────────┼─────────────┼────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼────────────┐
│           Flask REST API Layer                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │Employees │  │  Alerts  │  │Analytics │     │
│  └──────────┘  └──────────┘  └──────────┘     │
└─────────┬───────────────────────┬───────────────┘
          │                       │
┌─────────▼───────────┐  ┌────────▼──────────────┐
│   Services Layer    │  │    Data Layer         │
│ ┌─────────────────┐ │  │ ┌──────────────────┐ │
│ │Anomaly Detector │ │  │ │  SQLite DB       │ │
│ │Sentiment Analyze│ │  │ │  Employee Model  │ │
│ │RAG Service      │ │  │ │  Alert Model     │ │
│ │Vector Store     │ │  │ │  Comm Model      │ │
│ │Slack Service    │ │  │ └──────────────────┘ │
│ └─────────────────┘ │  │ ┌──────────────────┐ │
│                     │  │ │  ChromaDB Cloud  │ │
│                     │  │ │  Vector Store    │ │
│                     │  │ └──────────────────┘ │
└─────────────────────┘  └───────────────────────┘
```

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/
│   │   └── employee.py          # SQLAlchemy models
│   ├── routes/
│   │   ├── employees.py         # Employee CRUD endpoints
│   │   ├── alerts.py            # Alert & analysis endpoints
│   │   ├── analytics.py         # Analytics endpoints
│   │   ├── vector_db.py         # Vector DB endpoints
│   │   └── n8n_webhooks.py      # n8n integration webhooks
│   └── services/
│       ├── anomaly_detector.py  # Behavioral anomaly detection
│       ├── sentiment_analyzer.py # NLP sentiment analysis
│       ├── rag_service.py       # RAG with Claude AI
│       ├── vector_store.py      # ChromaDB operations
│       ├── seed_vector_db.py    # Database seeding
│       └── slack_service.py     # Slack notifications
├── mcp_server.py                # MCP server implementation
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── requirements-mcp.txt         # MCP-specific dependencies
└── test_integration.py          # Integration test suite
```

---

## 🎯 Core Features

### 1. Employee Management

- CRUD operations for employee records
- Performance metrics tracking (productivity, attendance, ratings)
- Department and role management

### 2. Anomaly Detection

- **Productivity Drop Detection**: Flags >30% decline
- **Attendance Issues**: Alerts when <80%
- **Communication Pattern Changes**: Monitors frequency and sentiment
- **Performance Decline**: Tracks rating drops

### 3. Sentiment Analysis

- NLP-based sentiment classification (POSITIVE/NEGATIVE/NEUTRAL)
- Exit intent keyword detection
- Communication source tracking (email, slack, etc.)
- Sentiment score calculation

### 4. RAG (Retrieval Augmented Generation)

- **Vector Database**: ChromaDB Cloud for semantic search
- **LLM Integration**: Claude AI for intelligent analysis
- **Knowledge Base**: HR policies and retention strategies
- **Historical Cases**: Past absconding cases for learning
- **Context-Aware Recommendations**: Tailored advice based on similar cases

### 5. Alert System

- Risk score calculation (0-100)
- Risk level classification (LOW/MEDIUM/HIGH/CRITICAL)
- Confidence scoring
- AI-generated insights and recommendations
- Timeline estimates for potential exit

### 6. Analytics Dashboard

- Risk distribution across organization
- Alert trends over time
- Top at-risk employees ranking
- Department-wise statistics
- Alert summary and status breakdown

### 7. n8n Workflow Integration

- Webhook endpoints for automation
- Batch analysis capabilities
- Single employee analysis triggers
- High-risk employee retrieval

### 8. Slack Notifications (Optional)

- Automatic alerts for HIGH/CRITICAL cases
- Formatted messages with employee details
- Graceful fallback to console logging

### 9. MCP Server

- Exposes resources (employees, alerts, analytics)
- Provides tools for AI assistants
- Real-time data access
- Standardized protocol implementation

---

## 📡 API Endpoints

### Employees

| Method | Endpoint                      | Description                |
| ------ | ----------------------------- | -------------------------- |
| GET    | `/api/employees`              | List all employees         |
| GET    | `/api/employees/<id>`         | Get specific employee      |
| POST   | `/api/employees`              | Create new employee        |
| PUT    | `/api/employees/<id>`         | Update employee            |
| DELETE | `/api/employees/<id>`         | Delete employee            |
| PUT    | `/api/employees/<id>/metrics` | Update performance metrics |

### Alerts

| Method | Endpoint                            | Description                    |
| ------ | ----------------------------------- | ------------------------------ |
| GET    | `/api/alerts`                       | List all alerts (with filters) |
| GET    | `/api/alerts/<id>`                  | Get specific alert             |
| POST   | `/api/alerts/analyze/<employee_id>` | Trigger risk analysis          |
| POST   | `/api/alerts/<id>/outcome`          | Record intervention outcome    |

**Query Parameters for GET /api/alerts**:

- `status`: Filter by status (OPEN, ACKNOWLEDGED, IN_PROGRESS, RESOLVED)
- `risk_level`: Filter by risk level (LOW, MEDIUM, HIGH, CRITICAL)
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)

### Analytics

| Method | Endpoint                               | Description             |
| ------ | -------------------------------------- | ----------------------- |
| GET    | `/api/analytics/risk-distribution`     | Risk level counts       |
| GET    | `/api/analytics/alert-trends`          | Alert trends over time  |
| GET    | `/api/analytics/top-at-risk`           | Top high-risk employees |
| GET    | `/api/analytics/department-stats`      | Department statistics   |
| GET    | `/api/analytics/alert-summary`         | Overall alert summary   |
| GET    | `/api/analytics/employee/<id>/history` | Employee alert history  |

### n8n Webhooks

| Method | Endpoint                             | Description                      |
| ------ | ------------------------------------ | -------------------------------- |
| POST   | `/api/webhooks/n8n/trigger-analysis` | Trigger single employee analysis |
| POST   | `/api/webhooks/n8n/batch-analysis`   | Analyze all active employees     |
| GET    | `/api/webhooks/n8n/get-high-risk`    | Get current high-risk employees  |
| POST   | `/api/webhooks/n8n/alert-created`    | Workflow status tracking         |

### Vector Database

| Method | Endpoint                                    | Description                     |
| ------ | ------------------------------------------- | ------------------------------- |
| GET    | `/api/vector-db/stats`                      | Collection statistics           |
| POST   | `/api/vector-db/search/knowledge`           | Search knowledge base           |
| POST   | `/api/vector-db/search/cases`               | Search historical cases         |
| GET    | `/api/vector-db/search/communications/<id>` | Search employee comms           |
| POST   | `/api/vector-db/seed`                       | Seed database with initial data |
| POST   | `/api/vector-db/add/knowledge`              | Add knowledge document          |

---

## 🗄️ Data Models

### Employee Model

```python
{
    "id": int,
    "employee_id": str (unique),
    "name": str,
    "email": str,
    "phone": str,
    "role": str,
    "department": str,
    "tenure_years": float,
    "manager_id": str,
    "manager_name": str,
    "employment_status": str,
    "productivity_score": float (0-100),
    "attendance_percentage": float (0-100),
    "performance_rating": float (0-4),
    "created_at": datetime,
    "updated_at": datetime
}
```

### Alert Model

```python
{
    "id": int,
    "employee_id": str,
    "risk_score": float (0-100),
    "risk_level": str (LOW/MEDIUM/HIGH/CRITICAL),
    "confidence_score": float,
    "behavioral_indicators": json,
    "sentiment_indicators": json,
    "ai_summary": text,
    "timeline_estimate": str,
    "recommendations": json,
    "status": str,
    "created_at": datetime,
    "updated_at": datetime
}
```

### Communication Model

```python
{
    "id": int,
    "employee_id": str,
    "text": text,
    "source": str,
    "message_id": str,
    "sentiment": str,
    "sentiment_score": float,
    "keywords": json,
    "created_at": datetime
}
```

---

## 🔧 Services

### AnomalyDetector (`anomaly_detector.py`)

Detects behavioral anomalies in employee data.

**Key Methods**:

- `detect_anomalies(employee_id)`: Identifies anomalies
- `calculate_risk_score(anomalies)`: Computes overall risk
- `_detect_communication_anomaly()`: Monitors comm patterns
- `_calculate_severity()`: Scores anomaly severity

**Thresholds**:

- Productivity: < 70%
- Attendance: < 80%
- Performance: < 2.5/4.0

### SentimentAnalyzer (`sentiment_analyzer.py`)

NLP-based sentiment analysis using HuggingFace transformers.

**Key Methods**:

- `analyze_text(text)`: Analyzes single message
- `analyze_communications(comms)`: Batch analysis
- `_detect_exit_keywords()`: Identifies resignation intent

**Exit Keywords**: "quit", "resign", "leave", "frustrated", "toxic", etc.

### RAGService (`rag_service.py`)

Retrieval Augmented Generation with Claude AI.

**Key Methods**:

- `analyze_risk()`: Main RAG analysis
- `store_case_outcome()`: Learns from interventions
- `_build_context()`: Creates AI prompt context

**Components**:

- Vector DB search for similar cases
- Knowledge base retrieval
- Claude AI for insights
- Response parsing

### VectorStore (`vector_store.py`)

ChromaDB Cloud integration for semantic search.

**Collections**:

- `hr_knowledge_base`: HR policies and strategies
- `historical_cases`: Past absconding cases
- `employee_communications`: Communication history

**Key Methods**:

- `search_knowledge()`: Knowledge base search
- `search_similar_cases()`: Find similar past cases
- `add_knowledge_document()`: Store new documents
- `get_collection_stats()`: Collection statistics

### SlackService (`slack_service.py`)

Slack integration for notifications.

**Key Methods**:

- `send_alert()`: Send general message
- `send_high_risk_alert()`: Formatted high-risk alert

**Fallback**: Logs to console if Slack not configured

---

## 🔐 Environment Variables

Create a `.env` file in the backend directory:

```bash
# Database
DATABASE_URL=sqlite:///absconding.db

# Flask
SECRET_KEY=your-secret-key-here

# Anthropic Claude AI
ANTHROPIC_API_KEY=your-anthropic-api-key

# ChromaDB Cloud
CHROMA_API_KEY=your-chroma-api-key
CHROMA_TENANT=your-tenant-id
CHROMA_DATABASE=absconding-detection-system

# Slack (Optional)
SLACK_BOT_TOKEN=xoxb-your-slack-token
SLACK_CHANNEL_ID=C01234567
```

---

## 🧪 Testing

### Run Integration Tests

```bash
python test_integration.py
```

**Tests Include**:

- Employee CRUD operations
- Anomaly detection
- Sentiment analysis
- RAG integration
- Alert generation and retrieval
- Analytics endpoints
- n8n webhooks
- Vector DB operations

### Create Demo Data

```bash
python create_demo_data.py
```

Creates a high-risk employee for testing.

### Manual API Testing

```bash
# Get all employees
curl http://localhost:5000/api/employees

# Trigger analysis
curl -X POST http://localhost:5000/api/alerts/analyze/DEMO001 \
  -H "Content-Type: application/json" \
  -d '{"communications": [{"text": "I quit", "source": "email"}]}'

# Get high-risk employees (for n8n)
curl http://localhost:5000/api/webhooks/n8n/get-high-risk
```

---

## 🤖 AI Tools Integration

### 1. RAG (Retrieval Augmented Generation)

**Status**: ✅ Fully Operational

**Components**:

- **Vector DB**: ChromaDB Cloud (Free tier)
- **LLM**: Claude API (Pay-per-use)
- **Embeddings**: SentenceTransformers (Free)

**How It Works**:

1. Employee data triggers analysis
2. Vector DB searched for similar historical cases
3. HR knowledge base consulted for strategies
4. Context + data sent to Claude AI
5. AI returns risk assessment and recommendations

**Files**:

- `app/services/rag_service.py`
- `app/services/vector_store.py`
- `app/services/seed_vector_db.py`

### 2. n8n (Workflow Automation)

**Status**: ✅ Fully Operational

**Deployment**: Self-hosted Docker (Free, unlimited)

**Use Cases**:

- Daily employee risk scans
- Alert escalation workflows
- Automated notifications
- Report generation

**Webhook Endpoints**: See n8n Webhooks section above

**Files**:

- `app/routes/n8n_webhooks.py`
- `docker-compose.yml` (project root)

**Setup**:

```bash
docker compose up -d
# Access: http://localhost:5678
```

### 3. MCP (Model Context Protocol)

**Status**: ✅ Implemented

**Purpose**: Enables AI assistants to query HR data

**Resources Exposed**:

- Employee list
- Active alerts
- Risk distribution
- Department statistics

**Tools Provided**:

- `analyze_employee_risk`
- `get_employee_details`
- `update_employee_metrics`
- `get_high_risk_employees`

**Files**:

- `mcp_server.py`
- `requirements-mcp.txt`

**Setup**:

```bash
pip install -r requirements-mcp.txt
python mcp_server.py
```

---

## 📊 Analytics & Reporting

### Risk Distribution

Shows count of employees at each risk level.

### Alert Trends

Visualizes alert creation over time (configurable period).

### Department Statistics

- Employee count per department
- Average productivity, attendance, performance
- High-risk alert count

### Top At-Risk

Ranked list of highest-risk employees with details.

---

## 🔔 Notification System

### Slack Integration

**Triggers**: HIGH or CRITICAL risk alerts

**Message Format**:

```
🚨 High Risk Employee Alert

Employee: John Doe (Engineering)
Risk Level: HIGH
Risk Score: 75.5/100
Confidence: 75.5%

📊 Indicators:
- Productivity drop: 35% decrease
- Negative communications detected

🎯 Recommendations:
- Immediate HR meeting
- Compensation review
```

**Fallback**: If Slack not configured, logs to console.

---

## 🚀 Deployment

### Local Development

```bash
python run.py
```

### Production Deployment

**Recommended Stack**:

- **Server**: Gunicorn + Nginx
- **Database**: PostgreSQL (migrate from SQLite)
- **Vector DB**: Self-hosted ChromaDB
- **Process Manager**: Systemd or Supervisor

**Example with Gunicorn**:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

---

## 🔒 Security Considerations

- Use environment variables for all API keys
- Enable HTTPS in production
- Implement API authentication (JWT/OAuth)
- Add rate limiting for public endpoints
- Validate all user inputs
- Sanitize database queries
- Regular security audits

---

## 📈 Performance

**Expected Response Times**:

- Employee CRUD: < 100ms
- Simple analysis: < 2s
- RAG analysis: 3-8s (depends on Claude API)
- Batch analysis: 15-30s (10 employees)
- Vector DB search: < 500ms

**Optimization Tips**:

- Cache frequently accessed data
- Use database indexes
- Implement request queuing for batch jobs
- Monitor Claude API usage and costs

---

## 🐛 Troubleshooting

### Common Issues

**Flask won't start**:

- Check port 5000 isn't in use
- Verify all dependencies installed
- Check `.env` file exists

**RAG returns empty results**:

- Seed vector database: `POST /api/vector-db/seed`
- Check ChromaDB Cloud credentials
- Verify Anthropic API key

**Slack notifications not working**:

- Check `SLACK_BOT_TOKEN` in `.env`
- Verify `SLACK_CHANNEL_ID` correct
- Check bot has permissions in Slack

**n8n can't connect to Flask**:

- Use `host.docker.internal:5000` NOT `localhost:5000`
- Ensure Flask is running
- Check Docker network settings

---

## 📚 Dependencies

### Core Dependencies

- `Flask` - Web framework
- `Flask-SQLAlchemy` - ORM
- `Flask-CORS` - CORS support

### AI & ML

- `anthropic` - Claude AI integration
- `transformers` - HuggingFace models
- `torch` - PyTorch for NLP
- `sentence-transformers` - Embeddings
- `chromadb` - Vector database

### Utilities

- `python-dotenv` - Environment variables
- `requests` - HTTP client
- `pandas`, `numpy` - Data processing
- `slack-sdk` - Slack integration

### Optional

- `mcp` - Model Context Protocol

---

## 🎓 Learning Resources

- **Flask**: https://flask.palletsprojects.com/
- **ChromaDB**: https://docs.trychroma.com/
- **Claude AI**: https://docs.anthropic.com/
- **n8n**: https://docs.n8n.io/
- **Transformers**: https://huggingface.co/docs/transformers/

---

## 📝 License

[Your License Here]

---

## 🤝 Contributing

[Contribution Guidelines]

---

## 📧 Support

For issues and questions:

- Check troubleshooting section above
- Review test results in `/test_integration.py`
- Consult API documentation

---

**Built with ❤️ for predictive HR analytics**
