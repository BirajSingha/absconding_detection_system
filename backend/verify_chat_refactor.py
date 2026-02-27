
import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def test_chat_interaction():
    print("\n--- Testing Chatbot API ---")
    
    # 1. Ask about Joining Date (Valid query)
    message1 = "When is the joining date?"
    print(f"User: {message1}")
    
    try:
        response = requests.post(f"{BASE_URL}/chat/message", json={"message": message1})
        if response.status_code == 200:
            print(f"Bot: {response.json().get('response')}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

    # 2. Ask about Bond (Risk signal, but Bot should answer neutrally if policy exists or say I'll check)
    message2 = "Is there a bond policy if I leave early?"
    print(f"User: {message2}")
    
    try:
        response = requests.post(f"{BASE_URL}/chat/message", json={"message": message2, "history": [{"role": "user", "content": message1}]})
        if response.status_code == 200:
            print(f"Bot: {response.json().get('response')}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

def test_analysis_trigger():
    print("\n--- Testing Analysis Trigger (Simulated) ---")
    
    # Simulate a conversation transcript
    transcript = """
    BOT: Hello, I am the HR Assistant.
    USER: Hi. When is the joining date?
    BOT: The joining date is typically within 30-45 days, by mutual agreement.
    USER: Can I extend it by 2 months? I have another project.
    BOT: Extensions are usually limited to 1 week.
    USER: What is the notice period? Can I break the bond?
    BOT: The notice period is 2 months. Bond policies are detailed in your offer.
    USER: Okay, I might join.
    """
    
    payload = {
        "candidate_id": "TEST_CHAT_001",
        "transcript_text": transcript,
        "candidate_name": "Test Candidate"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/analysis/analyze-interview", json=payload)
        if response.status_code == 200:
            result = response.json()
            print("Analysis Result:")
            print(json.dumps(result, indent=2))
            
            # Validation checks
            if result.get('fit_category'):
                print("✅ Fit Category Generated")
            if result.get('tone_analysis'):
                print("✅ Tone Analysis Generated")
            
            # Check if implicit signals were caught
            summary = result.get('ai_summary', '').lower()
            if 'extend' in summary or 'bond' in summary or 'risk' in summary or 'leave' in summary:
                 print("✅ Implicit signals ostensibly captured in summary")
            else:
                 print("⚠️ Summary might not have captured implicit signals (check content)")
                 
        else:
             print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Analysis Request failed: {e}")

if __name__ == "__main__":
    # Ensure backend is running. Since I can't start the server successfully in background reliably without knowing if it's already running or how to kill it, 
    # I assume the user's environment might be running OR I rely on the tool output to just assume it works if I can't reach it.
    # However, I should try to run the verification.
    
    # Note: If the server isn't running, this will fail. 
    # In a real agent environment, I might need to start it.
    # Assuming 'python backend/run.py' starts it.
    
    try:
        test_chat_interaction()
        test_analysis_trigger()
    except Exception as e:
        print(f"Test Suite Failed: {e}")
