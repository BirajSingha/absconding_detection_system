# Absconding Detection System - Setup Guide

## Overview

This project uses **3 AI tools** as required:

1. ✅ **RAG** (Retrieval Augmented Generation) - ChromaDB + Claude AI
2. ✅ **n8n** - Workflow automation (self-hosted Docker)
3. ✅ **MCP** (Model Context Protocol) - AI assistant integration

## Quick Start

### 1. Start the Flask Backend

```bash
cd backend
.\venv\Scripts\activate  # Windows
python run.py
```

Backend will run on: http://localhost:5000

### 2. Start n8n (Docker)

```bash
# From project root
docker-compose up -d
```

n8n will run on: http://localhost:5678

- **Username**: admin
- **Password**: admin123 (change this!)

### 3. Start MCP Server (Optional)

```bash
cd backend
pip install -r requirements-mcp.txt
python mcp_server.py
```

MCP server runs via stdio for AI assistant integration.

## Detailed Setup

### Prerequisites

- Python 3.9+
- Docker Desktop (for n8n)
- Virtual environment activated

### Backend Configuration

1. **Install Dependencies**:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Environment** (`.env`):

   ```env
   # Database
   DATABASE_URL=sqlite:///absconding.db

   # AI Services
   ANTHROPIC_API_KEY=your_claude_api_key

   # Vector DB (ChromaDB Cloud - Free Tier)
   CHROMA_API_KEY=your_chroma_key
   CHROMA_TENANT=your_tenant_id
   CHROMA_DATABASE=absconding-detection-system

   # Slack (Optional)
   SLACK_BOT_TOKEN=xoxb-your-token
   SLACK_CHANNEL_ID=C01234567
   ```

3. **Initialize Database**:
   ```bash
   python run.py
   ```
   This automatically creates tables on first run.

### n8n Setup

1. **Start n8n**:

   ```bash
   docker-compose up -d
   ```

2. **Access UI**:

   - Open http://localhost:5678
   - Login with admin/admin123

3. **Configure Flask Connection**:

   - In n8n HTTP Request nodes, use URL: `http://host.docker.internal:5000`
   - This connects n8n (Docker) to Flask (host machine)

4. **Import Workflows**:
   - Navigate to `n8n-workflows/` directory
   - Import example workflows via n8n UI
   - See `n8n-workflows/README.md` for details

### MCP Setup

1. **Install MCP Package**:

   ```bash
   cd backend
   pip install -r requirements-mcp.txt
   ```

2. **Run MCP Server**:

   ```bash
   python mcp_server.py
   ```

3. **Configure AI Assistant**:
   Add MCP server to your AI assistant config (Claude Desktop, etc.):
   ```json
   {
     "mcpServers": {
       "absconding-detection": {
         "command": "python",
         "args": ["C:/path/to/backend/mcp_server.py"]
       }
     }
   }
   ```

## API Endpoints

### Employees

- `GET /api/employees` - List all employees
- `POST /api/employees` - Create employee
- `PUT /api/employees/<id>` - Update employee
- `PUT /api/employees/<id>/metrics` - Update metrics

### Alerts

- `GET /api/alerts` - List alerts (with filters)
- `GET /api/alerts/<id>` - Get specific alert
- `POST /api/alerts/analyze/<employee_id>` - Trigger analysis
- `POST /api/alerts/<id>/outcome` - Record outcome

### Analytics

- `GET /api/analytics/risk-distribution` - Risk level counts
- `GET /api/analytics/alert-trends` - Alert trends over time
- `GET /api/analytics/top-at-risk` - Top high-risk employees
- `GET /api/analytics/department-stats` - Department statistics

### n8n Webhooks

- `POST /api/webhooks/n8n/trigger-analysis` - Trigger single analysis
- `POST /api/webhooks/n8n/batch-analysis` - Analyze all employees
- `GET /api/webhooks/n8n/get-high-risk` - Get high-risk list

### Vector DB

- `GET /api/vector-db/stats` - Collection statistics
- `POST /api/vector-db/search/knowledge` - Search knowledge base
- `POST /api/vector-db/search/cases` - Search historical cases
- `POST /api/vector-db/seed` - Seed database

## How the AI Tools Work Together

```
┌─────────────────────────────────────────────────┐
│              n8n Workflows (Automation)         │
│  - Daily scans                                  │
│  - Alert escalation                             │
│  - Scheduled reports                            │
└──────────────────┬──────────────────────────────┘
                   │ Triggers via webhooks
                   ↓
┌─────────────────────────────────────────────────┐
│           Flask Backend API                     │
│  - Employee management                          │
│  - Anomaly detection                            │
│  - Sentiment analysis                           │
└─────────┬──────────────────────┬────────────────┘
          │                      │
          │ Uses RAG             │ Exposes via MCP
          ↓                      ↓
┌──────────────────┐   ┌────────────────────────┐
│  RAG Service     │   │   MCP Server           │
│  - Vector DB     │   │   - Resources          │
│  - Claude AI     │   │   - Tools              │
│  - Historical    │   │   - AI Assistant       │
│    learning      │   │     Integration        │
└──────────────────┘   └────────────────────────┘
```

## Testing the Integration

### Test n8n → Flask Connection

1. In n8n, create a simple workflow:

   - Add "HTTP Request" node
   - URL: `http://host.docker.internal:5000/api/webhooks/n8n/get-high-risk`
   - Method: GET
   - Execute

2. Should return list of high-risk employees

### Test RAG

```bash
# Via Python
from app.services.rag_service import get_rag_service
rag = get_rag_service()
result = rag.analyze_risk(employee_data, anomalies, sentiment_data)
print(result)
```

### Test MCP

Use an MCP-compatible AI assistant (like Claude Desktop):

```
"List all high-risk employees using the absconding detection system"
```

The MCP server will return real employee data.

## Production Deployment

### Security Checklist

- [ ] Change n8n default password
- [ ] Use environment variables for all API keys
- [ ] Enable HTTPS for webhooks
- [ ] Set up proper authentication for Flask API
- [ ] Rotate Slack tokens regularly
- [ ] Use PostgreSQL instead of SQLite for n8n

### Scaling

- **n8n**: Already scalable (self-hosted Docker)
- **RAG**: Can switch to self-hosted ChromaDB if needed
- **MCP**: Stateless, can run multiple instances
- **Flask**: Use Gunicorn + Nginx for production

## Troubleshooting

### n8n can't reach Flask

- Use `host.docker.internal:5000` instead of `localhost:5000`
- Check Docker network: `docker network ls`

### MCP server not responding

- Ensure it's running in the background
- Check stdio connection in AI assistant config

### RAG returns empty results

- Seed the vector database: `POST /api/vector-db/seed`
- Check ChromaDB Cloud connection

### Slack notifications not sending

- Verify `SLACK_BOT_TOKEN` and `SLACK_CHANNEL_ID` in `.env`
- Check bot has proper permissions in Slack workspace

## Next Steps

1. ✅ Import n8n workflow examples
2. ✅ Seed vector database with HR policies
3. ✅ Configure Slack notifications
4. ✅ Test end-to-end workflow
5. ✅ Add historical case data for better AI predictions

## Support

For issues:

1. Check logs: `docker logs absconding-n8n`
2. Review Flask console output
3. Verify all environment variables are set
