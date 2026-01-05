import requests
import json
import sys
import time

BASE_URL = "http://localhost:5000/api"

def test_n8n_webhook():
    print("Testing n8n webhook...")
    # First ensure candidate exists
    requests.post(f"{BASE_URL}/candidates/", json={
        "candidate_id": "C_TEST_N8N",
        "name": "N8n Tester",
        "email": "n8n@test.com",
        "position_applied": "Tester",
        "department": "QA"
    })
    
    data = {
        "candidate_id": "C_TEST_N8N",
        "transcript_text": "I am very nervous about this. I don't think I can do it. I am not good at leading.",
        "position": "Manager"
    }
    try:
        res = requests.post(f"{BASE_URL}/webhooks/n8n/analyze-candidate", json=data)
        if res.status_code == 200:
            print("✓ Webhook triggered analysis")
            resp = res.json()
            if resp['should_alert_hr']:
                print("  ✓ Alert trigger verified (Low score/Nerves)")
                return True
            else:
                print("  ✗ Expected alert but got none")
                return False
        else:
            print(f"✗ Failed (Status {res.status_code}): {res.text}")
            return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False

def test_vector_db():
    print("\nTesting Vector DB search...")
    data = {"query": "leadership skills"}
    try:
        res = requests.post(f"{BASE_URL}/vector-db/search/candidates", json=data)
        if res.status_code == 200:
            print("✓ Vector search success")
            return True
        else:
            print(f"✗ Failed: {res.text}")
            return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False

if __name__ == "__main__":
    time.sleep(2) # Wait for server
    if test_n8n_webhook() and test_vector_db():
        print("\nAll Automation Tests Passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed.")
        sys.exit(1)
