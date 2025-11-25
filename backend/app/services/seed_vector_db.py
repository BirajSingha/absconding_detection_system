import os   
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
import uuid

def seed_all(vector_store=None):
    """
    Seed vector database with initial knowledge and historical data.
    If vector_store not provided, connects directly to Chroma Cloud.
    """
    
    if vector_store is None:
        # Direct connection for standalone seeding
        api_key = os.getenv('CHROMA_API_KEY', 'ck-3VzRxrm3GUsaxWetTi9VVxGrct7zCAyvjPVHZdcWB8MB')
        tenant = os.getenv('CHROMA_TENANT', '5ac23f85-bb0a-4f61-a7f4-76d4db665c3c')
        database = os.getenv('CHROMA_DATABASE', 'absconding-detection-system')
        
        try:
            client = chromadb.CloudClient(
                api_key=api_key,
                tenant=tenant,
                database=database
            )
            print("✓ Connected to Chroma Cloud\n")
        except Exception as e:
            print(f"✗ Failed to connect to Chroma Cloud: {e}")
            print("  Seeding skipped.")
            return False
        
        # Setup embedding function
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    else:
        # Use provided vector store
        if not vector_store.is_available:
            print("⚠️  Vector store not available. Seeding skipped.")
            return False
        
        client = vector_store.client
        embedding_function = vector_store.embedding_function

    print("\n" + "="*60)
    print("Seeding Vector Database")
    print("="*60 + "\n")

    # ===== COLLECTION 1: HR Knowledge Base =====
    print("Creating HR Knowledge Base collection...")

    try:
        client.delete_collection("hr_knowledge_base")  # Clean start
    except:
        pass

    knowledge_collection = client.create_collection(
        name="hr_knowledge_base",
        embedding_function=embedding_function,
        metadata={"description": "HR policies and retention strategies"}
    )

    # Add knowledge documents
    knowledge_docs = [
        {
            'id': 'policy_exit_indicators',
            'content': """
            Common Exit Indicators in Employees:
            
            1. Behavioral Changes:
               - Sudden drop in productivity (>30%)
               - Increased absenteeism or tardiness
               - Withdrawal from team activities
               
            2. Communication Patterns:
               - Negative sentiment in emails
               - Reduced meeting participation
               - Complaints about management
               
            3. Statistical Patterns:
               - 80% of absconding cases show attendance issues
               - 65% have negative sentiment
               - 90% have productivity drops >30%
            """,
            'metadata': {
                'category': 'exit_indicators',
                'source': 'HR_Research_2023'
            }
        },
        {
            'id': 'policy_retention_strategies',
            'content': """
            Proven Employee Retention Strategies:
            
            1. Compensation Adjustment (85% success rate)
               - Market salary review within 48 hours
               - Consider 10-15% increase for high performers
               
            2. Career Development (78% success rate)
               - Create clear promotion path
               - Assign mentor/coach
               - Provide training opportunities
               
            3. Flexible Work Arrangements (72% success rate)
               - Remote work options
               - Flexible hours
               - Work-life balance support
            """,
            'metadata': {
                'category': 'retention_strategies',
                'source': 'HR_Best_Practices_2023'
            }
        },
        {
            'id': 'policy_intervention_timeline',
            'content': """
            Intervention Timeline Guidelines:
            
            CRITICAL Risk (80%+ probability):
            - Response Time: Within 24 hours
            - Actions: Immediate HR meeting, compensation review
            - Success Rate: 70% if acted within 24 hours
            
            HIGH Risk (60-79% probability):
            - Response Time: Within 48 hours
            - Actions: Manager check-in, career discussion
            - Success Rate: 75% with proper intervention
            """,
            'metadata': {
                'category': 'intervention_timeline',
                'source': 'HR_Operations_Manual'
            }
        }
    ]

    print(f"Adding {len(knowledge_docs)} knowledge documents...")
    for doc in knowledge_docs:
        knowledge_collection.add(
            documents=[doc['content']],
            metadatas=[doc['metadata']],
            ids=[doc['id']]
        )
        print(f"  ✓ Added: {doc['id']}")

    print(f"✓ Knowledge Base: {knowledge_collection.count()} documents\n")

    # ===== COLLECTION 2: Historical Cases =====
    print("Creating Historical Cases collection...")

    try:
        client.delete_collection("historical_cases")  # Clean start
    except:
        pass

    cases_collection = client.create_collection(
        name="historical_cases",
        embedding_function=embedding_function,
        metadata={"description": "Past absconding cases"}
    )

    # Add historical cases
    cases = [
        {
            'employee_name': 'John Smith',
            'role': 'Senior Developer',
            'department': 'Engineering',
            'tenure_years': 3.5,
            'indicators': 'productivity_drop: 45%, attendance_issues: True, negative_sentiment: True',
            'intervention': 'Compensation increase (15%) + flexible remote work',
            'outcome': 'RETAINED',
            'success': True
        },
        {
            'employee_name': 'Sarah Johnson',
            'role': 'Marketing Manager',
            'department': 'Marketing',
            'tenure_years': 2.0,
            'indicators': 'productivity_drop: 35%, team_conflict: True, negative_sentiment: True',
            'intervention': 'Team restructuring + career development plan',
            'outcome': 'RETAINED',
            'success': True
        },
        {
            'employee_name': 'Michael Chen',
            'role': 'Data Analyst',
            'department': 'Analytics',
            'tenure_years': 1.5,
            'indicators': 'productivity_drop: 50%, attendance_issues: True, resignation_keywords: True',
            'intervention': 'Attempted compensation adjustment (too late)',
            'outcome': 'RESIGNED',
            'success': False
        }
    ]

    print(f"Adding {len(cases)} historical cases...")
    for i, case in enumerate(cases):
        case_id = f"case_{uuid.uuid4().hex[:8]}"
        case_text = f"""
        Employee: {case['employee_name']}
        Role: {case['role']}
        Department: {case['department']}
        Tenure: {case['tenure_years']} years
        
        Indicators: {case['indicators']}
        Intervention: {case['intervention']}
        Outcome: {case['outcome']}
        Success: {case['success']}
        """
        
        cases_collection.add(
            documents=[case_text],
            metadatas=[{
                'outcome': case['outcome'],
                'success': str(case['success']),
                'role': case['role']
            }],
            ids=[case_id]
        )
        print(f"  ✓ Added: {case['employee_name']} ({case['outcome']})")

    print(f"✓ Historical Cases: {cases_collection.count()} cases\n")

    # ===== COLLECTION 3: Employee Communications =====
    print("Creating Employee Communications collection...")

    try:
        client.delete_collection("employee_communications")
    except:
        pass

    comms_collection = client.create_collection(
        name="employee_communications",
        embedding_function=embedding_function,
        metadata={"description": "Employee communications"}
    )

    print("✓ Communications collection created (empty for now)\n")

    # ===== SUMMARY =====
    print("="*60)
    print("✓ SEEDING COMPLETE!")
    print("="*60)
    print(f"\nCollections Created:")
    print(f"  - hr_knowledge_base: {knowledge_collection.count()} documents")
    print(f"  - historical_cases: {cases_collection.count()} cases")
    print(f"  - employee_communications: {comms_collection.count()} messages")
    print("\nCheck your Chroma Cloud dashboard to see the data!")
    print("\n")
    
    return True


if __name__ == '__main__':
    # Allow running as standalone script
    seed_all()