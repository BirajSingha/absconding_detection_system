from flask import Blueprint, request, jsonify
from app.models.employee import Employee, Alert
from app.services.anomaly_detector import AnomalyDetector
from app.services.sentiment_analyzer import SentimentAnalyzer
from app import db
import hmac
import hashlib
from datetime import datetime

bp = Blueprint('n8n_webhooks', __name__, url_prefix='/api/webhooks/n8n')

anomaly_detector = AnomalyDetector()
sentiment_analyzer = SentimentAnalyzer()

# Webhook secret for security (optional but recommended)
WEBHOOK_SECRET = "n8n_webhook_secret_key"  # Should be in .env

def verify_webhook_signature(data, signature):
    """Verify webhook signature for security"""
    if not signature:
        return True  # Skip verification if no signature provided
    
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)

@bp.route('/trigger-analysis', methods=['POST'])
def trigger_analysis():
    """
    Webhook endpoint for n8n to trigger employee analysis.
    
    Expected payload:
    {
        "employee_id": "EMP001",
        "communications": [...],
        "notify": true,
        "timeframe_days": 30
    }
    """
    data = request.json
    
    if not data or 'employee_id' not in data:
        return jsonify({'error': 'employee_id is required'}), 400
    
    employee_id = data['employee_id']
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    # Check tenure (must be at least 30 days)
    days_active = (datetime.utcnow() - employee.created_at).days
    if days_active < 30:
        return jsonify({
            'employee_id': employee_id,
            'employee_name': employee.name,
            'risk_score': 0,
            'risk_level': 'LOW',
            'anomalies': [],
            'sentiment': None,
            'should_alert': False,
            'message': f'Employee has only been active for {days_active} days. Minimum 30 days required for analysis.'
        })

    # Perform analysis
    timeframe_days = data.get('timeframe_days', 30)
    anomalies = anomaly_detector.detect_anomalies(employee_id, timeframe_days)
    communications = data.get('communications', [])
    sentiment_data = sentiment_analyzer.analyze_communications(communications)
    
    risk_score = anomaly_detector.calculate_risk_score(anomalies)
    if sentiment_data:
        risk_score = (risk_score + sentiment_data['exit_intent_score']) / 2
    
    # Determine risk level
    if risk_score >= 80:
        risk_level = 'CRITICAL'
    elif risk_score >= 60:
        risk_level = 'HIGH'
    elif risk_score >= 40:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'
    
    return jsonify({
        'employee_id': employee_id,
        'employee_name': employee.name,
        'risk_score': risk_score,
        'risk_level': risk_level,
        'anomalies': anomalies,
        'sentiment': sentiment_data,
        'should_alert': risk_level in ['HIGH', 'CRITICAL'],
        'timeframe_days': timeframe_days
    })

@bp.route('/batch-analysis', methods=['POST'])
def batch_analysis():
    """
    Webhook for n8n to trigger batch analysis of all employees.
    Returns list of employees with risk scores.
    """
    employees = Employee.query.filter_by(employment_status='ACTIVE').all()
    data = request.json or {}
    timeframe_days = data.get('timeframe_days', 30)
    
    results = []
    for employee in employees:
        # Check tenure
        days_active = (datetime.utcnow() - employee.created_at).days
        if days_active < 30:
            results.append({
                'employee_id': employee.employee_id,
                'name': employee.name,
                'department': employee.department,
                'risk_score': 0,
                'risk_level': 'LOW',
                'anomaly_count': 0,
                'status': 'SKIPPED_TENURE',
                'days_active': days_active
            })
            continue

        anomalies = anomaly_detector.detect_anomalies(employee.employee_id, timeframe_days)
        risk_score = anomaly_detector.calculate_risk_score(anomalies)
        
        if risk_score >= 80:
            risk_level = 'CRITICAL'
        elif risk_score >= 60:
            risk_level = 'HIGH'
        elif risk_score >= 40:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        results.append({
            'employee_id': employee.employee_id,
            'name': employee.name,
            'department': employee.department,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'anomaly_count': len(anomalies)
        })
    
    # Sort by risk score descending
    results.sort(key=lambda x: x['risk_score'], reverse=True)
    
    return jsonify({
        'total_employees': len(results),
        'high_risk_count': sum(1 for r in results if r['risk_level'] in ['HIGH', 'CRITICAL']),
        'employees': results,
        'timeframe_days': timeframe_days
    })

@bp.route('/alert-created', methods=['POST'])
def alert_created():
    """
    Webhook to receive notifications from n8n when alert workflow completes.
    Can be used for tracking workflow status.
    """
    data = request.json
    
    # Log the workflow completion
    print(f"n8n workflow completed: {data}")
    
    return jsonify({
        'status': 'received',
        'message': 'Workflow notification received'
    })

@bp.route('/get-high-risk', methods=['GET'])
def get_high_risk_employees():
    """
    Simple endpoint for n8n to fetch current high-risk employees.
    No POST data required.
    """
    alerts = Alert.query.filter(
        Alert.risk_level.in_(['HIGH', 'CRITICAL']),
        Alert.status.in_(['OPEN', 'ACKNOWLEDGED'])
    ).order_by(Alert.risk_score.desc()).limit(20).all()
    
    result = []
    for alert in alerts:
        employee = Employee.query.filter_by(employee_id=alert.employee_id).first()
        if employee:
            result.append({
                'alert_id': alert.id,
                'employee_id': employee.employee_id,
                'employee_name': employee.name,
                'department': employee.department,
                'risk_score': alert.risk_score,
                'risk_level': alert.risk_level,
                'created_at': alert.created_at.isoformat()
            })
    
    return jsonify({
        'count': len(result),
        'employees': result
    })

@bp.route('/lookup-by-email', methods=['GET'])
def lookup_by_email():
    """
    Helper endpoint for n8n to find an employee by email address.
    Query param: ?email=john@example.com
    """
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email parameter is required'}), 400
        
    # Case-insensitive search
    employee = Employee.query.filter(Employee.email.ilike(email)).first()
    
    if not employee:
        return jsonify({'error': 'Employee not found', 'found': False}), 404
        
    return jsonify({
        'found': True,
        'employee_id': employee.employee_id,
        'name': employee.name,
        'email': employee.email,
        'department': employee.department,
        'role': employee.role
    })
