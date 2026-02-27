from app import create_app, db
from app.models.candidate import Candidate

app = create_app()

with app.app_context():
    # Check if user exists
    if not Candidate.query.filter_by(email="test@test.com").first():
        candidate = Candidate(
            candidate_id="CAND-001",
            name="Test Candidate",
            email="test@test.com",
            position_applied="Software Engineer",
            department="Engineering",
            phone="1234567890"
        )
        candidate.set_password("password123")
        db.session.add(candidate)
        db.session.commit()
        print("User created successfully")
    else:
        print("User already exists")
