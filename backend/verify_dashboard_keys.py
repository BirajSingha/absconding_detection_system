
import requests
import sys

def verify_dashboard_api():
    url = "http://localhost:5000/api/analytics/alert-summary"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"FAILED: Status {response.status_code}")
            return False
            
        data = response.json()
        print("Received Data Keys:", data.keys())
        
        required_keys = [
            'total_candidates', 
            'total_interviews', 
            'pending_interviews', 
            'completed_interviews', 
            'average_fit_score'
        ]
        
        missing = [k for k in required_keys if k not in data]
        if missing:
            print(f"FAILED: Missing keys: {missing}")
            return False
            
        print("SUCCESS: All keys match frontend expectations.")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if verify_dashboard_api():
        sys.exit(0)
    else:
        sys.exit(1)
