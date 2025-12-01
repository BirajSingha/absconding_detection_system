from app import create_app, db
from app.models.employee import Employee, Communication
from datetime import datetime, timedelta
import random

app = create_app()

def seed_data():
    with app.app_context():
        print("Seeding test employees...")
        
        # 1. New Hire (Tenure < 30 days) - Should be skipped
        new_hire = Employee(
            employee_id=f"TEST_NEW_{random.randint(1000, 9999)}",
            name="Alice Newhire",
            email="alice.new@example.com",
            role="Junior Developer",
            department="Engineering",
            tenure_years=0.1,
            employment_status="ACTIVE",
            productivity_score=85,
            attendance_percentage=95,
            created_at=datetime.utcnow() - timedelta(days=10)
        )
        
        # 2. Stable Employee (Tenure > 30 days) - Low Risk
        stable_emp = Employee(
            employee_id=f"TEST_STABLE_{random.randint(1000, 9999)}",
            name="Bob Stable",
            email="bob.stable@example.com",
            role="Senior Developer",
            department="Engineering",
            tenure_years=2.5,
            employment_status="ACTIVE",
            productivity_score=95,
            attendance_percentage=98,
            created_at=datetime.utcnow() - timedelta(days=365)
        )
        
        # 3. High Risk Employee (Tenure > 30 days) - High Risk
        risk_emp = Employee(
            employee_id=f"TEST_RISK_{random.randint(1000, 9999)}",
            name="Charlie Risk",
            email="charlie.risk@example.com",
            role="Product Manager",
            department="Product",
            tenure_years=1.2,
            employment_status="ACTIVE",
            productivity_score=60,  # Low productivity
            attendance_percentage=75, # Low attendance
            performance_rating=2.0, # Low performance
            created_at=datetime.utcnow() - timedelta(days=120)
        )

        db.session.add(new_hire)
        db.session.add(stable_emp)
        db.session.add(risk_emp)
        db.session.commit()
        
        # Add negative communications for the risky employee
        comms = [
            "I'm really frustrated with the current workload.",
            "Thinking about looking for other opportunities.",
            "This environment is becoming toxic.",
            "I can't handle this stress anymore.",
            "Seriously considering quitting."
        ]
        
        for text in comms:
            comm = Communication(
                employee_id=risk_emp.employee_id,
                text=text,
                source="slack",
                sentiment="NEGATIVE",
                created_at=datetime.utcnow() - timedelta(days=2)
            )
            db.session.add(comm)
            
        db.session.commit()
        
        print("Successfully created:")
        print(f"1. {new_hire.name} (Joined 10 days ago) - Expect: SKIPPED")
        print(f"2. {stable_emp.name} (Joined 1 year ago) - Expect: LOW RISK")
        print(f"3. {risk_emp.name} (Joined 4 months ago) - Expect: HIGH/CRITICAL RISK")

if __name__ == "__main__":
    seed_data()
