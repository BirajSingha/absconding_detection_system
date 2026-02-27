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

    # Add knowledge documents - REPLACED for Chatbot FAQ
    knowledge_docs = [
        {
            'id': 'faq_offer_details',
            'content': """
            Offer Letter & Joining Details:
            
            1. Offer Validity: 7 days from the date of issuance.
            2. Joining Date: Mutual agreement, typically within 30-45 days.
            3. Extension Policy: One-time extension of up to 1 week allowed with valid reason.
            4. Relocation: Company provides relocation assistance (up to $2000) for >50 miles.
            5. Documents Required: ID Proof, Previous Relieving Letter, Education Certificates.
            """,
            'metadata': {
                'category': 'offer_details',
                'source': 'HR_Offer_Policy_2024'
            }
        },
        {
            'id': 'faq_benefits',
            'content': """
            Employee Benefits & Perks:
            
            1. Health Insurance: Comprehensive coverage for self + family.
            2. Leave Policy: 20 Earned Leaves, 12 Sick Leaves, 10 Public Holidays.
            3. Remote Policy: Hybrid model (3 days office, 2 days home).
            4. Learning Budget: $500 per year for certifications/courses.
            5. Wellness: Gym reimbursement and mental health support.
            """,
            'metadata': {
                'category': 'benefits',
                'source': 'HR_Benefits_Guide_2024'
            }
        },
        {
            'id': 'faq_onboarding',
            'content': """
            Onboarding Process (Day 1):
            
            1. Reporting Time: 9:30 AM at Reception.
            2. IT Setup: Laptop and access cards provided on arrival.
            3. Orientation: HR Induction 10:00 AM - 1:00 PM.
            4. Team Intro: Lunch with the team at 1:00 PM.
            5. Buddy System: A mentor will be assigned for the first 30 days.
            """,
            'metadata': {
                'category': 'onboarding',
                'source': 'HR_Onboarding_Manual'
            }
        },
        {
            'id': 'faq_probation',
            'content': """
            Probation & Notice Period:
            
            1. Probation Period: 6 months standard.
            2. Confirmation: Performance review at 5.5 months.
            3. Notice Period (Probation): 15 days from either side.
            4. Notice Period (Confirmed): 2 months.
            """,
            'metadata': {
                'category': 'policies',
                'source': 'HR_Policy_Handbook'
            }
        }
    ]

    print(f"Adding {len(knowledge_docs)} knowledge documents (FAQs)...")
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