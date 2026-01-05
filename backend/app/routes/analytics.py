from flask import Blueprint, request, jsonify
from app.models.candidate import Candidate, InterviewAnalysis
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@bp.route('/dashboard', methods=['GET'])
def dashboard_stats():
    """Get aggregated dashboard statistics"""
    
    # 1. Fit Distribution
    # Use categories from the model: LOW, MEDIUM, HIGH, EXCELLENT
    fit_counts = {
        'EXCELLENT': InterviewAnalysis.query.filter_by(fit_category='EXCELLENT').count(),
        'HIGH': InterviewAnalysis.query.filter_by(fit_category='HIGH').count(),
        'MEDIUM': InterviewAnalysis.query.filter_by(fit_category='MEDIUM').count(),
        'LOW': InterviewAnalysis.query.filter_by(fit_category='LOW').count()
    }
    
    risk_distribution = [
        {'name': 'Excellent Fit', 'value': fit_counts['EXCELLENT'], 'color': '#10B981'}, # Green
        {'name': 'High Fit', 'value': fit_counts['HIGH'], 'color': '#34D399'}, # Light Green
        {'name': 'Medium Fit', 'value': fit_counts['MEDIUM'], 'color': '#F59E0B'}, # Amber
        {'name': 'Low Fit', 'value': fit_counts['LOW'], 'color': '#EF4444'} # Red
    ]
    
    # 2. Department Stats (Candidates per dept)
    dept_risk = []
    departments = db.session.query(Candidate.department).distinct().all()
    for dept in departments:
        if not dept[0]: continue
        count = Candidate.query.filter_by(department=dept[0]).count()
        dept_risk.append({'name': dept[0], 'high_risk_count': count}) # Reusing field name for frontend compactibility
            
    # 3. Top Candidates (Best Fit)
    top_analyses = InterviewAnalysis.query.order_by(InterviewAnalysis.fit_score.desc()).limit(5).all()
    
    top_risk_employees = [] # Reusing name for frontend compatibility
    for analysis in top_analyses:
        candidate = Candidate.query.filter_by(candidate_id=analysis.candidate_id).first()
        if candidate:
            cand_dict = candidate.to_dict()
            cand_dict['fit_score'] = analysis.fit_score
            cand_dict['fit_category'] = analysis.fit_category
            top_risk_employees.append(cand_dict)
            
    # 4. Recent Analysis
    recent_alerts = InterviewAnalysis.query.order_by(InterviewAnalysis.created_at.desc()).limit(10).all()
    
    return jsonify({
        'risk_distribution': risk_distribution, # Frontend expects this key
        'department_risk': dept_risk,
        'top_risk_employees': top_risk_employees,
        'recent_alerts': [a.to_dict() for a in recent_alerts]
    })

@bp.route('/alert-summary', methods=['GET'])
def alert_summary():
    """Get overall summary stats"""
    total_candidates = Candidate.query.count()
    total_interviews = InterviewAnalysis.query.count()
    pending_interviews = Candidate.query.filter_by(status='PENDING').count()
    completed_interviews = Candidate.query.filter_by(status='INTERVIEWED').count()
    
    avg_fit = db.session.query(func.avg(InterviewAnalysis.fit_score)).scalar() or 0
    
    # Mock trends for now
    trends = {
        'candidates': 5.0, 
        'at_risk': -2.0, 
        'resolved': 10.0, 
        'fit_score': 1.5 
    }
    
    return jsonify({
        'total_candidates': total_candidates,
        'total_interviews': total_interviews,
        'pending_interviews': pending_interviews,
        'completed_interviews': completed_interviews,
        'average_fit_score': float(avg_fit),
        'status_breakdown': {},
        'trends': trends
    })
