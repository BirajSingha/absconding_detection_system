from flask import Blueprint, request, jsonify
from app.models.candidate import Candidate, InterviewAnalysis
from app.services.llm_analyzer import LLMAnalyzer
from app.services.rag_service import get_rag_service
from app import db
import requests
import os

bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')
llm_analyzer = None
def get_llm_analyzer():
    global llm_analyzer
    if not llm_analyzer:
        llm_analyzer = LLMAnalyzer()
    return llm_analyzer

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
    candidate_name = data.get('candidate_name', 'Guest Candidate')
    position = data.get('position', 'Unknown Position')
    
    candidate = Candidate.query.filter_by(candidate_id=candidate_id).first()
    if not candidate:
        # Auto-create candidate if they don't exist
        candidate = Candidate(
            candidate_id=candidate_id,
            name=candidate_name,
            email=f"guest_{candidate_id}@example.com",
            position_applied=position,
            department="General",
            status="PENDING"
        )
        db.session.add(candidate)
        db.session.commit()
    else:
        # Update name/position if previously generic
        if candidate.name == "Guest Candidate" and candidate_name != "Guest Candidate":
            candidate.name = candidate_name
        if candidate.position_applied == "Unknown Position" and position != "Unknown Position":
            candidate.position_applied = position
        db.session.commit()
    
    # Run LLM Analysis (basic)
    analysis_result = get_llm_analyzer().analyze_transcript(transcript_text, candidate.position_applied)
    
    # Enhance with RAG for absconding risk detection
    rag_result = None
    try:
        rag_service = get_rag_service()
        
        # Build employee data for RAG
        from datetime import datetime
        tenure_years = 0
        bond_risk = False
        
        if candidate.joining_date:
            try:
                # Calculate tenure in years
                join_date = candidate.joining_date
                if isinstance(join_date, str):
                    try:
                        join_date = datetime.strptime(join_date, "%Y-%m-%d").date()
                    except:
                        pass # Keep as is if parsing fails, or handle appropriately
                
                # If join_date is a date object
                today = datetime.now().date()
                if hasattr(join_date, 'year'):
                    tenure_years = (today - join_date).days / 365.25
                
                # Check bond status
                if tenure_years < 2 and candidate.service_bond_active:
                    bond_risk = True
            except Exception as e:
                print(f"Error calculating tenure: {e}")

        employee_data = {
            'employee_id': candidate_id,
            'name': candidate.name,
            'role': candidate.position_applied,
            'department': candidate.department,
            'tenure_years': round(tenure_years, 1),
            'bond_active': bond_risk
        }
        
        # Extract anomalies from tone analysis
        anomalies = []
        tone = analysis_result.get('tone_analysis', {})
        if tone.get('nervousness', 0) > 6:
            anomalies.append({'type': 'high_nervousness', 'value': tone['nervousness']})
        if tone.get('confidence', 10) < 5:
            anomalies.append({'type': 'low_confidence', 'value': tone['confidence']})
            
        # Policy-based anomalies
        if bond_risk:
            # If high exit intent is detected (inverse of fit score or from tone), flag bond risk
            exit_intent_score = 100 - analysis_result.get('fit_score', 0)
            if exit_intent_score > 40: # Threshold for concern
                anomalies.append({
                    'type': 'Service Bond Violation Risk',
                    'value': 'High',
                    'drop': f"Potential early exit within {int(tenure_years*12)} months of 24-month bond"
                })
        
        # Sentiment data from analysis
        sentiment_data = {
            'overall_sentiment': tone.get('tone_label', 'Neutral'),
            'exit_intent_score': 100 - analysis_result['fit_score']  # Inverse of fit score
        }
        
        # Fetch previous analysis for context
        previous_analysis_record = InterviewAnalysis.query.filter_by(candidate_id=candidate_id).order_by(InterviewAnalysis.created_at.desc()).first()
        previous_context = None
        if previous_analysis_record:
            traits = previous_analysis_record.behavioral_traits or {}
            risk_data = traits.get('absconding_risk', {})
            previous_context = {
                'risk_level': risk_data.get('risk_level', 'UNKNOWN'),
                'summary': previous_analysis_record.ai_summary
            }

        # Run RAG analysis
        rag_result = rag_service.analyze_risk(employee_data, anomalies, sentiment_data, previous_analysis=previous_context)
        
        # Merge RAG insights
        if rag_result:
            exit_prob = rag_result.get('exit_probability', 0)
            analysis_result['exit_probability'] = exit_prob
            
            # Determine Risk Level based on probability
            if exit_prob > 70:
                risk_level = 'HIGH'
            elif exit_prob > 30:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            analysis_result['absconding_risk'] = risk_level
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
        behavioral_traits={
            **analysis_result['behavioral_traits'],
            'absconding_risk': {
                'exit_probability': analysis_result.get('exit_probability', 0),
                'risk_level': analysis_result.get('absconding_risk', 'LOW'),
                'key_indicators': analysis_result.get('key_risk_indicators', [])
            }
        },
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
        'risk_level': ('HIGH' if (rag_result.get('exit_probability', 0) if rag_result else 0) > 70 
                      else 'MEDIUM' if (rag_result.get('exit_probability', 0) if rag_result else 0) > 30 
                      else 'LOW'),
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
