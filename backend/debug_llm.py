import os
from dotenv import load_dotenv
import logging
from google import genai

# Load environment variables
load_dotenv()

def test_llm():
    api_key = os.getenv('GEMINI_API_KEY')
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    if api_key:
        print(f"API Key prefix: {api_key[:10]}...")
    
    if not api_key:
        print("ERROR: GEMINI_API_KEY is missing")
        return

    try:
        print("Initializing Gemini Client...")
        client = genai.Client(api_key=api_key)
        
        print("Listing available models...")
        try:
            for m in client.models.list(config={"page_size": 10}):
                print(f" - {m.name}")
        except Exception as list_err:
            print(f"Could not list models: {list_err}")

        model_name = 'models/gemini-2.5-flash'
        print(f"Calling model: {model_name}")
        response = client.models.generate_content(
            model=model_name,
            contents="Say 'Hello World' if you can hear me."
        )
        print("Response received:")
        print(response.text)
        print("SUCCESS: LLM is working.")
        
    except Exception as e:
        print(f"ERROR: LLM call failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm()
