import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

class EmailService:
    """Service for sending email notifications"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.hr_team_emails = os.getenv('HR_TEAM_EMAILS', '').split(',')
        
        if not self.sender_email or not self.sender_password:
            print("⚠️  EmailService: Email credentials not found. Notifications will be logged to console only.")
            self.enabled = False
        else:
            self.enabled = True
            print(f"✓ EmailService: Configured with {self.sender_email}")
    
    def send_email(self, to_emails: List[str], subject: str, body_html: str, body_text: Optional[str] = None):
        """
        Send an email notification.
        
        Args:
            to_emails: List of recipient email addresses
            subject: Email subject line
            body_html: HTML content of the email
            body_text: Plain text fallback (optional)
        """
        if not self.enabled:
            print(f"\n[MOCK EMAIL NOTIFICATION]")
            print(f"To: {', '.join(to_emails)}")
            print(f"Subject: {subject}")
            print(f"Body: {body_text or body_html[:200]}...\n")
            return False
        
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = ', '.join(to_emails)
            
            # Add plain text and HTML parts
            if body_text:
                part1 = MIMEText(body_text, 'plain')
                message.attach(part1)
            
            part2 = MIMEText(body_html, 'html')
            message.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"✓ Email sent to {', '.join(to_emails)}")
            return True
            
        except Exception as e:
            print(f"✗ Error sending email: {str(e)}")
            return False
    
    def send_high_risk_alert(self, employee, risk_score, risk_level, anomalies, sentiment_data):
        """
        Format and send a high risk alert email to HR team.
        """
        subject = f"🚨 High Risk Alert: {employee.name} - {risk_level}"
        
        # Format anomalies
        anomaly_list = ""
        for a in anomalies:
            anomaly_list += f"<li>{a.get('description', 'Unknown anomaly')}</li>\n"
        
        # Format sentiment
        sentiment_info = "Neutral"
        sentiment_details = ""
        if sentiment_data:
            sentiment_info = sentiment_data.get('overall_sentiment', 'NEUTRAL')
            exit_intent = sentiment_data.get('exit_intent_score', 0)
            keywords = sentiment_data.get('exit_keywords_found', [])
            
            sentiment_details = f"""
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;"><strong>Overall Sentiment:</strong></td>
                <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;">{sentiment_info}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;"><strong>Exit Intent Score:</strong></td>
                <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;">{exit_intent}%</td>
            </tr>
            """
            if keywords:
                sentiment_details += f"""
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;"><strong>Keywords Found:</strong></td>
                    <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;">{', '.join(keywords)}</td>
                </tr>
                """
        
        # Determine badge color
        if risk_level == 'CRITICAL':
            badge_color = '#dc2626'
        elif risk_level == 'HIGH':
            badge_color = '#ef4444'
        elif risk_level == 'MEDIUM':
            badge_color = '#f59e0b'
        else:
            badge_color = '#10b981'
        
        # HTML email body
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px 10px 0 0; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 24px;">🚨 Employee Risk Alert</h1>
            </div>
            
            <div style="background: #ffffff; padding: 30px; border: 1px solid #e0e0e0; border-top: none; border-radius: 0 0 10px 10px;">
                <div style="background: {badge_color}; color: white; padding: 10px 20px; border-radius: 5px; display: inline-block; margin-bottom: 20px;">
                    <strong>{risk_level} RISK</strong>
                </div>
                
                <h2 style="color: #333; margin-top: 0;">{employee.name}</h2>
                
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;"><strong>Employee ID:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;">{employee.employee_id}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;"><strong>Role:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;">{employee.role}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;"><strong>Department:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;">{employee.department}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;"><strong>Tenure:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;">{employee.tenure_years} years</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;"><strong>Risk Score:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #e0e0e0;"><strong style="color: {badge_color};">{risk_score:.1f}/100</strong></td>
                    </tr>
                </table>
                
                <h3 style="color: #667eea; margin-bottom: 10px;">📊 Detected Anomalies</h3>
                <ul style="background: #f8f9fa; padding: 15px 15px 15px 35px; border-radius: 5px;">
                    {anomaly_list}
                </ul>
                
                <h3 style="color: #667eea; margin-bottom: 10px;">💬 Sentiment Analysis</h3>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                    {sentiment_details}
                </table>
                
                <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin-top: 20px; border-radius: 5px;">
                    <h3 style="color: #856404; margin-top: 0;">🎯 Recommended Actions</h3>
                    <ul style="margin: 10px 0; padding-left: 20px; color: #856404;">
                        <li>Schedule immediate 1-on-1 meeting with employee</li>
                        <li>Review compensation and career development opportunities</li>
                        <li>Investigate workload and work environment concerns</li>
                        <li>Document all interactions and interventions</li>
                    </ul>
                </div>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; text-align: center; color: #666; font-size: 12px;">
                    <p>This is an automated alert from the <strong>Absconding Detection System</strong></p>
                    <p>Please treat this information confidentially and take appropriate action within 24-48 hours.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text fallback
        body_text = f"""
High Risk Employee Alert
========================

Employee: {employee.name} ({employee.employee_id})
Risk Level: {risk_level}
Risk Score: {risk_score:.1f}/100

Department: {employee.department}
Role: {employee.role}
Tenure: {employee.tenure_years} years

Detected Anomalies:
{chr(10).join(['- ' + a.get('description', 'Unknown') for a in anomalies])}

Sentiment: {sentiment_info}

Recommended Actions:
- Schedule immediate 1-on-1 meeting
- Review compensation and career development
- Investigate workload concerns
- Document all interactions

---
This is an automated alert from the Absconding Detection System.
Please take appropriate action within 24-48 hours.
        """
        
        # Send to HR team
        if self.hr_team_emails and self.hr_team_emails[0]:
            return self.send_email(
                to_emails=[email.strip() for email in self.hr_team_emails if email.strip()],
                subject=subject,
                body_html=body_html,
                body_text=body_text
            )
        else:
            print("⚠️  No HR team emails configured. Email not sent.")
            print(body_text)
            return False

# Singleton instance
_email_service_instance = None

def get_email_service() -> EmailService:
    """Get EmailService singleton instance"""
    global _email_service_instance
    if _email_service_instance is None:
        _email_service_instance = EmailService()
    return _email_service_instance
