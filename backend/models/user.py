"""
User Model
Handles user data structure and database operations
"""

from datetime import datetime
from database import db
from bson.objectid import ObjectId
import bcrypt

class User:
    """User model for authentication and authorization"""
    
    COLLECTION = 'users'
    
    # User roles
    ROLE_ADMIN = 'admin'
    ROLE_INVESTIGATOR = 'investigator'
    
    # User status
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_SUSPENDED = 'suspended'
    
    @staticmethod
    def create(email, password, full_name, badge_number, department, role='investigator', proof_document=None):
        """Create a new user"""
        collection = db.get_collection(User.COLLECTION)
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
        
        user_data = {
            'email': email.lower(),
            'password': hashed_password,
            'full_name': full_name,
            'badge_number': badge_number,
            'department': department,
            'role': role,
            'status': User.STATUS_PENDING if role == User.ROLE_INVESTIGATOR else User.STATUS_APPROVED,
            'proof_document': proof_document,  # Store base64 encoded document
            'login_attempts': 0,
            'account_locked': False,
            'locked_until': None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'last_login': None
        }
        
        result = collection.insert_one(user_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        collection = db.get_collection(User.COLLECTION)
        user = collection.find_one({'email': email.lower()})
        if user:
            user['_id'] = str(user['_id'])
        return user
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        collection = db.get_collection(User.COLLECTION)
        user = collection.find_one({'_id': ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
        return user
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify password hash"""
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)
    
    @staticmethod
    def update_login_attempts(user_id, attempts, locked=False, locked_until=None):
        """Update login attempts and lock status"""
        collection = db.get_collection(User.COLLECTION)
        update_data = {
            'login_attempts': attempts,
            'account_locked': locked,
            'updated_at': datetime.utcnow()
        }
        if locked_until:
            update_data['locked_until'] = locked_until
        
        collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
    
    @staticmethod
    def update_last_login(user_id):
        """Update last login timestamp"""
        collection = db.get_collection(User.COLLECTION)
        collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {
                'last_login': datetime.utcnow(),
                'login_attempts': 0,
                'account_locked': False
            }}
        )
    
    @staticmethod
    def update_status(user_id, status):
        """Update user approval status"""
        collection = db.get_collection(User.COLLECTION)
        # Update both status fields for compatibility
        update_data = {
            'status': status,
            'updated_at': datetime.utcnow()
        }
        # Also update is_approved for older records
        if status == User.STATUS_APPROVED:
            update_data['is_approved'] = True
        elif status == User.STATUS_PENDING:
            update_data['is_approved'] = False
        
        collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
    
    @staticmethod
    def get_all_pending():
        """Get all pending users for admin approval"""
        collection = db.get_collection(User.COLLECTION)
        # Handle both old (is_approved) and new (status) formats
        users = list(collection.find({
            '$or': [
                {'status': User.STATUS_PENDING},
                {'is_approved': False}
            ]
        }))
        for user in users:
            user['_id'] = str(user['_id'])
        return users
    
    @staticmethod
    def get_all_users():
        """Get all users (admin only)"""
        collection = db.get_collection(User.COLLECTION)
        users = list(collection.find({}))
        for user in users:
            user['_id'] = str(user['_id'])
        return users
