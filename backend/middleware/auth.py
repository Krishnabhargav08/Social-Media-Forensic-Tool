"""
JWT Authentication Middleware
Protects routes and validates JWT tokens
"""

from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models.user import User

def jwt_required_custom(fn):
    """Custom JWT required decorator with user validation"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            # Verify user exists and is approved
            user = User.find_by_id(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 401
            
            if user['status'] != User.STATUS_APPROVED:
                return jsonify({'error': 'Account not approved'}), 403
            
            if user.get('account_locked'):
                return jsonify({'error': 'Account is locked'}), 403
            
            # Attach user to request context
            request.current_user = user
            return fn(*args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': 'Invalid or expired token'}), 401
    
    return wrapper

def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            user = User.find_by_id(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 401
            
            if user['role'] != User.ROLE_ADMIN:
                return jsonify({'error': 'Admin access required'}), 403
            
            request.current_user = user
            return fn(*args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': 'Unauthorized'}), 401
    
    return wrapper

def investigator_required(fn):
    """Decorator to require investigator role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            user = User.find_by_id(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 401
            
            if user['role'] != User.ROLE_INVESTIGATOR:
                return jsonify({'error': 'Investigator access required'}), 403
            
            if user['status'] != User.STATUS_APPROVED:
                return jsonify({'error': 'Account not approved'}), 403
            
            request.current_user = user
            return fn(*args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': 'Unauthorized'}), 401
    
    return wrapper
