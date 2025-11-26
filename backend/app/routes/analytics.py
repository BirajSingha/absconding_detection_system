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
    
    # Calculate trends (compare to 30 days ago)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    sixty_days_ago = datetime.utcnow() - timedelta(days=60)
    
    # 1. Employee Growth Trend
    employees_last_month = Employee.query.filter(Employee.created_at < thirty_days_ago).count()
    if employees_last_month > 0:
        emp_trend = ((total_employees - employees_last_month) / employees_last_month) * 100
    else:
        emp_trend = 100 if total_employees > 0 else 0
        
    # 2. At Risk Trend (New alerts in last 30 days vs previous 30 days)
    new_alerts_current = Alert.query.filter(Alert.created_at >= thirty_days_ago).count()
    new_alerts_prev = Alert.query.filter(Alert.created_at >= sixty_days_ago, Alert.created_at < thirty_days_ago).count()
    
    if new_alerts_prev > 0:
        risk_trend = ((new_alerts_current - new_alerts_prev) / new_alerts_prev) * 100
    else:
        risk_trend = 100 if new_alerts_current > 0 else 0
        
    # 3. Resolution Trend (Resolved in last 30 days vs previous 30 days)
    # Note: Using updated_at as proxy for resolution time if resolved_at not available
    resolved_current = Alert.query.filter(
        Alert.status == 'RESOLVED',
        Alert.updated_at >= thirty_days_ago
    ).count()
    resolved_prev = Alert.query.filter(
        Alert.status == 'RESOLVED',
        Alert.updated_at >= sixty_days_ago,
        Alert.updated_at < thirty_days_ago
    ).count()
    
    if resolved_prev > 0:
        resolution_trend = ((resolved_current - resolved_prev) / resolved_prev) * 100
    else:
        resolution_trend = 100 if resolved_current > 0 else 0
        
    # 4. Risk Score Trend (Avg risk of alerts in last 30 days vs previous)
    avg_risk_current = db.session.query(func.avg(Alert.risk_score)).filter(
        Alert.created_at >= thirty_days_ago
    ).scalar() or 0
    
    avg_risk_prev = db.session.query(func.avg(Alert.risk_score)).filter(
        Alert.created_at >= sixty_days_ago,
        Alert.created_at < thirty_days_ago
    ).scalar() or 0
    
    if avg_risk_prev > 0:
        score_trend = ((avg_risk_current - avg_risk_prev) / avg_risk_prev) * 100
    else:
        score_trend = 0 # No previous data to compare
    
    return jsonify({
        'total_employees': total_employees,
        'total_alerts': total_alerts,
        'open_alerts': open_alerts,
        'resolved_alerts': resolved_alerts,
        'average_risk_score': float(avg_risk),
        'status_breakdown': status_breakdown,
        'trends': {
            'employees': round(emp_trend, 1),
            'at_risk': round(risk_trend, 1),
            'resolved': round(resolution_trend, 1),
            'risk_score': round(score_trend, 1)
        }
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

@bp.route('/dashboard', methods=['GET'])
def dashboard_stats():
    """Get aggregated dashboard statistics"""
    # 1. Risk Distribution
    risk_counts = {
        'CRITICAL': Alert.query.filter_by(risk_level='CRITICAL', status='OPEN').count(),
        'HIGH': Alert.query.filter_by(risk_level='HIGH', status='OPEN').count(),
        'MEDIUM': Alert.query.filter_by(risk_level='MEDIUM', status='OPEN').count(),
        'LOW': Alert.query.filter_by(risk_level='LOW', status='OPEN').count()
    }
    
    risk_distribution = [
        {'name': 'Critical', 'value': risk_counts['CRITICAL'], 'color': '#EF4444'},
        {'name': 'High Risk', 'value': risk_counts['HIGH'], 'color': '#F97316'},
        {'name': 'Medium Risk', 'value': risk_counts['MEDIUM'], 'color': '#F59E0B'},
        {'name': 'Low Risk', 'value': risk_counts['LOW'], 'color': '#10B981'}
    ]
    
    # 2. Department Risk
    dept_risk = []
    departments = db.session.query(Employee.department).distinct().all()
    for dept in departments:
        high_risk_count = db.session.query(func.count(Alert.id)).filter(
            Alert.employee_id.in_(
                db.session.query(Employee.employee_id).filter_by(department=dept[0])
            ),
            Alert.risk_level.in_(['HIGH', 'CRITICAL']),
            Alert.status == 'OPEN'
        ).scalar()
        if high_risk_count > 0:
            dept_risk.append({'name': dept[0], 'high_risk_count': high_risk_count})
    
    # 3. Top Risk Employees
    top_alerts = Alert.query.filter(
        Alert.status.in_(['OPEN', 'ACKNOWLEDGED'])
    ).order_by(Alert.risk_score.desc()).limit(5).all()
    
    top_risk_employees = []
    for alert in top_alerts:
        employee = Employee.query.filter_by(employee_id=alert.employee_id).first()
        if employee:
            emp_dict = employee.to_dict()
            emp_dict['risk_score'] = alert.risk_score
            emp_dict['risk_level'] = alert.risk_level
            top_risk_employees.append(emp_dict)
            
    # 4. Recent Alerts
    recent_alerts = Alert.query.order_by(Alert.created_at.desc()).limit(10).all()
    
    return jsonify({
        'risk_distribution': risk_distribution,
        'department_risk': dept_risk,
        'top_risk_employees': top_risk_employees,
        'recent_alerts': [alert.to_dict() for alert in recent_alerts]
    })
