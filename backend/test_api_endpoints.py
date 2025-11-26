import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def print_result(name, success, details=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {name}")
    if details:
        print(f"   {details}")

def test_api():
    print("🚀 Starting API Verification...")
    
    # 1. Test Health/Root (if exists) or just check connection
    try:
        requests.get("http://localhost:5000/")
        print_result("Backend Connection", True)
    except Exception as e:
        print_result("Backend Connection", False, str(e))
        return

    # 2. Test Employees API
    try:
        res = requests.get(f"{BASE_URL}/employees")
        success = res.status_code == 200 and 'employees' in res.json()
        print_result("GET /employees", success, f"Count: {len(res.json().get('employees', []))}")
    except Exception as e:
        print_result("GET /employees", False, str(e))

    # 3. Test Alerts API
    try:
        res = requests.get(f"{BASE_URL}/alerts")
        success = res.status_code == 200 and 'alerts' in res.json()
        print_result("GET /alerts", success, f"Count: {len(res.json().get('alerts', []))}")
        
        alerts = res.json().get('alerts', [])
        alert_id = alerts[0]['id'] if alerts else None
    except Exception as e:
        print_result("GET /alerts", False, str(e))
        alert_id = None

    # 4. Test Analytics Dashboard (NEW)
    try:
        res = requests.get(f"{BASE_URL}/analytics/dashboard")
        data = res.json()
        success = res.status_code == 200 and 'risk_distribution' in data
        print_result("GET /analytics/dashboard", success)
        if success:
            print(f"   Risk Dist: {len(data.get('risk_distribution', []))} items")
            print(f"   Recent Alerts: {len(data.get('recent_alerts', []))} items")
    except Exception as e:
        print_result("GET /analytics/dashboard", False, str(e))

    # 5. Test Update Alert Status (NEW)
    if alert_id:
        try:
            # First set to ACKNOWLEDGED
            res = requests.put(f"{BASE_URL}/alerts/{alert_id}/status", json={'status': 'ACKNOWLEDGED'})
            success1 = res.status_code == 200 and res.json().get('status') == 'ACKNOWLEDGED'
            print_result(f"PUT /alerts/{alert_id}/status (ACKNOWLEDGED)", success1)
            
            # Revert to OPEN (if possible/needed, or just leave it)
            # requests.put(f"{BASE_URL}/alerts/{alert_id}/status", json={'status': 'OPEN'})
        except Exception as e:
            print_result("PUT /alerts/status", False, str(e))
    else:
        print("⚠️ Skipping Update Alert Test (No alerts found)")

    # 6. Test Risk Distribution
    try:
        res = requests.get(f"{BASE_URL}/analytics/risk-distribution")
        success = res.status_code == 200
        print_result("GET /analytics/risk-distribution", success, str(res.json()) if success else "")
    except Exception as e:
        print_result("GET /analytics/risk-distribution", False, str(e))

if __name__ == "__main__":
    # Wait a bit for server to be fully ready if just started
    time.sleep(2)
    test_api()
