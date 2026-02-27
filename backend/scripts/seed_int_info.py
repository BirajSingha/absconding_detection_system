import requests
import json
import time

BASE_URL = "http://localhost:5000/api/vector-db"

def seed_data():
    print(f"Connecting to {BASE_URL}...")
    
    # 1. Company Culture
    culture_docs = [
        {
            "id": "int_culture_001",
            "content": "Indus Net Technologies (INT.) fosters a supportive and friendly work environment where teamwork is highly valued. Employees report that management is approachable and provides guidance on technical challenges.",
            "metadata": {"category": "Culture", "source": "Employee Reviews"}
        },
        {
            "id": "int_culture_002",
            "content": "Work-life balance is respected at INT., with flexible timings and a lack of micromanagement reported by many employees. The atmosphere is productive yet fun.",
            "metadata": {"category": "Culture", "source": "Indeed Reviews"}
        },
        {
            "id": "int_culture_003",
            "content": "The company emphasizes continuous learning and professional development. It is described as a 'great learning' environment where employees can explore professional talents.",
            "metadata": {"category": "Culture", "source": "Employee Feedback"}
        }
    ]

    # 2. Projects & Expertise
    project_docs = [
        {
            "id": "int_project_001",
            "content": "INT. successfully developed a user-friendly corporate banking application for Axis Bank, one of India's largest private sector banks, showcasing expertise in fintech solutions.",
            "metadata": {"category": "Projects", "client": "Axis Bank"}
        },
        {
            "id": "int_project_002",
            "content": "For SBI General Insurance, INT. created a multilingual responsive website and transaction portal, enabling seamless online processing of insurance products.",
            "metadata": {"category": "Projects", "client": "SBI General Insurance"}
        },
        {
            "id": "int_project_003",
            "content": "INT. serves as a digital partner for major pharmaceutical companies like Cipla and steel manufacturers like Elegant Steel, delivering digital transformation solutions.",
            "metadata": {"category": "Projects", "Sector": "Pharma & Manufacturing"}
        }
    ]

    # 3. Structure & Innovation
    structure_docs = [
        {
            "id": "int_structure_001",
            "content": "Indus Net Technologies has established 'Centers of Excellence' in key areas: Digital Engineering, Data & AI, Cloud & Cybersecurity, and Digital Marketing.",
            "metadata": {"category": "Structure", "type": "Center of Excellence"}
        },
        {
            "id": "int_structure_002",
            "content": "INT. operates 'Indus Net Labs', a digital acceleration lab that nurtures and mentors B2B digital technology startups, and 'Indus Net Academy' for training.",
            "metadata": {"category": "Structure", "type": "Innovation Lab"}
        },
        {
            "id": "int_structure_003",
            "content": "The company philosophy is 'Co-owning outcomes', meaning they focus on delivering measurable business impact for clients rather than just software deliverables.",
            "metadata": {"category": "Values", "concept": "Co-owning outcomes"}
        }
    ]

    all_docs = culture_docs + project_docs + structure_docs
    
    success_count = 0
    for doc in all_docs:
        try:
            response = requests.post(f"{BASE_URL}/add-knowledge", json=doc)
            if response.status_code == 201:
                print(f"✅ Added: {doc['id']}")
                success_count += 1
            else:
                print(f"❌ Failed: {doc['id']} - {response.text}")
        except Exception as e:
            print(f"❌ Error connecting: {e}")
            break
            
    print(f"\nSeeding Complete! Added {success_count}/{len(all_docs)} documents.")

if __name__ == "__main__":
    seed_data()
