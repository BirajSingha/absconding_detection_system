import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def test_create_candidate():
    print("Testing create candidate...")
    data = {
        "candidate_id": "C_TEST_001",
        "name": "John Doe",
        "email": "john@example.com",
        "position_applied": "Software Engineer",
        "department": "Engineering"
    }
    try:
        res = requests.post(f"{BASE_URL}/candidates/", json=data)
        if res.status_code == 201:
            print("✓ Candidate created")
            return True
        else:
            print(f"✗ Failed (Status {res.status_code}): {res.text}")
            # If failing because exists, that's okay for retries
            if "already exists" in res.text:
                print("  (Candidate already exists, proceeding)")
                return True
            return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False

def test_analyze_interview():
    print("\nTesting interview analysis...")
    data = {
        "candidate_id": "C_TEST_001",
        "transcript_text": "I am very confident in my leadership abilities. I have led teams of 10 people and we delivered projects on time. I believe teamwork is essential."
    }
    try:
        res = requests.post(f"{BASE_URL}/analysis/analyze-interview", json=data)
        if res.status_code == 201:
            print("✓ Analysis created")
            data = res.json()
            print(f"  Score: {data['fit_score']}, Category: {data['fit_category']}")
            return True
        else:
            print(f"✗ Failed: {res.text}")
            return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False

def test_dashboard_stats():
    print("\nTesting dashboard stats...")
    try:
        res = requests.get(f"{BASE_URL}/analytics/dashboard")
        if res.status_code == 200:
            print("✓ Dashboard stats retrieved")
            data = res.json()
            print(f"  Top Risks Count: {len(data.get('top_risk_employees', []))}")
            return True
        else:
            print(f"✗ Failed: {res.text}")
            return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False

if __name__ == "__main__":
    if test_create_candidate() and test_analyze_interview() and test_dashboard_stats():
        print("\nAll Backend Tests Passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed.")
        sys.exit(1)
