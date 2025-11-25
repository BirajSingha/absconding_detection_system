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
        print("⚠️  Warning: Chroma Cloud credentials not set. Vector DB will not be available.")
        CHROMA_API_KEY = None
        CHROMA_TENANT = None
        CHROMA_DATABASE = None

_chroma_client = None

def get_chroma_client():
    """Get Chroma Cloud client instance (lazy loading with fallback)"""
    global _chroma_client
    
    if _chroma_client is not None:
        return _chroma_client
    
    # If credentials not set, return None (will use fallback in vector_store)
    if not all([VectorDBConfig.CHROMA_API_KEY, VectorDBConfig.CHROMA_TENANT, VectorDBConfig.CHROMA_DATABASE]):
        print("⚠️  Chroma Cloud not configured. Using local vector store fallback.")
        return None
    
    try:
        _chroma_client = chromadb.CloudClient(
            api_key=VectorDBConfig.CHROMA_API_KEY,
            tenant=VectorDBConfig.CHROMA_TENANT,
            database=VectorDBConfig.CHROMA_DATABASE
        )
        
        # Test connection
        _chroma_client.heartbeat()
        print("✓ Connected to Chroma Cloud successfully!")
        
        return _chroma_client
    
    except Exception as e:
        print(f"⚠️  Could not connect to Chroma Cloud: {e}")
        print("   Using local vector store fallback instead.")
        return None