import os
import sys

print("Starting ChromaDB debug...")
try:
    import chromadb
    from chromadb.config import Settings
    print(f"ChromaDB version: {chromadb.__version__}")
except ImportError as e:
    print(f"Failed to import chromadb: {e}")
    sys.exit(1)

try:
    persist_path = os.path.join(os.path.dirname(__file__), 'data', 'chroma_debug')
    os.makedirs(persist_path, exist_ok=True)
    print(f"Creating PersistentClient at {persist_path}...")
    
    client = chromadb.PersistentClient(path=persist_path)
    print("Client created successfully.")
    
    print("Creating collection test_collection...")
    collection = client.create_collection("test_collection")
    print("Collection created.")
    
    print("Adding document...")
    collection.add(documents=["hello world"], ids=["1"])
    print("Document added.")
    
    print("Querying...")
    results = collection.query(query_texts=["hello"], n_results=1)
    print(f"Query result: {results}")

    print("✅ ChromaDB debug passed.")

except Exception as e:
    print(f"❌ ChromaDB error: {e}")
    import traceback
    traceback.print_exc()
