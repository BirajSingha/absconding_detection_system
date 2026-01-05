from app import db
from datetime import datetime
import json

class Candidate(db.Model):
    """Candidate model for tracking interview analysis"""
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(20))
    position_applied = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    interview_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='PENDING')  # PENDING, INTERVIEWED, HIRED, REJECTED
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    analyses = db.relationship('InterviewAnalysis', backref='candidate', lazy=True, cascade='all, delete-orphan')
    transcripts = db.relationship('TranscriptSegment', backref='candidate', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        # Get latest analysis for fit score
        latest_analysis = None
        if self.analyses:
            latest_analysis = max(self.analyses, key=lambda a: a.created_at)
            
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'position_applied': self.position_applied,
            'department': self.department,
            'interview_date': self.interview_date.isoformat(),
            'status': self.status,
            'fit_score': latest_analysis.fit_score if latest_analysis else 0,
            'fit_category': latest_analysis.fit_category if latest_analysis else 'UNKNOWN',
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Candidate {self.candidate_id}: {self.name}>'


class InterviewAnalysis(db.Model):
    """Analysis model for interview performance and fit"""
    __tablename__ = 'interview_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.String(100), db.ForeignKey('candidates.candidate_id'), nullable=False, index=True)
    
    # Fit assessment
    fit_score = db.Column(db.Float, nullable=False)
    fit_category = db.Column(db.String(50), nullable=False)  # LOW, MEDIUM, HIGH, EXCELLENT
    confidence_score = db.Column(db.Float, default=0)
    
    # AI Analysis Data
    tone_analysis = db.Column(db.JSON, default={}) # Tone scores (confidence, nervousness, etc.)
    behavioral_traits = db.Column(db.JSON, default={}) # Traits extracted (leadership, teamwork)
    
    # AI Summary
    ai_summary = db.Column(db.Text)
    recommendations = db.Column(db.JSON, default=[])
    
    # Status tracking
    status = db.Column(db.String(50), default='COMPLETED') 
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'fit_score': self.fit_score,
            'fit_category': self.fit_category,
            'confidence_score': self.confidence_score,
            'tone_analysis': self.tone_analysis,
            'behavioral_traits': self.behavioral_traits,
            'ai_summary': self.ai_summary,
            'recommendations': self.recommendations,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<InterviewAnalysis {self.id}: {self.candidate_id} - {self.fit_category}>'


class TranscriptSegment(db.Model):
    """Model for storing interview transcript segments"""
    __tablename__ = 'transcript_segments'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.String(100), db.ForeignKey('candidates.candidate_id'), nullable=False, index=True)
    
    # Segment data
    text = db.Column(db.Text, nullable=False)
    timestamp_start = db.Column(db.Float) # Seconds from start
    timestamp_end = db.Column(db.Float)
    speaker = db.Column(db.String(50), default='CANDIDATE') # CANDIDATE or INTERVIEWER
    
    # Analysis results (per segment)
    sentiment = db.Column(db.String(50), default='NEUTRAL')
    sentiment_score = db.Column(db.Float, default=0)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'text': self.text,
            'timestamp_start': self.timestamp_start,
            'timestamp_end': self.timestamp_end,
            'speaker': self.speaker,
            'sentiment': self.sentiment,
            'sentiment_score': self.sentiment_score,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<TranscriptSegment {self.id}: {self.candidate_id}>'
