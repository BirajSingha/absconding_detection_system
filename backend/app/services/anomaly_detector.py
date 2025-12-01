from datetime import datetime, timedelta
from app.models.employee import Employee, Communication
from app import db

class AnomalyDetector:
    """Detects behavioral anomalies in employee data"""
    
    def __init__(self):
        self.productivity_threshold = 30  # % drop that triggers alert
        self.attendance_threshold = 20    # % drop that triggers alert
        self.communication_threshold = 40  # % reduction in communications
    
    def detect_anomalies(self, employee_id, timeframe_days=30):
        """
        Detect behavioral anomalies for an employee.
        Returns list of detected anomalies with severity scores.
        """
        employee = Employee.query.filter_by(employee_id=employee_id).first()
        if not employee:
            return []
        
        anomalies = []
        
        # 1. Check productivity anomalies
        if employee.productivity_score < 70:
            anomalies.append({
                'type': 'productivity_drop',
                'severity': self._calculate_severity(employee.productivity_score, 100),
                'value': employee.productivity_score,
                'threshold': 70,
                'description': f'Productivity score dropped to {employee.productivity_score}% (baseline: 100%)'
            })
        
        # 2. Check attendance anomalies
        if employee.attendance_percentage < 80:
            anomalies.append({
                'type': 'attendance_issues',
                'severity': self._calculate_severity(employee.attendance_percentage, 100),
                'value': employee.attendance_percentage,
                'threshold': 80,
                'description': f'Attendance dropped to {employee.attendance_percentage}% (baseline: 100%)'
            })
        
        # 3. Check communication patterns
        comm_anomaly = self._detect_communication_anomaly(employee_id, timeframe_days)
        if comm_anomaly:
            anomalies.append(comm_anomaly)
        
        # 4. Check performance rating trend
        if employee.performance_rating < 2.5:
            anomalies.append({
                'type': 'performance_decline',
                'severity': self._calculate_severity(employee.performance_rating, 4.0),
                'value': employee.performance_rating,
                'threshold': 2.5,
                'description': f'Performance rating at {employee.performance_rating}/4.0 (expected: >3.0)'
            })
        
        # 5. Check employment status changes
        if employee.employment_status != 'ACTIVE':
            anomalies.append({
                'type': 'employment_status_change',
                'severity': 0.7,
                'value': employee.employment_status,
                'description': f'Employment status changed to {employee.employment_status}'
            })
        
        return anomalies
    
    def _calculate_severity(self, current_value, baseline_value, max_severity=1.0):
        """
        Calculate severity score (0-1) based on how far value deviates from baseline.
        """
        if baseline_value == 0:
            return 0
        
        percentage_drop = (baseline_value - current_value) / baseline_value
        severity = min(abs(percentage_drop), max_severity)
        return round(severity, 2)
    
    def _detect_communication_anomaly(self, employee_id, timeframe_days=30):
        """
        Detect changes in communication patterns.
        Returns anomaly if communication frequency drops significantly.
        """
        # Get communication history for last X days
        start_date = datetime.utcnow() - timedelta(days=timeframe_days)
        
        communications = Communication.query.filter(
            Communication.employee_id == employee_id,
            Communication.created_at >= start_date
        ).all()
        
        if len(communications) < 2:
            # Not enough data to detect pattern
            return None
        
        # Check if most recent communications are negative
        recent_comms = communications[-5:] if len(communications) >= 5 else communications
        negative_sentiment_count = sum(
            1 for comm in recent_comms 
            if comm.sentiment == 'NEGATIVE'
        )
        
        if negative_sentiment_count >= len(recent_comms) * 0.6:  # 60% negative
            return {
                'type': 'negative_sentiment_pattern',
                'severity': negative_sentiment_count / len(recent_comms),
                'value': f'{negative_sentiment_count}/{len(recent_comms)} recent messages negative',
                'description': f'{negative_sentiment_count} out of {len(recent_comms)} recent communications show negative sentiment (last {timeframe_days} days)'
            }
        
        return None
    
    def calculate_risk_score(self, anomalies):
        """
        Calculate overall risk score based on detected anomalies.
        Returns score from 0-100.
        """
        if not anomalies:
            return 0
        
        # Weight different anomaly types
        weights = {
            'productivity_drop': 0.25,
            'attendance_issues': 0.20,
            'performance_decline': 0.20,
            'negative_sentiment_pattern': 0.25,
            'employment_status_change': 0.10
        }
        
        total_weighted_score = 0
        total_weight = 0
        
        for anomaly in anomalies:
            anomaly_type = anomaly.get('type', 'unknown')
            weight = weights.get(anomaly_type, 0.1)
            severity = anomaly.get('severity', 0.5)
            
            total_weighted_score += (severity * weight * 100)
            total_weight += weight
        
        if total_weight == 0:
            return 0
        
        risk_score = min(total_weighted_score / total_weight, 100)
        return round(risk_score, 2)
    
    def detect_trend(self, employee_id, metric_name, days=30):
        """
        Detect trends in employee metrics over time.
        Returns trend direction: 'increasing', 'decreasing', or 'stable'
        """
        # This is a placeholder for trend detection
        # In a real implementation, you'd query historical data
        return 'stable'
