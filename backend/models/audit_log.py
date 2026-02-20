"""
Audit Log Model
Tracks all system actions for security monitoring
"""

from datetime import datetime, timedelta
from database import db
from bson.objectid import ObjectId

class AuditLog:
    """Audit log model for tracking system actions"""
    
    COLLECTION = 'audit_logs'
    
    # Action types
    ACTION_LOGIN = 'login'
    ACTION_LOGOUT = 'logout'
    ACTION_FAILED_LOGIN = 'failed_login'
    ACTION_REGISTER = 'register'
    ACTION_APPROVE_USER = 'approve_user'
    ACTION_REJECT_USER = 'reject_user'
    ACTION_CREATE_CASE = 'create_case'
    ACTION_UPDATE_CASE = 'update_case'
    ACTION_GENERATE_REPORT = 'generate_report'
    ACTION_DOWNLOAD_REPORT = 'download_report'
    ACTION_DATA_SCRAPE = 'data_scrape'
    ACTION_ANALYSIS = 'analysis'
    
    @staticmethod
    def log(user_id, action, details=None, ip_address=None):
        """Create an audit log entry"""
        collection = db.get_collection(AuditLog.COLLECTION)
        
        log_data = {
            'user_id': user_id,
            'action': action,
            'details': details or {},
            'ip_address': ip_address,
            'timestamp': datetime.utcnow()
        }
        
        collection.insert_one(log_data)
    
    @staticmethod
    def get_user_logs(user_id, limit=100):
        """Get audit logs for a specific user"""
        collection = db.get_collection(AuditLog.COLLECTION)
        logs = list(collection.find({'user_id': user_id}).sort('timestamp', -1).limit(limit))
        for log in logs:
            log['_id'] = str(log['_id'])
        return logs
    
    @staticmethod
    def get_recent_logs(limit=100):
        """Get recent audit logs (admin only)"""
        collection = db.get_collection(AuditLog.COLLECTION)
        logs = list(collection.find({}).sort('timestamp', -1).limit(limit))
        for log in logs:
            log['_id'] = str(log['_id'])
        return logs
    
    @staticmethod
    def get_failed_login_attempts(email, minutes=30):
        """Get failed login attempts in last N minutes"""
        collection = db.get_collection(AuditLog.COLLECTION)
        since = datetime.utcnow() - timedelta(minutes=minutes)
        count = collection.count_documents({
            'action': AuditLog.ACTION_FAILED_LOGIN,
            'details.email': email,
            'timestamp': {'$gte': since}
        })
        return count
