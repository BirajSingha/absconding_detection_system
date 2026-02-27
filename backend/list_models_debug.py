import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

with open('models_list.txt', 'w') as f:
    try:
        for m in genai.list_models():
            f.write(f"name: {m.name}\n")
    except Exception as e:
        f.write(f"Error listing models: {e}\n")
