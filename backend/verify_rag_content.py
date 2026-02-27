from app.services.vector_store import get_vector_store
import sys

def verify_content():
    print("Initializing Vector Store...")
    try:
        vs = get_vector_store()
        
        queries = [
            "What is the company culture like?",
            "Tell me about the Axis Bank project",
            "Does the company offer mentorship or training?"
        ]
        
        all_passed = True
        
        for q in queries:
            print(f"\nQuerying: '{q}'")
            results = vs.search_knowledge(q, n_results=1)
            
            if not results:
                print("❌ No results found!")
                all_passed = False
                continue
                
            top_result = results[0]['content']
            print(f"✅ Result: {top_result[:100]}...")
            
        if all_passed:
            print("\n✅ Verification Successful: RAG is retrieving seeded content.")
        else:
            print("\n❌ Verification Failed: Some queries returned no results.")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_content()
