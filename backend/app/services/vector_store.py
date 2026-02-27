import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import json
from datetime import datetime
import os

class VectorStore:
    """Manages vector embeddings and similarity search with Chroma Cloud"""
    
    def __init__(self):
        # Initialize Chroma Cloud client (with fallback)
        from app.config.vector_db import get_chroma_client
        self.client = get_chroma_client()
        self.is_available = self.client is not None
        
        if self.is_available:
            print("[INFO] Vector Store Client initialized", flush=True)
        else:
            print("[WARN] Vector Store unavailable - Using in-memory storage fallback", flush=True)
            self.in_memory_docs = {}  # Fallback storage
        
        # Use sentence-transformers for embeddings (FREE & fast)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create embedding function for Chroma (if available)
        if self.is_available:
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        else:
            self.embedding_function = None
        
        # Initialize collections
        self._init_collections()
    
    def _init_collections(self):
        """Initialize vector database collections"""
        if not self.is_available:
            print("   Skipping collection initialization (Chroma Cloud unavailable)")
            return
        
        # Collection 1: HR Knowledge Base
        try:
            self.knowledge_collection = self.client.get_collection(
                name="hr_knowledge_base",
                embedding_function=self.embedding_function
            )
            print("   [OK] Connected to 'hr_knowledge_base' collection")
        except:
            self.knowledge_collection = self.client.create_collection(
                name="hr_knowledge_base",
                embedding_function=self.embedding_function,
                metadata={"description": "HR policies, retention strategies, and best practices"}
            )
            print("   [OK] Created 'hr_knowledge_base' collection")
        
        # Collection 2: Historical Cases
        try:
            self.cases_collection = self.client.get_collection(
                name="historical_cases",
                embedding_function=self.embedding_function
            )
            print("   [OK] Connected to 'historical_cases' collection")
        except:
            self.cases_collection = self.client.create_collection(
                name="historical_cases",
                embedding_function=self.embedding_function,
                metadata={"description": "Past absconding cases and outcomes"}
            )
            print("   [OK] Created 'historical_cases' collection")
        
        # Collection 3: Employee Communications
        try:
            self.communications_collection = self.client.get_collection(
                name="employee_communications",
                embedding_function=self.embedding_function
            )
            print("   [OK] Connected to 'employee_communications' collection")
        except:
            self.communications_collection = self.client.create_collection(
                name="employee_communications",
                embedding_function=self.embedding_function,
                metadata={"description": "Employee email and chat history"}
            )
            print("   [OK] Created 'employee_communications' collection")
    
    # Rest of the methods remain the same...
    # (Keep all other methods from the previous vector_store.py)
    
    def add_knowledge_document(self, doc_id: str, content: str, metadata: Dict):
        """Add document to knowledge base"""
        if not self.is_available:
            return
        
        try:
            self.knowledge_collection.add(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
        except Exception as e:
            print(f"   Error adding knowledge document: {e}")
    
    def add_historical_case(self, case_id: str, case_data: Dict):
        """Add historical absconding case"""
        if not self.is_available:
            return
        
        try:
            case_text = f"""
            Employee: {case_data.get('employee_name')}
            Role: {case_data.get('role')}
            Department: {case_data.get('department')}
            Tenure: {case_data.get('tenure_years')} years
            
            Indicators:
            {json.dumps(case_data.get('indicators', {}), indent=2)}
            
            Intervention: {case_data.get('intervention')}
            Outcome: {case_data.get('outcome')}
            Success: {case_data.get('success', False)}
            """
            
            self.cases_collection.add(
                documents=[case_text],
                metadatas=[{
                    'case_id': case_id,
                    'outcome': case_data.get('outcome'),
                    'success': case_data.get('success'),
                    'timestamp': case_data.get('timestamp', str(datetime.now()))
                }],
                ids=[case_id]
            )
        except Exception as e:
            print(f"   Error adding historical case: {e}")
    
    def add_communication(self, comm_id: str, employee_id: str, text: str, 
                         source: str, sentiment: str):
        """Add employee communication for analysis"""
        if not self.is_available:
            return
        
        try:
            self.communications_collection.add(
                documents=[text],
                metadatas=[{
                    'employee_id': employee_id,
                    'source': source,
                    'sentiment': sentiment,
                    'timestamp': str(datetime.now())
                }],
                ids=[comm_id]
            )
        except Exception as e:
            print(f"   Error adding communication: {e}")
    
    def search_similar_cases(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for similar historical cases"""
        if not self.is_available:
            print("   (Using mock results - Chroma Cloud unavailable)")
            return []
        
        try:
            results = self.cases_collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return self._format_results(results)
        except Exception as e:
            print(f"   Error searching cases: {e}")
            return []
    
    def search_knowledge(self, query: str, n_results: int = 3) -> List[Dict]:
        """Search HR knowledge base"""
        if not self.is_available:
            print("   (Using mock results - Chroma Cloud unavailable)")
            return []
        
        try:
            results = self.knowledge_collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return self._format_results(results)
        except Exception as e:
            print(f"   Error searching knowledge: {e}")
            return []
    
    def search_employee_communications(self, employee_id: str, 
                                      query: Optional[str] = None,
                                      n_results: int = 10) -> List[Dict]:
        """Search employee's past communications"""
        if not self.is_available:
            print("   (Using mock results - Chroma Cloud unavailable)")
            return []
        
        try:
            if query:
                results = self.communications_collection.query(
                    query_texts=[query],
                    where={"employee_id": employee_id},
                    n_results=n_results
                )
            else:
                results = self.communications_collection.get(
                    where={"employee_id": employee_id},
                    limit=n_results
                )
            return self._format_results(results)
        except Exception as e:
            print(f"   Error searching communications: {e}")
            return []
    
    def _format_results(self, results: Dict) -> List[Dict]:
        """Format Chroma query results"""
        formatted = []
        
        if 'documents' in results and results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                formatted.append({
                    'content': doc,
                    'metadata': results['metadatas'][0][i] if 'metadatas' in results else {},
                    'distance': results['distances'][0][i] if 'distances' in results else None,
                    'id': results['ids'][0][i] if 'ids' in results else None
                })
        
        return formatted
    
    def get_collection_stats(self):
        """Get statistics about collections"""
        if not self.is_available:
            return {
                'knowledge_base_count': 0,
                'historical_cases_count': 0,
                'communications_count': 0,
                'status': 'Chroma Cloud unavailable'
            }
        
        try:
            return {
                'knowledge_base_count': self.knowledge_collection.count(),
                'historical_cases_count': self.cases_collection.count(),
                'communications_count': self.communications_collection.count()
            }
        except Exception as e:
            print(f"   Error getting collection stats: {e}")
            return {}


# Singleton instance
_vector_store_instance = None

def get_vector_store() -> VectorStore:
    """Get VectorStore singleton instance"""
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore()
    return _vector_store_instance