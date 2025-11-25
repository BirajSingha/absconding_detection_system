import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackService:
    """Service for sending notifications to Slack"""
    
    def __init__(self):
        self.token = os.getenv('SLACK_BOT_TOKEN')
        self.channel_id = os.getenv('SLACK_CHANNEL_ID')
        self.client = WebClient(token=self.token) if self.token else None
        
        if not self.token:
            print("⚠️  SlackService: SLACK_BOT_TOKEN not found. Notifications will be logged to console only.")
    
    def send_alert(self, message, blocks=None):
        """
        Send an alert message to the configured Slack channel.
        """
        if not self.client or not self.channel_id:
            print(f"\n[MOCK SLACK NOTIFICATION]\nChannel: {self.channel_id or 'Not Configured'}\nMessage: {message}\n")
            return False
            
        try:
            self.client.chat_postMessage(
                channel=self.channel_id,
                text=message,
                blocks=blocks
            )
            return True
        except SlackApiError as e:
            print(f"Error sending Slack message: {e.response['error']}")
            return False

    def send_high_risk_alert(self, employee, risk_score, risk_level, anomalies, sentiment_data):
        """
        Format and send a high risk alert.
        """
        header_text = f"🚨 High Risk Alert: {employee.name} ({employee.role})"
        
        # Format anomalies for display
        anomaly_text = ""
        for a in anomalies:
            anomaly_text += f"• {a.get('description', 'Unknown anomaly')}\n"
            
        sentiment_text = "Neutral"
        if sentiment_data:
            sentiment_text = f"{sentiment_data.get('overall_sentiment')} (Exit Intent: {sentiment_data.get('exit_intent_score')}%)"
            
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": header_text
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Risk Level:*\n{risk_level}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Risk Score:*\n{risk_score}/100"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Department:*\n{employee.department}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Tenure:*\n{employee.tenure_years} years"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Detected Anomalies:*\n{anomaly_text}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Sentiment Analysis:*\n{sentiment_text}"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "⚠️ This is an automated alert from the Absconding Detection System."
                    }
                ]
            }
        ]
        
        return self.send_alert(header_text, blocks=blocks)

# Singleton instance
_slack_service_instance = None

def get_slack_service() -> SlackService:
    """Get SlackService singleton instance"""
    global _slack_service_instance
    if _slack_service_instance is None:
        _slack_service_instance = SlackService()
    return _slack_service_instance
