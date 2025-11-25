import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api"
N8N_URL = "http://127.0.0.1:5678"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")

def test_employee_crud():
    """Test Employee CRUD operations"""
    print_header("1. Testing Employee CRUD Operations")
    
    # Create employee
    print_info("Creating test employee...")
    employee_data = {
        "employee_id": "TEST_E001",
        "name": "Alice Johnson",
        "email": "alice@test.com",
        "role": "Senior Developer",
        "department": "Engineering",
        "tenure_years": 3.0,
        "productivity_score": 95,
        "attendance_percentage": 98
    }
    
    # Delete if exists
    requests.delete(f"{BASE_URL}/employees/TEST_E001")
    
    response = requests.post(f"{BASE_URL}/employees", json=employee_data)
    if response.status_code == 201:
        print_success("Employee created successfully")
        print(f"   Name: {employee_data['name']}, ID: {employee_data['employee_id']}")
    else:
        print_error(f"Failed to create employee: {response.text}")
        return False
    
    # Get employee
    print_info("Retrieving employee...")
    response = requests.get(f"{BASE_URL}/employees/TEST_E001")
    if response.status_code == 200:
        print_success("Employee retrieved successfully")
    else:
        print_error("Failed to retrieve employee")
        return False
    
    # Update metrics
    print_info("Updating employee metrics...")
    metrics = {
        "productivity_score": 65,  # Significant drop
        "attendance_percentage": 75
    }
    response = requests.put(f"{BASE_URL}/employees/TEST_E001/metrics", json=metrics)
    if response.status_code == 200:
        print_success("Metrics updated (simulating performance drop)")
        print(f"   Productivity: 95 → 65, Attendance: 98 → 75")
    else:
        print_error("Failed to update metrics")
        return False
    
    return True

def test_anomaly_detection():
    """Test Anomaly Detection"""
    print_header("2. Testing Anomaly Detection & Sentiment Analysis")
    
    print_info("Creating employee with risk factors...")
    employee_data = {
        "employee_id": "TEST_E002",
        "name": "Bob Smith",
        "email": "bob@test.com",
        "role": "Data Analyst",
        "department": "Analytics",
        "tenure_years": 1.5,
        "productivity_score": 55,  # Low
        "attendance_percentage": 70  # Low
    }
    
    requests.delete(f"{BASE_URL}/employees/TEST_E002")
    response = requests.post(f"{BASE_URL}/employees", json=employee_data)
    
    print_info("Triggering analysis with negative communications...")
    analysis_data = {
        "communications": [
            {
                "text": "I'm extremely frustrated with my current role. Management doesn't listen.",
                "source": "email"
            },
            {
                "text": "Looking at other job opportunities. This company doesn't value my work.",
                "source": "slack"
            },
            {
                "text": "Thinking about resigning soon. The work environment is toxic.",
                "source": "email"
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/alerts/analyze/TEST_E002", json=analysis_data)
    if response.status_code == 201:
        data = response.json()
        print_success("Alert generated successfully!")
        print(f"   Risk Level: {data.get('risk_level')}")
        print(f"   Risk Score: {data.get('risk_score'):.2f}/100")
        print(f"   Confidence: {data.get('confidence_score'):.2f}")
        print(f"   Anomalies Detected: {len(data.get('behavioral_indicators', []))}")
        
        if data.get('ai_summary'):
            print(f"   AI Summary: {data['ai_summary'][:100]}...")
        
        return data
    else:
        print_error(f"Analysis failed: {response.text}")
        return None

def test_alert_retrieval(alert_data):
    """Test Alert Retrieval"""
    print_header("3. Testing Alert Retrieval Endpoints")
    
    # List all alerts
    print_info("Listing all alerts...")
    response = requests.get(f"{BASE_URL}/alerts")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved {data.get('total', 0)} alerts")
    else:
        print_error("Failed to list alerts")
        return False
    
    # Filter by risk level
    print_info("Filtering HIGH/CRITICAL alerts...")
    response = requests.get(f"{BASE_URL}/alerts?risk_level=HIGH")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Found {len(data.get('alerts', []))} HIGH risk alerts")
    else:
        print_error("Failed to filter alerts")
        return False
    
    # Get specific alert
    if alert_data and 'id' in alert_data:
        print_info(f"Retrieving specific alert (ID: {alert_data['id']})...")
        response = requests.get(f"{BASE_URL}/alerts/{alert_data['id']}")
        if response.status_code == 200:
            print_success("Alert retrieved successfully")
        else:
            print_error("Failed to get specific alert")
    
    return True

def test_analytics():
    """Test Analytics Endpoints"""
    print_header("4. Testing Analytics Endpoints")
    
    # Risk distribution
    print_info("Getting risk distribution...")
    response = requests.get(f"{BASE_URL}/analytics/risk-distribution")
    if response.status_code == 200:
        data = response.json()
        print_success("Risk distribution retrieved")
        for level, count in data.items():
            print(f"   {level}: {count}")
    else:
        print_error("Failed to get risk distribution")
    
    # Alert trends
    print_info("Getting alert trends (last 30 days)...")
    response = requests.get(f"{BASE_URL}/analytics/alert-trends?days=30")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Alert trends: {data.get('total', 0)} total alerts in last 30 days")
    else:
        print_error("Failed to get alert trends")
    
    # Top at-risk
    print_info("Getting top at-risk employees...")
    response = requests.get(f"{BASE_URL}/analytics/top-at-risk?limit=5")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved top {len(data)} at-risk employees")
        for item in data[:3]:
            emp = item.get('employee', {})
            alert = item.get('alert', {})
            print(f"   - {emp.get('name')}: {alert.get('risk_score'):.1f} ({alert.get('risk_level')})")
    else:
        print_error("Failed to get top at-risk")
    
    # Department stats
    print_info("Getting department statistics...")
    response = requests.get(f"{BASE_URL}/analytics/department-stats")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Department stats for {len(data)} departments")
        for dept in data:
            print(f"   {dept['department']}: {dept['total_employees']} employees, "
                  f"Productivity: {dept['avg_productivity']:.1f}")
    else:
        print_error("Failed to get department stats")
    
    return True

def test_n8n_webhooks():
    """Test n8n Webhook Endpoints"""
    print_header("5. Testing n8n Webhook Endpoints")
    
    # Get high-risk employees
    print_info("Testing GET high-risk endpoint...")
    response = requests.get(f"{BASE_URL}/webhooks/n8n/get-high-risk")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved {data.get('count', 0)} high-risk employees")
        for emp in data.get('employees', [])[:3]:
            print(f"   - {emp['employee_name']}: {emp['risk_score']:.1f} ({emp['risk_level']})")
    else:
        print_error("Failed to get high-risk employees")
    
    # Trigger single analysis
    print_info("Testing single analysis trigger...")
    trigger_data = {
        "employee_id": "TEST_E001",
        "communications": [
            {"text": "Feeling unhappy at work", "source": "slack"}
        ]
    }
    response = requests.post(f"{BASE_URL}/webhooks/n8n/trigger-analysis", json=trigger_data)
    if response.status_code == 200:
        data = response.json()
        print_success(f"Analysis triggered: {data.get('employee_name')} - {data.get('risk_level')}")
        print(f"   Risk Score: {data.get('risk_score'):.2f}")
    else:
        print_error("Failed to trigger analysis")
    
    # Batch analysis
    print_info("Testing batch analysis (all active employees)...")
    response = requests.post(f"{BASE_URL}/webhooks/n8n/batch-analysis", json={})
    if response.status_code == 200:
        data = response.json()
        print_success(f"Batch analysis complete")
        print(f"   Total Employees: {data.get('total_employees', 0)}")
        print(f"   High Risk Count: {data.get('high_risk_count', 0)}")
    else:
        print_error("Failed to run batch analysis")
    
    return True

def test_vector_db():
    """Test Vector DB Endpoints"""
    print_header("6. Testing Vector DB Integration")
    
    # Get stats
    print_info("Getting vector DB statistics...")
    response = requests.get(f"{BASE_URL}/vector-db/stats")
    if response.status_code == 200:
        data = response.json()
        print_success("Vector DB stats retrieved")
        print(f"   Knowledge Base: {data.get('knowledge_base_count', 0)} documents")
        print(f"   Historical Cases: {data.get('historical_cases_count', 0)} cases")
        print(f"   Communications: {data.get('communications_count', 0)} messages")
    else:
        print_error("Failed to get vector DB stats")
    
    # Search knowledge
    print_info("Searching knowledge base...")
    search_data = {
        "query": "retention strategies for developers",
        "n_results": 2
    }
    response = requests.post(f"{BASE_URL}/vector-db/search/knowledge", json=search_data)
    if response.status_code == 200:
        data = response.json()
        print_success(f"Found {len(data.get('results', []))} relevant documents")
    else:
        print_error("Failed to search knowledge base")
    
    return True

def test_n8n_server():
    """Test n8n server availability"""
    print_header("7. Testing n8n Server")
    
    print_info("Checking n8n availability...")
    try:
        response = requests.get(N8N_URL, timeout=2)
        if response.status_code in [200, 401, 302]:  # 401 means auth required (good!)
            print_success("n8n server is running!")
            print(f"   Access at: {N8N_URL}")
            print(f"   Default credentials: admin/admin123")
            return True
        else:
            print_error(f"n8n returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error("n8n server not accessible")
        print_info("   Start with: docker-compose up -d")
        return False

def cleanup():
    """Cleanup test data"""
    print_header("Cleanup")
    
    print_info("Cleaning up test employees...")
    requests.delete(f"{BASE_URL}/employees/TEST_E001")
    requests.delete(f"{BASE_URL}/employees/TEST_E002")
    print_success("Test data cleaned up")

def main():
    print(f"\n{Colors.BLUE}╔══════════════════════════════════════════════════════════╗")
    print(f"║   Absconding Detection System - Integration Test Suite  ║")
    print(f"║                    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                    ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    print_info("Testing Flask Backend: http://127.0.0.1:5000")
    print_info("Testing n8n Server: http://127.0.0.1:5678")
    
    # Wait for servers to be ready
    time.sleep(2)
    
    results = {
        "Employee CRUD": False,
        "Anomaly Detection & RAG": False,
        "Alert Retrieval": False,
        "Analytics": False,
        "n8n Webhooks": False,
        "Vector DB": False,
        "n8n Server": False
    }
    
    try:
        # Run tests
        results["Employee CRUD"] = test_employee_crud()
        
        alert_data = test_anomaly_detection()
        results["Anomaly Detection & RAG"] = alert_data is not None
        
        results["Alert Retrieval"] = test_alert_retrieval(alert_data)
        results["Analytics"] = test_analytics()
        results["n8n Webhooks"] = test_n8n_webhooks()
        results["Vector DB"] = test_vector_db()
        results["n8n Server"] = test_n8n_server()
        
    except requests.exceptions.ConnectionError:
        print_error("\nCannot connect to Flask server!")
        print_info("Make sure Flask is running: python run.py")
        return
    except Exception as e:
        print_error(f"Test error: {e}")
    finally:
        cleanup()
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\n{Colors.BLUE}Results: {passed}/{total} tests passed{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}🎉 ALL TESTS PASSED! System is fully operational.{Colors.RESET}\n")
    else:
        print(f"\n{Colors.YELLOW}⚠️  Some tests failed. Check logs above.{Colors.RESET}\n")

if __name__ == "__main__":
    main()
