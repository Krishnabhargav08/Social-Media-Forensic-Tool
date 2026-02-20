"""
User Routes
User profile and management endpoints
"""

from flask import Blueprint, request, jsonify
from middleware.auth import jwt_required_custom
from models.user import User
from models.audit_log import AuditLog
from bson.objectid import ObjectId

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required_custom
def get_profile():
    """Get current user profile"""
    try:
        user = request.current_user
        user.pop('password', None)
        
        return jsonify({
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/profile', methods=['PUT'])
@jwt_required_custom
def update_profile():
    """Update user profile"""
    try:
        data = request.get_json()
        user_id = request.current_user['_id']
        
        # Only allow updating certain fields
        allowed_fields = ['full_name', 'department']
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if update_data:
            from database import db
            collection = db.get_collection(User.COLLECTION)
            collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )
        
        return jsonify({
            'message': 'Profile updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/activity-logs', methods=['GET'])
@jwt_required_custom
def get_activity_logs():
    """Get user's activity logs"""
    try:
        user_id = request.current_user['_id']
        limit = request.args.get('limit', 50, type=int)
        
        logs = AuditLog.get_user_logs(user_id, limit)
        
        return jsonify({
            'logs': logs,
            'count': len(logs)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
