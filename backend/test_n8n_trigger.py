
import requests
import json

def test_n8n():
    urls = [
        ("Production", "http://localhost:5678/webhook/hr-alert"),
        ("Test", "http://localhost:5678/webhook-test/hr-alert")
    ]
    
    payload = {
        "candidate_id": "TEST_001",
        "candidate_name": "Test User",
        "risk_level": "HIGH",
        "summary": "This is a test alert triggered by the system."
    }
    
    for mode, url in urls:
        try:
            print(f"[{mode}] Sending POST to {url}...")
            response = requests.post(url, json=payload, timeout=5)
            print(f"[{mode}] Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ {mode} Webhook Triggered Successfully!")
                print(f"response: {response.text}")
                return # Stop after success
            elif response.status_code == 404:
                print(f"❌ {mode} Webhook Not Found.")
            else:
                print(f"⚠️ {mode} Unexpected Status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {mode} Connection Failed: {e}")
            
    print("\nTroubleshooting:")
    print("1. If 'Test' failed: Click 'Execute Workflow' in n8n UI first.")
    print("2. If 'Production' failed: Toggle 'Active' switch to ON in n8n UI.")

if __name__ == "__main__":
    test_n8n()
