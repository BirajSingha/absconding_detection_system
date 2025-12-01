from app import create_app, db
from app.models.employee import Employee, Alert

app = create_app()

def check_alerts():
    with app.app_context():
        # Get the test employees
        test_ids = ["TEST_NEW", "TEST_STABLE", "TEST_RISK"]
        
        print(f"{'Employee Name':<20} | {'ID':<15} | {'Risk Score':<10} | {'Alert Status'}")
        print("-" * 65)
        
        employees = Employee.query.filter(Employee.employee_id.like("TEST_%")).all()
        
        for emp in employees:
            # Get latest alert
            latest_alert = Alert.query.filter_by(employee_id=emp.employee_id)\
                .order_by(Alert.created_at.desc()).first()
            
            score = latest_alert.risk_score if latest_alert else "N/A"
            status = latest_alert.status if latest_alert else "No Alert"
            
            print(f"{emp.name:<20} | {emp.employee_id:<15} | {str(score):<10} | {status}")

if __name__ == "__main__":
    check_alerts()
