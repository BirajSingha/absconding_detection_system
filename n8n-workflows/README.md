# n8n Workflow Examples for Absconding Detection System

This directory contains example n8n workflow templates that can be imported into your n8n instance.

## Setup Instructions

1. **Start n8n**:

   ```bash
   cd /path/to/absconding-detection-system
   docker-compose up -d
   ```

2. **Access n8n**:

   - Open http://localhost:5678
   - Login with credentials (admin/admin123)

3. **Import Workflows**:
   - Click "Import from File"
   - Select one of the JSON files from this directory

## Available Workflows

### 1. Daily Employee Risk Scan (`daily-risk-scan.json`)

**Purpose**: Automatically analyze all active employees daily and alert on high-risk cases.

**Triggers**: Every day at 9 AM
**Actions**:

- Calls `/api/webhooks/n8n/batch-analysis`
- Filters employees with HIGH/CRITICAL risk
- Sends Slack notification for each high-risk employee
- Creates summary report

**Setup**:

- Configure Slack credentials in n8n
- Set Flask API URL (http://host.docker.internal:5000)

### 2. Alert Escalation Workflow (`alert-escalation.json`)

**Purpose**: Automatically escalate high-risk alerts through multiple channels.

**Triggers**: Webhook from Flask when HIGH/CRITICAL alert created
**Actions**:

- Send immediate Slack notification
- Send email to HR team
- Create ticket in helpdesk system (optional)
- Schedule follow-up reminder after 24 hours

**Setup**:

- Configure webhook URL in Flask Slack service
- Set up email credentials in n8n
- Optional: Configure helpdesk API

### 3. Weekly Analytics Report (`weekly-analytics.json`)

**Purpose**: Generate and send weekly HR analytics report.

**Triggers**: Every Monday at 8 AM
**Actions**:

- Fetch analytics from `/api/analytics/*` endpoints
- Generate formatted report
- Send PDF via email to management
- Store in Google Drive (optional)

**Setup**:

- Configure email settings
- Optional: Set up Google Drive integration

## Creating Custom Workflows

### Connecting to Flask API

In n8n HTTP Request nodes, use:

- **URL**: `http://host.docker.internal:5000/api/...`
- **Method**: GET/POST as needed
- **Headers**: `Content-Type: application/json`

### Available Webhook Endpoints

```
POST /api/webhooks/n8n/trigger-analysis
POST /api/webhooks/n8n/batch-analysis
GET  /api/webhooks/n8n/get-high-risk
POST /api/webhooks/n8n/alert-created
```

### Example: Simple Analysis Trigger

```json
{
  "nodes": [
    {
      "type": "n8n-nodes-base.httpRequest",
      "name": "Analyze Employee",
      "parameters": {
        "url": "http://host.docker.internal:5000/api/webhooks/n8n/trigger-analysis",
        "method": "POST",
        "bodyParameters": {
          "employee_id": "={{ $json.employee_id }}"
        }
      }
    }
  ]
}
```

## Tips

- Use **Schedule Trigger** for periodic scans
- Use **Webhook Trigger** for event-driven workflows
- Use **IF** nodes to route based on risk level
- Use **Set** nodes to transform data between services
- Test workflows with small batches first

## Troubleshooting

**Can't connect to Flask API**:

- Ensure Flask is running on port 5000
- Use `host.docker.internal` instead of `localhost`
- Check Docker network settings

**Webhook not triggering**:

- Verify webhook URL in n8n matches Flask config
- Check n8n logs: `docker logs absconding-n8n`

## Security

> [!WARNING] > **Production Deployment**:
>
> - Change default n8n credentials
> - Use environment variables for API keys
> - Enable HTTPS for webhooks
> - Implement webhook signature verification
