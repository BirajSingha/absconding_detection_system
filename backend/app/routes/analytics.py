from flask import Blueprint, request, jsonify
from app.models.employee import Employee, Alert
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@bp.route('/risk-distribution', methods=['GET'])
def risk_distribution():
    """Get distribution of employees by risk level"""
    risk_counts = {
        'CRITICAL': Alert.query.filter_by(risk_level='CRITICAL').count(),
        'HIGH': Alert.query.filter_by(risk_level='HIGH').count(),
        'MEDIUM': Alert.query.filter_by(risk_level='MEDIUM').count(),
        'LOW': Alert.query.filter_by(risk_level='LOW').count()
    }
    
    return jsonify(risk_counts)

@bp.route('/alert-trends', methods=['GET'])
def alert_trends():
    """Get alert trends over the last 30 days"""
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Group alerts by day
    alerts_by_day = db.session.query(
        func.date(Alert.created_at).label('date'),
        func.count(Alert.id).label('count')
    ).filter(Alert.created_at >= start_date).group_by(
        func.date(Alert.created_at)
    ).all()
    
    return jsonify({
        'data': [{'date': str(row[0]), 'count': row[1]} for row in alerts_by_day],
        'total': sum(row[1] for row in alerts_by_day)
    })

@bp.route('/top-at-risk', methods=['GET'])
def top_at_risk():
    """Get top N employees at highest risk"""
    limit = request.args.get('limit', 10, type=int)
    
    alerts = Alert.query.filter(
        Alert.status.in_(['OPEN', 'ACKNOWLEDGED'])
    ).order_by(Alert.risk_score.desc()).limit(limit).all()
    
    result = []
    for alert in alerts:
        employee = Employee.query.filter_by(employee_id=alert.employee_id).first()
        if employee:
            result.append({
                'employee': employee.to_dict(),
                'alert': alert.to_dict()
            })
    
    return jsonify(result)

@bp.route('/department-stats', methods=['GET'])
def department_stats():
    """Get risk statistics by department"""
    departments = db.session.query(
        Employee.department,
        func.count(Employee.id).label('total'),
        func.avg(Employee.productivity_score).label('avg_productivity'),
        func.avg(Employee.attendance_percentage).label('avg_attendance'),
        func.avg(Employee.performance_rating).label('avg_performance')
    ).group_by(Employee.department).all()
    
    result = []
    for dept in departments:
        # Get alert count for this department
        alert_count = db.session.query(func.count(Alert.id)).filter(
            Alert.employee_id.in_(
                db.session.query(Employee.employee_id).filter_by(department=dept[0])
            ),
            Alert.risk_level.in_(['HIGH', 'CRITICAL'])
        ).scalar()
        
        result.append({
            'department': dept[0],
            'total_employees': dept[1],
            'avg_productivity': float(dept[2]) if dept[2] else 0,
            'avg_attendance': float(dept[3]) if dept[3] else 0,
            'avg_performance': float(dept[4]) if dept[4] else 0,
            'high_risk_alerts': alert_count or 0
        })
    
    return jsonify(result)

@bp.route('/alert-summary', methods=['GET'])
def alert_summary():
    """Get overall alert summary"""
    total_employees = Employee.query.count()
    total_alerts = Alert.query.count()
    open_alerts = Alert.query.filter_by(status='OPEN').count()
    resolved_alerts = Alert.query.filter_by(status='RESOLVED').count()
    
    # Calculate average risk score
    avg_risk = db.session.query(func.avg(Alert.risk_score)).scalar() or 0
    
    # Count by status
    status_breakdown = {
        'OPEN': Alert.query.filter_by(status='OPEN').count(),
        'ACKNOWLEDGED': Alert.query.filter_by(status='ACKNOWLEDGED').count(),
        'IN_PROGRESS': Alert.query.filter_by(status='IN_PROGRESS').count(),
        'RESOLVED': Alert.query.filter_by(status='RESOLVED').count()
    }
    
    return jsonify({
        'total_employees': total_employees,
        'total_alerts': total_alerts,
        'open_alerts': open_alerts,
        'resolved_alerts': resolved_alerts,
        'average_risk_score': float(avg_risk),
        'status_breakdown': status_breakdown
    })

@bp.route('/employee/<employee_id>/history', methods=['GET'])
def employee_alert_history(employee_id):
    """Get alert history for a specific employee"""
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    alerts = Alert.query.filter_by(employee_id=employee_id).order_by(
        Alert.created_at.desc()
    ).all()
    
    return jsonify({
        'employee': employee.to_dict(),
        'alerts': [alert.to_dict() for alert in alerts],
        'total_alerts': len(alerts)
    })
