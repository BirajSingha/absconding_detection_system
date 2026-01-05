from flask import Blueprint, request, jsonify
from app.models.candidate import Candidate, InterviewAnalysis
from app.services.llm_analyzer import LLMAnalyzer
from app import db
import hmac
import hashlib
from datetime import datetime

bp = Blueprint('n8n_webhooks', __name__, url_prefix='/api/webhooks/n8n')

llm_analyzer = LLMAnalyzer()

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

@bp.route('/analyze-candidate', methods=['POST'])
def analyze_candidate():
    """
    Webhook endpoint for n8n to trigger candidate analysis.
    
    Expected payload:
    {
        "candidate_id": "CAND123",
        "transcript_text": "...",
        "position": "Software Engineer"
    }
    """
    data = request.json
    
    if not data or 'candidate_id' not in data:
        return jsonify({'error': 'candidate_id is required'}), 400
    
    candidate_id = data['candidate_id']
    candidate = Candidate.query.filter_by(candidate_id=candidate_id).first()
    
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404

    # Perform Analysis
    transcript_text = data.get('transcript_text', '')
    position = data.get('position', candidate.position_applied)
    
    analysis_result = llm_analyzer.analyze_transcript(transcript_text, position)
    
    # Check for Alert Conditions (Low fit or specific sentiment flags)
    should_alert = False
    alert_reason = []
    
    if analysis_result['fit_category'] == 'LOW':
        should_alert = True
        alert_reason.append("Low Fit Score")
        
    tone = analysis_result.get('tone_analysis', {})
    if tone.get('nervousness', 0) > 8:
        should_alert = True
        alert_reason.append("High Nervousness Detected")
        
    # Save analysis to DB
    analysis = InterviewAnalysis(
        candidate_id=candidate.candidate_id,
        fit_score=analysis_result['fit_score'],
        fit_category=analysis_result['fit_category'],
        confidence_score=analysis_result['confidence_score'],
        tone_analysis=analysis_result['tone_analysis'],
        behavioral_traits=analysis_result['behavioral_traits'],
        ai_summary=analysis_result['ai_summary'],
        recommendations=analysis_result['recommendations']
    )
    db.session.add(analysis)
    
    # Update candidate status
    candidate.status = 'INTERVIEWED'
    db.session.commit()
    
    return jsonify({
        'candidate_id': candidate_id,
        'candidate_name': candidate.name,
        'fit_score': analysis_result['fit_score'],
        'fit_category': analysis_result['fit_category'],
        'tone_analysis': analysis_result['tone_analysis'],
        'should_alert_hr': should_alert,
        'alert_reason': ", ".join(alert_reason),
        'summary': analysis_result['ai_summary']
    })

@bp.route('/get-candidates-for-review', methods=['GET'])
def get_candidates_for_review():
    """
    Endpoint for n8n to fetch candidates that need manual HR review.
    """
    # Fetch candidates interviewed but not yet hired/rejected
    # OR fetch recent analyses with alerts
    
    results = []
    # Get recent analyses with LOW category
    analyses = InterviewAnalysis.query.filter_by(fit_category='LOW').order_by(InterviewAnalysis.created_at.desc()).limit(10).all()
    
    for analysis in analyses:
        cand = Candidate.query.filter_by(candidate_id=analysis.candidate_id).first()
        if cand:
            results.append({
                'candidate_id': cand.candidate_id,
                'name': cand.name,
                'position': cand.position_applied,
                'fit_score': analysis.fit_score,
                'fit_category': analysis.fit_category,
                'alert_reason': 'Low Fit Score' # Simplified for now
            })
            
    return jsonify({
        'count': len(results),
        'candidates': results
    })
