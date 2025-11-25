# n8n Workflows for Absconding Detection System

Complete guide to workflow automation using n8n for the Absconding Detection System.

---

## 🚀 Quick Start

### 1. Start n8n

```bash
# From project root
docker compose up -d
```

**Access n8n**: http://localhost:5678

**Login Credentials**:

- Email: `biraj.singha@intglobal.com`
- Password: `Biraj.INT@123`

### 2. Test Connection

**Quick Test Workflow**:

1. In n8n, click **"New workflow"**
2. Add **HTTP Request** node
3. Configure:
   - Method: **GET**
   - URL: `http://host.docker.internal:5000/api/webhooks/n8n/get-high-risk`
4. Click **"Test step"**
5. See results! 🎉

---

## 📋 Available n8n Webhook Endpoints

All endpoints connect to your Flask backend running on port 5000.

### 1. Get High-Risk Employees

```
GET http://host.docker.internal:5000/api/webhooks/n8n/get-high-risk
```

**Returns**: List of current HIGH/CRITICAL risk employees

**Response**:

```json
{
  "count": 1,
  "employees": [
    {
      "alert_id": 1,
      "employee_id": "DEMO001",
      "employee_name": "Demo High-Risk Employee",
      "department": "Engineering",
      "risk_score": 80.0,
      "risk_level": "CRITICAL",
      "created_at": "2025-11-25T..."
    }
  ]
}
```

**Use Case**: Real-time monitoring dashboard, Slack alerts

---

### 2. Trigger Single Employee Analysis

```
POST http://host.docker.internal:5000/api/webhooks/n8n/trigger-analysis
```

**Request Body**:

```json
{
  "employee_id": "EMP001",
  "communications": [
    {
      "text": "Feeling unhappy at work",
      "source": "slack"
    }
  ]
}
```

**Response**:

```json
{
  "employee_id": "EMP001",
  "employee_name": "John Doe",
  "risk_score": 65.28,
  "risk_level": "HIGH",
  "anomalies": [...],
  "sentiment": {...},
  "should_alert": true
}
```

**Use Case**: On-demand analysis, manager-triggered checks

---

### 3. Batch Analysis (All Employees)

```
POST http://host.docker.internal:5000/api/webhooks/n8n/batch-analysis
```

**Request Body**: `{}` (empty)

**Response**:

```json
{
  "total_employees": 20,
  "high_risk_count": 3,
  "employees": [
    {
      "employee_id": "E001",
      "name": "John Doe",
      "department": "Engineering",
      "risk_score": 75.5,
      "risk_level": "HIGH",
      "anomaly_count": 2
    }
  ]
}
```

**Use Case**: Daily scans, weekly reports

---

### 4. Alert Created Notification

```
POST http://host.docker.internal:5000/api/webhooks/n8n/alert-created
```

**Request Body**: Alert data (sent from Flask)

**Use Case**: Workflow completion tracking

---

## 🎯 Pre-Built Workflow Examples

### Workflow 1: Daily Employee Risk Scan

**Purpose**: Automatically analyze all employees daily and notify on high-risk cases

**Schedule**: Every day at 9:00 AM

**Workflow Steps**:

```
┌─────────────────────┐
│  Schedule Trigger   │
│   (Daily 9 AM)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   HTTP Request      │
│  batch-analysis     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     IF Node         │
│ high_risk_count > 0 │
└──────────┬──────────┘
           │
      Yes  │  No (end)
           ▼
┌─────────────────────┐
│    Code Node        │
│ Format for Slack    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Slack Node        │
│  Send Alert         │
└─────────────────────┘
```

**n8n Configuration**:

1. **Schedule Trigger**

   - Trigger: Cron
   - Expression: `0 9 * * *` (9 AM daily)

2. **HTTP Request (Batch Analysis)**

   - Method: POST
   - URL: `http://host.docker.internal:5000/api/webhooks/n8n/batch-analysis`
   - Body: `{}`

3. **IF Node**

   - Condition: `{{ $json.high_risk_count }} > 0`

4. **Code Node** (JavaScript)

   ```javascript
   const employees = $input.first().json.employees || [];
   const highRisk = employees.filter(
     (e) => e.risk_level === "HIGH" || e.risk_level === "CRITICAL"
   );

   return [
     {
       json: {
         message:
           `🚨 Daily Risk Scan Alert\n\nFound ${highRisk.length} high-risk employees:\n\n` +
           highRisk
             .map(
               (emp) =>
                 `• ${emp.name} (${emp.department}): ${emp.risk_score.toFixed(
                   1
                 )} - ${emp.risk_level}`
             )
             .join("\n"),
       },
     },
   ];
   ```

5. **Slack Node** (or Email)
   - Message: `{{ $json.message }}`

---

### Workflow 2: Real-Time Alert Escalation

**Purpose**: Automatically escalate HIGH/CRITICAL alerts through multiple channels

**Trigger**: Webhook from Flask when alert created

**Workflow Steps**:

```
┌─────────────────────┐
│  Webhook Trigger    │
│  (from Flask)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     IF Node         │
│ risk_level >= HIGH  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Slack Node        │
│ Immediate Alert     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Email Node        │
│  Notify HR Team     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   HTTP Request      │
│ Create Ticket       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Wait 24h Node     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Slack Node        │
│  Follow-up Reminder │
└─────────────────────┘
```

---

### Workflow 3: Weekly Analytics Report

**Purpose**: Generate and send weekly HR analytics

**Schedule**: Every Monday at 8:00 AM

**Workflow Steps**:

```
┌─────────────────────┐
│  Schedule Trigger   │
│  (Monday 8 AM)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  HTTP Request       │
│  risk-distribution  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  HTTP Request       │
│  department-stats   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Code Node         │
│  Format Report      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Email Node        │
│  Send to Management │
└─────────────────────┘
```

---

## 🛠️ Creating Custom Workflows

### Step-by-Step Guide

#### 1. Plan Your Workflow

- What should trigger it? (Schedule, webhook, manual)
- What data do you need? (Which API endpoints)
- What actions to take? (Slack, email, tickets)

#### 2. Add Nodes

**Common Node Types**:

- **Schedule Trigger** - Run at specific times
- **Webhook Trigger** - Listen for events
- **HTTP Request** - Call Flask API
- **IF** - Conditional logic
- **Code** - JavaScript for data transformation
- **Slack/Email** - Notifications
- **Wait** - Delays between actions

#### 3. Connect to Flask API

**Critical**: Always use `host.docker.internal:5000` NOT `localhost:5000`

**Available Endpoints**:

```
http://host.docker.internal:5000/api/webhooks/n8n/get-high-risk
http://host.docker.internal:5000/api/webhooks/n8n/trigger-analysis
http://host.docker.internal:5000/api/webhooks/n8n/batch-analysis
http://host.docker.internal:5000/api/analytics/risk-distribution
http://host.docker.internal:5000/api/analytics/department-stats
http://host.docker.internal:5000/api/analytics/top-at-risk
```

#### 4. Test Workflow

1. Click **"Execute Workflow"** (top right)
2. Watch nodes execute
3. Check output panel
4. Fix any errors

#### 5. Activate

1. Toggle **"Active"** switch (top right)
2. Workflow runs automatically

---

## 📊 Example: Data Transformation with Code Node

Transform batch analysis data into Slack-friendly format:

```javascript
// Input: { employees: [...], total_employees: 20, high_risk_count: 3 }

const data = $input.first().json;
const highRisk = data.employees.filter(
  (e) => e.risk_level === "HIGH" || e.risk_level === "CRITICAL"
);

// Group by department
const byDept = highRisk.reduce((acc, emp) => {
  if (!acc[emp.department]) acc[emp.department] = [];
  acc[emp.department].push(emp);
  return acc;
}, {});

// Format message
let message = `📊 Daily Risk Scan Results\n\n`;
message += `Total Employees: ${data.total_employees}\n`;
message += `High Risk: ${data.high_risk_count}\n\n`;

for (const [dept, emps] of Object.entries(byDept)) {
  message += `🏢 ${dept}:\n`;
  emps.forEach((emp) => {
    message += `  • ${emp.name}: ${emp.risk_score.toFixed(1)} (${
      emp.risk_level
    })\n`;
  });
  message += `\n`;
}

return [
  {
    json: {
      message: message,
      high_risk_count: data.high_risk_count,
      departments: Object.keys(byDept),
    },
  },
];
```

---

## 🔧 Advanced Features

### Error Handling

Add error handling to workflows:

```javascript
try {
  // Your code here
  const result = processData($input.all());
  return result;
} catch (error) {
  return [
    {
      json: {
        error: error.message,
        timestamp: new Date().toISOString(),
      },
    },
  ];
}
```

### Rate Limiting

Add delays between API calls:

```
HTTP Request → Wait (2s) → HTTP Request
```

### Parallel Processing

Process multiple employees simultaneously:

```
Split In Batches → HTTP Request (Loop) → Merge
```

---

## 🐛 Troubleshooting

### ❌ "Could not connect to Flask API"

**Solutions**:

1. ✅ Use `host.docker.internal:5000` not `localhost:5000`
2. ✅ Verify Flask is running: `curl http://localhost:5000/api/employees`
3. ✅ Check Docker network: `docker network ls`

### ❌ "Node execution failed"

**Solutions**:

1. Click node to see error details
2. Check request/response in output panel
3. Verify URL is correct
4. Test endpoint manually with curl

### ❌ "Workflow not triggering"

**Solutions**:

1. Check "Active" toggle is ON
2. Verify schedule cron expression
3. Check execution history tab
4. Look for errors in n8n logs: `docker logs absconding-n8n`

### ❌ "Empty response from API"

**Expected!** If no high-risk employees exist:

```json
{ "count": 0, "employees": [] }
```

**Solution**: Create demo data:

```bash
cd backend
python create_demo_data.py
```

---

## 📦 Managing n8n Container

### Start/Stop Commands

```bash
# Start n8n
docker compose up -d

# Stop n8n
docker compose down

# Restart n8n
docker compose restart

# View logs
docker logs absconding-n8n

# View real-time logs
docker logs -f absconding-n8n
```

### Data Persistence

Workflows are saved in Docker volume: `absconding-detection-system_n8n_data`

**Backup workflows**:

1. In n8n UI, click workflow
2. Click "..." menu
3. Select "Download"
4. Save JSON file

**Reset n8n** (delete all workflows):

```bash
docker compose down
docker volume rm absconding-detection-system_n8n_data
docker compose up -d
```

---

## 🎓 Learning Resources

- **n8n Documentation**: https://docs.n8n.io
- **Workflow Examples**: https://n8n.io/workflows
- **Community Forum**: https://community.n8n.io

---

## 📝 Best Practices

### Workflow Design

- ✅ Give descriptive names to workflows
- ✅ Add notes to complex nodes
- ✅ Test with small data sets first
- ✅ Use error handling nodes
- ✅ Log important events

### Performance

- ✅ Batch API calls when possible
- ✅ Add delays between requests
- ✅ Use pagination for large datasets
- ✅ Monitor execution times

### Security

- ✅ Store API keys in n8n credentials
- ✅ Use webhook signatures
- ✅ Validate input data
- ✅ Don't log sensitive information

---

## ✅ Verified Working

**Status**: All webhook endpoints tested and operational

**Test Results**:

- ✅ GET high-risk employees: Working
- ✅ POST trigger analysis: Working
- ✅ POST batch analysis: Working
- ✅ n8n ↔ Flask connection: Working

**Test Workflow**: Successfully created and executed simple test workflow connecting to Flask API

---

## 🚀 Next Steps

1. Create your first workflow (follow Quick Start above)
2. Test with demo data (`python create_demo_data.py`)
3. Build daily risk scan workflow
4. Set up Slack notifications
5. Create automated reports

---

**Need Help?**  
Check the main project documentation in `/SETUP.md` or backend `/backend/README.md`

**Happy Automating!** 🎉
