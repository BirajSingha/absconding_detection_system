
import sys
import os
import json
from dotenv import load_dotenv

# Add the backend directory to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Load env variables
load_dotenv()

from app.services.rag_service import get_rag_service

def verify_gemini_integration():
    print("Testing Gemini Integration...")
    
    # Check API Key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env")
        return False
        
    print(f"✅ Found GEMINI_API_KEY")

    # Mock Data
    employee_data = {
        "employee_id": "EMP001",
        "name": "John Doe",
        "role": "Senior Developer",
        "department": "Engineering",
        "tenure_years": 3
    }
    
    anomalies = [
        {"type": "productivity_drop", "drop": "30%", "severity": "HIGH"},
        {"type": "attendance_issues", "drop": "20%", "severity": "MEDIUM"}
    ]
    
    sentiment_data = {
        "overall_sentiment": "NEGATIVE",
        "exit_intent_score": 75
    }

    try:
        rag_service = get_rag_service()
        print("✅ RAGService initialized")
        
        print("🤖 Requesting analysis from Gemini...")
        result = rag_service.analyze_risk(employee_data, anomalies, sentiment_data)
        
        print("\n--- Gemini Analysis Result ---")
        print(json.dumps(result, indent=2))
        
        if 'exit_probability' in result:
            print("\n✅ Verification SUCCESS: Received valid analysis from Gemini")
            return True
        else:
            print("\n❌ Verification FAILED: Invalid response structure")
            return False
            
    except Exception as e:
        print(f"\n❌ Verification FAILED with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if verify_gemini_integration():
        sys.exit(0)
    else:
        sys.exit(1)
