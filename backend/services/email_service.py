"""
Email Service
Sends email alerts for high-risk cases and system notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

class EmailService:
    """Service for sending email notifications"""
    
    def __init__(self):
        self.mail_server = None
        self.mail_port = None
        self.mail_username = None
        self.mail_password = None
        self.mail_sender = None
    
    def _init_config(self):
        """Initialize email configuration from Flask app"""
        if not self.mail_server:
            self.mail_server = current_app.config.get('MAIL_SERVER')
            self.mail_port = current_app.config.get('MAIL_PORT')
            self.mail_username = current_app.config.get('MAIL_USERNAME')
            self.mail_password = current_app.config.get('MAIL_PASSWORD')
            self.mail_sender = current_app.config.get('MAIL_DEFAULT_SENDER')
    
    def send_high_risk_alert(self, case_data, admin_email):
        """Send alert for high-risk case detection"""
        self._init_config()
        
        subject = f"HIGH RISK ALERT - Case {case_data['_id']}"
        
        body = f"""
        HIGH RISK CASE DETECTED
        
        Case ID: {case_data['_id']}
        Target Username: {case_data['target_username']}
        Platform: {case_data['platform']}
        Risk Level: {case_data['risk_level'].upper()}
        Risk Score: {case_data['risk_score']}/100
        
        This case requires immediate attention.
        
        Please login to the Forensic Tool dashboard for full details.
        
        ---
        Social Media Forensic Tool
        Automated Alert System
        """
        
        return self._send_email(admin_email, subject, body)
    
    def send_user_approval_notification(self, user_email, user_name, approved=True):
        """Send notification to user about account approval status"""
        self._init_config()
        
        if approved:
            subject = "Account Approved - Social Media Forensic Tool"
            body = f"""
            Dear {user_name},
            
            Your account has been approved by the administrator.
            You can now login and access the forensic investigation platform.
            
            Login URL: http://localhost:3000/login
            
            Please ensure you maintain security best practices:
            - Keep your password secure
            - Do not share your credentials
            - Report any suspicious activity
            
            ---
            Social Media Forensic Tool
            Security Team
            """
        else:
            subject = "Account Registration - Pending Approval"
            body = f"""
            Dear {user_name},
            
            Your registration for the Social Media Forensic Tool has been received.
            
            Your account is currently pending administrator approval.
            You will receive another email once your account is reviewed.
            
            ---
            Social Media Forensic Tool
            Security Team
            """
        
        return self._send_email(user_email, subject, body)
    
    def _send_email(self, to_email, subject, body):
        """Send email using SMTP"""
        try:
            # Create message
            message = MIMEMultipart()
            message['From'] = self.mail_sender
            message['To'] = to_email
            message['Subject'] = subject
            
            message.attach(MIMEText(body, 'plain'))
            
            # Send email
            if self.mail_username and self.mail_password:
                server = smtplib.SMTP(self.mail_server, self.mail_port)
                server.starttls()
                server.login(self.mail_username, self.mail_password)
                server.send_message(message)
                server.quit()
                return True
            else:
                # If email not configured, just log it (for development)
                print(f"[EMAIL] To: {to_email} | Subject: {subject}")
                return True
                
        except Exception as e:
            print(f"[EMAIL ERROR] {str(e)}")
            return False
