import requests
import json

url = "http://127.0.0.1:5000/api/analysis/analyze-interview"
# Use a new ID to ensure fresh record
candidate_id = "TEST_CANDIDATE_002" 
payload = {
    "candidate_id": candidate_id,
    "candidate_name": "Test User 2",
    "transcript_text": "I am not sure if I want to stay long term. I feel a bit overwhelmed and the commute is long."
}

try:
    print(f"Triggering analysis for {candidate_id}...")
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        print("Analysis created successfully.")
    else:
        print(f"Error: {response.text}")

except Exception as e:
    print(f"Request failed: {e}")
