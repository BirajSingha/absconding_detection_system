from app import db
from datetime import datetime
import json

class Employee(db.Model):
    """Employee model for tracking absconding risk"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    tenure_years = db.Column(db.Float, default=0)
    manager_id = db.Column(db.String(100))
    manager_name = db.Column(db.String(255))
    employment_status = db.Column(db.String(50), default='ACTIVE')  # ACTIVE, ON_LEAVE, INACTIVE
    
    # Performance metrics
    productivity_score = db.Column(db.Float, default=100)
    attendance_percentage = db.Column(db.Float, default=100)
    performance_rating = db.Column(db.Float, default=3.0)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    alerts = db.relationship('Alert', backref='employee', lazy=True, cascade='all, delete-orphan')
    communications = db.relationship('Communication', backref='employee', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'department': self.department,
            'tenure_years': self.tenure_years,
            'manager_id': self.manager_id,
            'manager_name': self.manager_name,
            'employment_status': self.employment_status,
            'productivity_score': self.productivity_score,
            'attendance_percentage': self.attendance_percentage,
            'performance_rating': self.performance_rating,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Employee {self.employee_id}: {self.name}>'


class Alert(db.Model):
    """Alert model for tracking absconding risk alerts"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(100), db.ForeignKey('employees.employee_id'), nullable=False, index=True)
    
    # Risk assessment
    risk_score = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(50), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    confidence_score = db.Column(db.Float, default=0)
    
    # Behavioral data
    behavioral_indicators = db.Column(db.JSON, default={})
    sentiment_indicators = db.Column(db.JSON, default={})
    
    # AI insights
    ai_summary = db.Column(db.Text)
    timeline_estimate = db.Column(db.String(255))
    recommendations = db.Column(db.JSON, default=[])
    
    # Status tracking
    status = db.Column(db.String(50), default='OPEN')  # OPEN, ACKNOWLEDGED, IN_PROGRESS, RESOLVED
    reviewed_by = db.Column(db.String(255))
    reviewed_at = db.Column(db.DateTime)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'risk_score': self.risk_score,
            'risk_level': self.risk_level,
            'confidence_score': self.confidence_score,
            'behavioral_indicators': self.behavioral_indicators,
            'sentiment_indicators': self.sentiment_indicators,
            'ai_summary': self.ai_summary,
            'timeline_estimate': self.timeline_estimate,
            'recommendations': self.recommendations,
            'status': self.status,
            'reviewed_by': self.reviewed_by,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Alert {self.id}: {self.employee_id} - {self.risk_level}>'


class Communication(db.Model):
    """Communication model for storing employee communications"""
    __tablename__ = 'communications'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(100), db.ForeignKey('employees.employee_id'), nullable=False, index=True)
    
    # Communication data
    text = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(100))  # email, slack, teams, etc.
    message_id = db.Column(db.String(255), unique=True)
    
    # Analysis results
    sentiment = db.Column(db.String(50), default='NEUTRAL')  # POSITIVE, NEUTRAL, NEGATIVE
    sentiment_score = db.Column(db.Float, default=0)
    keywords = db.Column(db.JSON, default=[])
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'text': self.text,
            'source': self.source,
            'message_id': self.message_id,
            'sentiment': self.sentiment,
            'sentiment_score': self.sentiment_score,
            'keywords': self.keywords,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Communication {self.id}: {self.employee_id}>'
