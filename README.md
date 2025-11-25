# Absconding Detection System

> **AI-Powered Employee Attrition Risk Prediction System**  
> Detect early signs of employee resignation using behavioral anomaly detection, sentiment analysis, and predictive analytics.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Overview

The **Absconding Detection System** is an intelligent HR analytics platform that predicts employee attrition risk **2-4 weeks** before resignation. Using advanced AI/ML techniques, it analyzes behavioral patterns, communication sentiment, and performance metrics to provide actionable insights for proactive retention.

### Key Features

- 🤖 **AI-Powered Risk Analysis** - Claude AI + RAG for intelligent insights
- 📊 **Behavioral Anomaly Detection** - Real-time monitoring of productivity, attendance
- 💬 **Sentiment Analysis** - NLP-based communication analysis with exit intent detection
- 📧 **Multi-Channel Alerts** - Email + Slack notifications with beautiful HTML templates
- 🔄 **Workflow Automation** - n8n integration for automated processes
- 📈 **Analytics Dashboard** - Comprehensive HR analytics and reporting
- 🎯 **High Accuracy** - 85%+ prediction accuracy with confidence scoring

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Frontend (Next.js)                 │
│  Dashboard | Analytics | Employee Management   │
└─────────────────┬───────────────────────────────┘
                  │ REST API
┌─────────────────▼───────────────────────────────┐
│           Backend (Flask + Python)              │
├─────────────────────────────────────────────────┤
│  Anomaly Detection | Sentiment Analysis | RAG  │
├─────────────────────────────────────────────────┤
│  SQLite/PostgreSQL | ChromaDB Cloud | n8n      │
└─────────────────────────────────────────────────┘
```

### Technology Stack

**Backend**

- **Framework**: Flask (Python 3.11+)
- **AI/ML**: Anthropic Claude, HuggingFace Transformers, scikit-learn
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Vector DB**: ChromaDB Cloud
- **Automation**: n8n (self-hosted)

**Frontend** (Planned)

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- Docker (for n8n)
- Git

### Installation

```bash
# 1. Clone repository
git clone https://github.com/BirajSingha/absconding-detection-system.git
cd absconding-detection-system

# 2. Backend setup
cd backend
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Start backend
python run.py

# 5. Start n8n (optional - for workflow automation)
docker compose up -d
```

**Backend**: http://localhost:5000  
**n8n Dashboard**: http://localhost:5678

---

## 📁 Project Structure

```
absconding-detection-system/
├── backend/                    # Flask REST API
│   ├── app/
│   │   ├── models/            # SQLAlchemy models
│   │   ├── routes/            # API endpoints
│   │   └── services/          # Business logic
│   ├── .env                   # Environment configuration
│   ├── run.py                 # Application entry point
│   └── README.md              # Backend documentation
├── frontend/                   # Next.js application (planned)
│   └── README.md              # Frontend documentation
├── n8n-workflows/             # Workflow automation
│   └── README.md              # n8n documentation
├── docker-compose.yml         # n8n container configuration
└── README.md                  # This file
```

---

## 🎯 Core Features

### 1. **Risk Prediction**

Analyzes multiple data points to calculate risk score (0-100):

- Productivity trends
- Attendance patterns
- Performance metrics
- Communication sentiment
- Historical case similarity

**Risk Levels**: LOW | MEDIUM | HIGH | CRITICAL

### 2. **Anomaly Detection**

Monitors behavioral indicators:

- ✓ Productivity drops (>30% decline)
- ✓ Attendance issues (<80%)
- ✓ Performance decline
- ✓ Communication pattern changes

### 3. **Sentiment Analysis**

NLP-powered analysis of employee communications:

- Overall sentiment classification
- Exit intent keyword detection
- Sentiment trend tracking
- Multi-source analysis (email, Slack, surveys)

### 4. **RAG (Retrieval Augmented Generation)**

AI-powered insights using:

- ChromaDB vector database
- Claude AI (Anthropic)
- Historical case knowledge
- HR best practices database

### 5. **Smart Notifications**

Dual-channel alerting system:

- **Email**: Professional HTML templates with risk details
- **Slack**: Real-time team notifications
- **Configurable**: Choose channels and thresholds

### 6. **Analytics Dashboard**

Comprehensive HR insights:

- Risk distribution charts
- Alert trends over time
- Department statistics
- Top at-risk employees

---

## 📡 API Endpoints

### Employees

```http
GET    /api/employees              # List all employees
POST   /api/employees              # Create employee
GET    /api/employees/:id          # Get employee details
PUT    /api/employees/:id          # Update employee
DELETE /api/employees/:id          # Delete employee
PUT    /api/employees/:id/metrics  # Update performance metrics
```

### Alerts

```http
GET  /api/alerts                    # List alerts (with filters)
GET  /api/alerts/:id                # Get alert details
POST /api/alerts/analyze/:emp_id   # Trigger risk analysis
POST /api/alerts/:id/outcome        # Record intervention outcome
```

### Analytics

```http
GET /api/analytics/risk-distribution  # Risk level distribution
GET /api/analytics/alert-trends       # Alert trends over time
GET /api/analytics/top-at-risk        # Top at-risk employees
GET /api/analytics/department-stats   # Department statistics
```

**Full API documentation**: See [backend/README.md](backend/README.md)

---

## 🤖 AI Tools Integration

### RAG (Retrieval Augmented Generation)

- **Status**: ✅ Operational
- **Vector DB**: ChromaDB Cloud
- **LLM**: Claude AI (Anthropic)
- **Purpose**: Context-aware risk analysis with historical case matching

### n8n (Workflow Automation)

- **Status**: ✅ Operational
- **Deployment**: Self-hosted Docker
- **Use Cases**:
  - Daily employee risk scans
  - Automated alert escalation
  - Weekly analytics reports

### MCP (Model Context Protocol)

- **Status**: ✅ Implemented
- **Purpose**: AI assistant integration
- **Features**: Expose HR data as resources and tools

**Details**: See [n8n-workflows/README.md](n8n-workflows/README.md)

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file in `backend/` directory:

```bash
# Database
DATABASE_URL=sqlite:///absconding.db

# AI Services
ANTHROPIC_API_KEY=your-anthropic-key
CHROMA_API_KEY=your-chroma-key
CHROMA_TENANT=your-tenant-id
CHROMA_DATABASE=absconding-detection-system

# Notifications (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
HR_TEAM_EMAILS=hr@company.com,manager@company.com

SLACK_BOT_TOKEN=xoxb-your-token
SLACK_CHANNEL_ID=C0123456789
```

**See**: [backend/ENV_SETUP_GUIDE.md](backend/ENV_SETUP_GUIDE.md) for detailed setup

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Health check
python health_check.py

# Full integration tests
python test_integration.py

# Create demo data
python create_demo_data.py
```

**Expected**: 6/6 health checks pass

### Testing Individual Features

```bash
# Test API endpoint
curl http://localhost:5000/api/employees

# Test risk analysis
curl -X POST http://localhost:5000/api/alerts/analyze/EMP001 \
  -H "Content-Type: application/json" \
  -d '{"communications":[{"text":"Feeling frustrated","source":"email"}]}'

# Test n8n integration
curl http://localhost:5000/api/webhooks/n8n/get-high-risk
```

---

## 📊 System Status

### ✅ Fully Operational Components

- **Backend API** (30+ endpoints)
- **Database Models** (Employee, Alert, Communication)
- **AI Services** (Anomaly Detection, Sentiment Analysis, RAG)
- **Vector Database** (ChromaDB Cloud integration)
- **Notification Services** (Email + Slack)
- **n8n Integration** (Webhook endpoints)
- **Documentation** (Comprehensive guides)

### 🚧 In Development

- **Frontend Dashboard** (Next.js + TypeScript)
- **Production Deployment** (AWS/Azure/GCP)
- **Mobile App** (React Native)

---

## 📈 Performance

### Benchmarks

| Operation      | Response Time | Status |
| -------------- | ------------- | ------ |
| Employee CRUD  | <100ms        | ✅     |
| Risk Analysis  | 1-2s          | ✅     |
| RAG Analysis   | 3-8s          | ✅     |
| Batch (10 emp) | 15-30s        | ✅     |
| Vector Search  | <500ms        | ✅     |

**Accuracy**: 85%+ risk prediction accuracy

---

## 🔒 Security

### Features

- ✅ Environment variable protection
- ✅ CORS configuration
- ✅ Input validation
- ✅ Webhook signature verification
- ✅ SQL injection prevention

### Production Recommendations

- Use strong `SECRET_KEY`
- Enable HTTPS
- Implement JWT authentication
- Add rate limiting
- Regular security audits

---

## 🚀 Deployment

### Development

```bash
python run.py
```

### Production

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

**Recommended Stack**:

- **Server**: Gunicorn + Nginx
- **Database**: PostgreSQL
- **Platform**: AWS/Azure/Google Cloud
- **Monitoring**: Sentry, New Relic

**See**: [backend/README.md](backend/README.md) for detailed deployment guide

---

## 📚 Documentation

| Document                                                 | Description               |
| -------------------------------------------------------- | ------------------------- |
| [backend/README.md](backend/README.md)                   | Backend API documentation |
| [frontend/README.md](frontend/README.md)                 | Frontend setup guide      |
| [n8n-workflows/README.md](n8n-workflows/README.md)       | Workflow automation guide |
| [backend/ENV_SETUP_GUIDE.md](backend/ENV_SETUP_GUIDE.md) | Environment configuration |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎓 Acknowledgments

- **Anthropic** - Claude AI for intelligent analysis
- **ChromaDB** - Vector database for semantic search
- **HuggingFace** - Transformers for NLP
- **n8n** - Workflow automation platform
- **Flask** - Python web framework

---

## 📧 Contact

**Developer**: Biraj Singha  
**Email**: biraj.singha@intglobal.com  
**Repository**: [github.com/BirajSingha/absconding-detection-system](https://github.com/BirajSingha/absconding-detection-system)

---

## 🎯 Roadmap

### Phase 1: Core Functionality ✅

- [x] Backend API development
- [x] Anomaly detection
- [x] Sentiment analysis
- [x] RAG integration
- [x] Email notifications

### Phase 2: Enhanced Features 🚧

- [ ] Frontend dashboard
- [ ] Real-time streaming
- [ ] Advanced ML models
- [ ] Mobile application

### Phase 3: Enterprise Features 📋

- [ ] Multi-tenant support
- [ ] SSO integration
- [ ] Advanced analytics
- [ ] Custom reporting

---

## 💡 Use Cases

1. **HR Departments** - Proactive employee retention
2. **Team Managers** - Early warning for team attrition
3. **C-Suite** - Organization-wide retention insights
4. **Consultants** - Client retention analysis

---

## ⚡ Quick Links

- [Backend Documentation](backend/README.md)
- [Frontend Documentation](frontend/README.md)
- [n8n Workflows](n8n-workflows/README.md)
- [API Reference](backend/README.md#api-endpoints)
- [Environment Setup](backend/ENV_SETUP_GUIDE.md)

---

<div align="center">

**Built with ❤️ for smarter HR analytics**

⭐ Star this repo if you find it helpful!

</div>
