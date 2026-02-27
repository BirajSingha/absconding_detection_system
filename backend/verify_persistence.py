import requests
import json

candidate_id = "TEST_CANDIDATE_002"
url = f"http://127.0.0.1:5000/api/analysis/candidate/{candidate_id}"

try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            latest = data[0]
            traits = latest.get('behavioral_traits', {})
            print("Behavioral Traits keys:", traits.keys())
            
            if 'absconding_risk' in traits:
                print("SUCCESS: absconding_risk found in behavioral_traits")
                print(json.dumps(traits['absconding_risk'], indent=2))
            else:
                print("FAILURE: absconding_risk NOT found")
        else:
            print("No analysis found for candidate")
    else:
        print(f"Error: {response.status_code}")
except Exception as e:
    print(f"Request failed: {e}")
