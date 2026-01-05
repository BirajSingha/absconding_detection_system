from flask import Blueprint, request, jsonify
from app.models.candidate import Candidate, InterviewAnalysis
from app.services.llm_analyzer import LLMAnalyzer
from app.services.rag_service import get_rag_service
from app import db
import requests
import os

bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')
llm_analyzer = LLMAnalyzer()

# n8n webhook URL for HR alerts
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL', 'http://localhost:5678/webhook/hr-alert')

@bp.route('/analyze-interview', methods=['POST'])
def analyze_interview():
    """
    Trigger analysis for a candidate's interview using RAG.
    Payload: { "candidate_id": "C001", "transcript_text": "..." }
    """
    data = request.json
    candidate_id = data.get('candidate_id')
    transcript_text = data.get('transcript_text')
    
    candidate = Candidate.query.filter_by(candidate_id=candidate_id).first()
    if not candidate:
        # Auto-create candidate if they don't exist
        candidate = Candidate(
            candidate_id=candidate_id,
            name="Guest Candidate",
            email=f"guest_{candidate_id}@example.com",
            position_applied="Unknown Position",
            department="General",
            status="PENDING"
        )
        db.session.add(candidate)
        db.session.commit()
    
    # Run LLM Analysis (basic)
    analysis_result = llm_analyzer.analyze_transcript(transcript_text, candidate.position_applied)
    
    # Enhance with RAG for absconding risk detection
    rag_result = None
    try:
        rag_service = get_rag_service()
        
        # Build employee data for RAG
        employee_data = {
            'employee_id': candidate_id,
            'name': candidate.name,
            'role': candidate.position_applied,
            'department': candidate.department,
            'tenure_years': 0  # New candidate
        }
        
        # Extract anomalies from tone analysis
        anomalies = []
        tone = analysis_result.get('tone_analysis', {})
        if tone.get('nervousness', 0) > 6:
            anomalies.append({'type': 'high_nervousness', 'value': tone['nervousness']})
        if tone.get('confidence', 10) < 5:
            anomalies.append({'type': 'low_confidence', 'value': tone['confidence']})
        
        # Sentiment data from analysis
        sentiment_data = {
            'overall_sentiment': tone.get('tone_label', 'Neutral'),
            'exit_intent_score': 100 - analysis_result['fit_score']  # Inverse of fit score
        }
        
        # Run RAG analysis
        rag_result = rag_service.analyze_risk(employee_data, anomalies, sentiment_data)
        
        # Merge RAG insights
        if rag_result:
            analysis_result['exit_probability'] = rag_result.get('exit_probability', 0)
            analysis_result['absconding_risk'] = rag_result.get('confidence_level', 'LOW')
            analysis_result['key_risk_indicators'] = rag_result.get('key_indicators', [])
            analysis_result['recommended_actions'] = rag_result.get('recommended_actions', [])
            analysis_result['rag_sources'] = rag_result.get('sources', {})
            
    except Exception as e:
        print(f"RAG analysis failed: {e}")
        # Continue with basic analysis
    
    # Save Analysis
    analysis = InterviewAnalysis(
        candidate_id=candidate_id,
        fit_score=analysis_result['fit_score'],
        fit_category=analysis_result['fit_category'],
        tone_analysis=analysis_result['tone_analysis'],
        behavioral_traits=analysis_result['behavioral_traits'],
        ai_summary=analysis_result['ai_summary'],
        recommendations=analysis_result.get('recommended_actions', analysis_result['recommendations'])
    )
    
    candidate.status = 'INTERVIEWED'
    # Note: fit_score/fit_category are derived from InterviewAnalysis relationship, not stored on Candidate
    
    db.session.add(analysis)
    db.session.commit()
    
    # Trigger n8n webhook for high-risk candidates
    if analysis_result['fit_category'] == 'LOW' or (rag_result and rag_result.get('exit_probability', 0) > 70):
        try:
            trigger_hr_alert(candidate, analysis_result, rag_result)
        except Exception as e:
            print(f"n8n webhook failed: {e}")
    
    return jsonify(analysis.to_dict()), 201


def trigger_hr_alert(candidate, analysis_result, rag_result):
    """Trigger n8n workflow for HR alert"""
    payload = {
        'candidate_id': candidate.candidate_id,
        'candidate_name': candidate.name,
        'position': candidate.position_applied,
        'fit_score': analysis_result['fit_score'],
        'fit_category': analysis_result['fit_category'],
        'exit_probability': rag_result.get('exit_probability', 0) if rag_result else 0,
        'risk_level': rag_result.get('confidence_level', 'UNKNOWN') if rag_result else 'HIGH',
        'key_indicators': rag_result.get('key_indicators', []) if rag_result else ['Low Fit Score'],
        'recommended_actions': rag_result.get('recommended_actions', []) if rag_result else ['HR Review Required'],
        'alert_type': 'HIGH_RISK_CANDIDATE',
        'summary': analysis_result.get('ai_summary', '')
    }
    
    try:
        requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
        print(f"HR Alert triggered for candidate {candidate.candidate_id}")
    except Exception as e:
        print(f"Failed to trigger n8n webhook: {e}")


@bp.route('/candidate/<candidate_id>', methods=['GET'])
def get_candidate_analysis(candidate_id):
    analyses = InterviewAnalysis.query.filter_by(candidate_id=candidate_id).order_by(InterviewAnalysis.created_at.desc()).all()
    return jsonify([a.to_dict() for a in analyses])
