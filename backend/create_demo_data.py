import requests
import json

BASE_URL = "http://localhost:5000/api"

print("Creating high-risk demo employee...")

# Create employee with poor metrics
employee_data = {
    "employee_id": "DEMO001",
    "name": "Demo High-Risk Employee",
    "email": "demo@test.com",
    "role": "Senior Developer",
    "department": "Engineering",
    "productivity_score": 50,  # Low
    "attendance_percentage": 65,  # Low
    "performance_rating": 2.0  # Low
}

response = requests.post(f"{BASE_URL}/employees", json=employee_data)
if response.status_code == 201:
    print(f"✓ Employee created: {employee_data['name']}")
else:
    print(f"Employee might already exist or other issue: {response.status_code}")

# Trigger analysis with negative communications
print("\nTriggering risk analysis...")
analysis_data = {
    "communications": [
        {
            "text": "I'm really frustrated with this job. Looking for other opportunities and thinking about quitting.",
            "source": "email"
        },
        {
            "text": "Management doesn't value my work. This place is becoming toxic. I deserve better.",
            "source": "slack"
        }
    ]
}

response = requests.post(f"{BASE_URL}/alerts/analyze/DEMO001", json=analysis_data)
if response.status_code == 201:
    alert = response.json()
    print(f"✓ Alert generated!")
    print(f"  Risk Level: {alert['risk_level']}")
    print(f"  Risk Score: {alert['risk_score']}")
    print(f"  Confidence: {alert['confidence_score']}")
else:
    print(f"Analysis failed: {response.status_code}")
    print(response.text)

# Verify high-risk endpoint
print("\nVerifying high-risk endpoint...")
response = requests.get(f"{BASE_URL}/webhooks/n8n/get-high-risk")
if response.status_code == 200:
    data = response.json()
    print(f"✓ High-risk employees: {data['count']}")
    if data['count'] > 0:
        for emp in data['employees']:
            print(f"  - {emp['employee_name']}: {emp['risk_score']} ({emp['risk_level']})")
    print("\n🎉 Now test your n8n workflow again - you should see data!")
else:
    print("Failed to check high-risk endpoint")
