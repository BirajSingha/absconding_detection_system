from flask import Blueprint, request, jsonify
from app.models.employee import Employee, Alert
from app.services.anomaly_detector import AnomalyDetector
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.services.rag_service import get_rag_service
from app.services.vector_store import get_vector_store
from app.services.slack_service import get_slack_service
from app.services.email_service import get_email_service
from app import db
import uuid

bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')

# Initialize services
anomaly_detector = AnomalyDetector()
sentiment_analyzer = SentimentAnalyzer()
rag_service = get_rag_service()
vector_store = get_vector_store()
slack_service = get_slack_service()
email_service = get_email_service()

@bp.route('', methods=['GET'])
def list_alerts():
    """Get all alerts with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    risk_level = request.args.get('risk_level')
    
    query = Alert.query
    
    if status:
        query = query.filter_by(status=status)
    if risk_level:
        query = query.filter_by(risk_level=risk_level)
        
    # Sort by created_at desc
    query = query.order_by(Alert.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'alerts': [alert.to_dict() for alert in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@bp.route('/<int:alert_id>', methods=['GET'])
def get_alert(alert_id):
    """Get specific alert details"""
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    return jsonify(alert.to_dict())

@bp.route('/analyze/<employee_id>', methods=['POST'])
def analyze_employee(employee_id):
    """Run comprehensive analysis on employee using Vector DB RAG"""
    
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    # Get request data
    data = request.json
    communications = data.get('communications', [])
    
    # Store communications in vector DB for future analysis
    for comm in communications:
        comm_id = f"comm_{employee_id}_{uuid.uuid4().hex[:8]}"
        # Analyze sentiment first
        sentiment = sentiment_analyzer.analyze_text(comm.get('text', ''))
        
        vector_store.add_communication(
            comm_id=comm_id,
            employee_id=employee_id,
            text=comm.get('text', ''),
            source=comm.get('source', 'unknown'),
            sentiment=sentiment['sentiment'] if sentiment else 'NEUTRAL'
        )
    
    # 1. Detect behavioral anomalies
    anomalies = anomaly_detector.detect_anomalies(employee_id)
    
    # 2. Analyze sentiment
    sentiment_data = sentiment_analyzer.analyze_communications(communications)
    
    # 3. Calculate initial risk score
    risk_score = anomaly_detector.calculate_risk_score(anomalies)
    if sentiment_data:
        risk_score = (risk_score + sentiment_data['exit_intent_score']) / 2
    
    # 4. Get AI insights with Vector DB RAG
    ai_insights = rag_service.analyze_risk(
        employee.to_dict(),
        anomalies,
        sentiment_data or {}
    )
    
    # Use AI's exit probability as final confidence score
    final_risk_score = ai_insights.get('exit_probability', risk_score)
    
    # Determine risk level
    if final_risk_score >= 80:
        risk_level = 'CRITICAL'
    elif final_risk_score >= 60:
        risk_level = 'HIGH'
    elif final_risk_score >= 40:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'
    
    # Create alert if risk is significant
    if final_risk_score >= 40:
        alert = Alert(
            employee_id=employee_id,
            risk_score=final_risk_score,
            risk_level=risk_level,
            confidence_score=final_risk_score,
            behavioral_indicators=anomalies,
            sentiment_indicators=sentiment_data or {},
            ai_summary=ai_insights.get('summary'),
            timeline_estimate=ai_insights.get('timeline_estimate'),
            recommendations=ai_insights.get('recommended_actions', [])
        )
        
        db.session.add(alert)
        db.session.commit()
        
        # TRIGGER: Send multi-channel notifications for high risk alerts
        if risk_level in ['HIGH', 'CRITICAL']:
            # Send Slack notification
            slack_service.send_high_risk_alert(
                employee=employee,
                risk_score=final_risk_score,
                risk_level=risk_level,
                anomalies=anomalies,
                sentiment_data=sentiment_data
            )
            
            # Send Email notification
            email_service.send_high_risk_alert(
                employee=employee,
                risk_score=final_risk_score,
                risk_level=risk_level,
                anomalies=anomalies,
                sentiment_data=sentiment_data
            )
        
        response = alert.to_dict()
        response['ai_insights'] = ai_insights
        response['vector_db_sources'] = ai_insights.get('sources', {})
        
        return jsonify(response), 201
    
    return jsonify({
        'message': 'No significant risk detected',
        'risk_score': final_risk_score,
        'anomalies': anomalies,
        'ai_insights': ai_insights
    })

@bp.route('/<int:alert_id>/outcome', methods=['POST'])
def record_outcome(alert_id):
    """Record the outcome of an alert for ML learning"""
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    data = request.json
    outcome = data.get('outcome')  # RETAINED, RESIGNED, FALSE_POSITIVE
    success = outcome == 'RETAINED'
    
    # Store outcome in vector DB for future learning
    employee = Employee.query.filter_by(employee_id=alert.employee_id).first()
    
    alert_data = {
        'employee_name': employee.name,
        'employee_id': employee.employee_id,
        'role': employee.role,
        'department': employee.department,
        'tenure_years': employee.tenure_years,
        'behavioral_indicators': alert.behavioral_indicators,
        'intervention_taken': data.get('intervention'),
        'timestamp': alert.created_at.isoformat()
    }
    
    rag_service.store_case_outcome(alert_data, outcome, success)
    
    # Update alert
from flask import Blueprint, request, jsonify
from app.models.employee import Employee, Alert
from app.services.anomaly_detector import AnomalyDetector
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.services.rag_service import get_rag_service
from app.services.vector_store import get_vector_store
from app.services.slack_service import get_slack_service
from app.services.email_service import get_email_service
from app import db
import uuid

bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')

# Initialize services
anomaly_detector = AnomalyDetector()
sentiment_analyzer = SentimentAnalyzer()
rag_service = get_rag_service()
vector_store = get_vector_store()
slack_service = get_slack_service()
email_service = get_email_service()

@bp.route('', methods=['GET'])
def list_alerts():
    """Get all alerts with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    risk_level = request.args.get('risk_level')
    
    query = Alert.query
    
    if status:
        query = query.filter_by(status=status)
    if risk_level:
        query = query.filter_by(risk_level=risk_level)
        
    # Sort by created_at desc
    query = query.order_by(Alert.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'alerts': [alert.to_dict() for alert in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@bp.route('/<int:alert_id>', methods=['GET'])
def get_alert(alert_id):
    """Get specific alert details"""
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    return jsonify(alert.to_dict())

@bp.route('/analyze/<employee_id>', methods=['POST'])
def analyze_employee(employee_id):
    """Run comprehensive analysis on employee using Vector DB RAG"""
    
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    # Get request data
    data = request.json
    communications = data.get('communications', [])
    
    # Store communications in vector DB for future analysis
    for comm in communications:
        comm_id = f"comm_{employee_id}_{uuid.uuid4().hex[:8]}"
        # Analyze sentiment first
        sentiment = sentiment_analyzer.analyze_text(comm.get('text', ''))
        
        vector_store.add_communication(
            comm_id=comm_id,
            employee_id=employee_id,
            text=comm.get('text', ''),
            source=comm.get('source', 'unknown'),
            sentiment=sentiment['sentiment'] if sentiment else 'NEUTRAL'
        )
    
    # 1. Detect behavioral anomalies
    anomalies = anomaly_detector.detect_anomalies(employee_id)
    
    # 2. Analyze sentiment
    sentiment_data = sentiment_analyzer.analyze_communications(communications)
    
    # 3. Calculate initial risk score
    risk_score = anomaly_detector.calculate_risk_score(anomalies)
    if sentiment_data:
        risk_score = (risk_score + sentiment_data['exit_intent_score']) / 2
    
    # 4. Get AI insights with Vector DB RAG
    ai_insights = rag_service.analyze_risk(
        employee.to_dict(),
        anomalies,
        sentiment_data or {}
    )
    
    # Use AI's exit probability as final confidence score
    final_risk_score = ai_insights.get('exit_probability', risk_score)
    
    # Determine risk level
    if final_risk_score >= 80:
        risk_level = 'CRITICAL'
    elif final_risk_score >= 60:
        risk_level = 'HIGH'
    elif final_risk_score >= 40:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'
    
    # Create alert if risk is significant
    if final_risk_score >= 40:
        alert = Alert(
            employee_id=employee_id,
            risk_score=final_risk_score,
            risk_level=risk_level,
            confidence_score=final_risk_score,
            behavioral_indicators=anomalies,
            sentiment_indicators=sentiment_data or {},
            ai_summary=ai_insights.get('summary'),
            timeline_estimate=ai_insights.get('timeline_estimate'),
            recommendations=ai_insights.get('recommended_actions', [])
        )
        
        db.session.add(alert)
        db.session.commit()
        
        # TRIGGER: Send multi-channel notifications for high risk alerts
        if risk_level in ['HIGH', 'CRITICAL']:
            # Send Slack notification
            slack_service.send_high_risk_alert(
                employee=employee,
                risk_score=final_risk_score,
                risk_level=risk_level,
                anomalies=anomalies,
                sentiment_data=sentiment_data
            )
            
            # Send Email notification
            email_service.send_high_risk_alert(
                employee=employee,
                risk_score=final_risk_score,
                risk_level=risk_level,
                anomalies=anomalies,
                sentiment_data=sentiment_data
            )
        
        response = alert.to_dict()
        response['ai_insights'] = ai_insights
        response['vector_db_sources'] = ai_insights.get('sources', {})
        
        return jsonify(response), 201
    
    return jsonify({
        'message': 'No significant risk detected',
        'risk_score': final_risk_score,
        'anomalies': anomalies,
        'ai_insights': ai_insights
    })

@bp.route('/<int:alert_id>/outcome', methods=['POST'])
def record_outcome(alert_id):
    """Record the outcome of an alert for ML learning"""
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    data = request.json
    outcome = data.get('outcome')  # RETAINED, RESIGNED, FALSE_POSITIVE
    success = outcome == 'RETAINED'
    
    # Store outcome in vector DB for future learning
    employee = Employee.query.filter_by(employee_id=alert.employee_id).first()
    
    alert_data = {
        'employee_name': employee.name,
        'employee_id': employee.employee_id,
        'role': employee.role,
        'department': employee.department,
        'tenure_years': employee.tenure_years,
        'behavioral_indicators': alert.behavioral_indicators,
        'intervention_taken': data.get('intervention'),
        'timestamp': alert.created_at.isoformat()
    }
    
    rag_service.store_case_outcome(alert_data, outcome, success)
    
    # Update alert
    alert.status = 'RESOLVED'
    alert.reviewed_by = data.get('reviewed_by')
    alert.reviewed_at = db.func.now()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Outcome recorded successfully',
        'alert_id': alert_id,
        'outcome': outcome,
        'learned': True
    })

@bp.route('/<int:alert_id>/status', methods=['PUT'])
def update_alert_status(alert_id):
    """Update alert status"""
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    data = request.json
    status = data.get('status')
    
    if status not in ['OPEN', 'ACKNOWLEDGED', 'RESOLVED', 'IN_PROGRESS']:
        return jsonify({'error': 'Invalid status'}), 400
        
    alert.status = status
    if status == 'RESOLVED':
        alert.resolved_at = db.func.now()
        
    db.session.commit()
    
    return jsonify(alert.to_dict())