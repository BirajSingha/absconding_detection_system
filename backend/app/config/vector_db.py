import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv

load_dotenv()

class VectorDBConfig:
    """Configuration for Chroma Cloud"""
    
    # Chroma Cloud credentials
    CHROMA_API_KEY = os.getenv('CHROMA_API_KEY')
    CHROMA_TENANT = os.getenv('CHROMA_TENANT')
    CHROMA_DATABASE = os.getenv('CHROMA_DATABASE')
    
    # Validate credentials
    if not all([CHROMA_API_KEY, CHROMA_TENANT, CHROMA_DATABASE]):
        print("[WARN] Chroma Cloud credentials not set. Vector DB will run locally.")
        CHROMA_API_KEY = None
        CHROMA_TENANT = None
        CHROMA_DATABASE = None

_chroma_client = None

def get_chroma_client():
    """Get Chroma Cloud client instance (lazy loading with fallback)"""
    global _chroma_client
    
    if _chroma_client is not None:
        return _chroma_client
    
    # If credentials not set, use local persistent client
    if not all([VectorDBConfig.CHROMA_API_KEY, VectorDBConfig.CHROMA_TENANT, VectorDBConfig.CHROMA_DATABASE]):
        print("[WARN] Chroma Cloud not configured. Using local persistent storage.")
        try:
            # Create local storage directory
            persist_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'chroma')
            os.makedirs(persist_path, exist_ok=True)
            
            _chroma_client = chromadb.PersistentClient(path=persist_path)
            print(f"[OK] Initialized local ChromaDB at {persist_path}")
            return _chroma_client
        except Exception as e:
            print(f"[ERROR] Failed to initialize local ChromaDB: {e}")
            return None
    
    try:
        _chroma_client = chromadb.CloudClient(
            api_key=VectorDBConfig.CHROMA_API_KEY,
            tenant=VectorDBConfig.CHROMA_TENANT,
            database=VectorDBConfig.CHROMA_DATABASE
        )
        
        # Test connection
        _chroma_client.heartbeat()
        print("[OK] Connected to Chroma Cloud successfully!")
        
        return _chroma_client
    
    except Exception as e:
        print(f"[WARN] Could not connect to Chroma Cloud: {e}")
        print("       Falling back to local storage.")
        try:
            persist_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'chroma')
            os.makedirs(persist_path, exist_ok=True)
            _chroma_client = chromadb.PersistentClient(path=persist_path)
            return _chroma_client
        except Exception as local_e:
             print(f"[ERROR] Failed to initialize local fallback: {local_e}")
             return None