"""
Admin Routes
Admin-only endpoints for user management and system monitoring
"""

from flask import Blueprint, request, jsonify
from middleware.auth import admin_required
from models.user import User
from models.case import Case
from models.audit_log import AuditLog

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/pending-users', methods=['GET'])
@admin_required
def get_pending_users():
    """Get all pending user registrations"""
    try:
        users = User.get_all_pending()
        
        # Remove sensitive data but keep proof_document for admin review
        for user in users:
            user.pop('password', None)
            # Add flag if proof document exists
            user['has_proof'] = bool(user.get('proof_document'))
        
        return jsonify({
            'users': users,
            'count': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users"""
    try:
        users = User.get_all_users()
        
        # Remove sensitive data
        for user in users:
            user.pop('password', None)
        
        return jsonify({
            'users': users,
            'count': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/approve-user/<user_id>', methods=['POST'])
@admin_required
def approve_user(user_id):
    """Approve a pending user"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        User.update_status(user_id, User.STATUS_APPROVED)
        
        # Log action
        AuditLog.log(
            user_id=request.current_user['_id'],
            action=AuditLog.ACTION_APPROVE_USER,
            details={'approved_user_id': user_id, 'email': user['email']},
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'User approved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/reject-user/<user_id>', methods=['POST'])
@admin_required
def reject_user(user_id):
    """Reject a pending user"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        User.update_status(user_id, User.STATUS_REJECTED)
        
        # Log action
        AuditLog.log(
            user_id=request.current_user['_id'],
            action=AuditLog.ACTION_REJECT_USER,
            details={'rejected_user_id': user_id, 'email': user['email']},
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'User rejected successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/cases', methods=['GET'])
@admin_required
def get_all_cases():
    """Get all investigation cases"""
    try:
        cases = Case.get_all_cases()
        
        return jsonify({
            'cases': cases,
            'count': len(cases)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/high-risk-cases', methods=['GET'])
@admin_required
def get_high_risk_cases():
    """Get high-risk and critical cases"""
    try:
        cases = Case.get_high_risk_cases()
        
        return jsonify({
            'cases': cases,
            'count': len(cases)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/audit-logs', methods=['GET'])
@admin_required
def get_audit_logs():
    """Get recent audit logs"""
    try:
        limit = request.args.get('limit', 100, type=int)
        logs = AuditLog.get_recent_logs(limit)
        
        return jsonify({
            'logs': logs,
            'count': len(logs)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/statistics', methods=['GET'])
@admin_required
def get_statistics():
    """Get system statistics"""
    try:
        all_users = User.get_all_users()
        all_cases = Case.get_all_cases()
        high_risk_cases = Case.get_high_risk_cases()
        
        # Count pending users (handle both 'status' and 'is_approved' fields)
        pending_count = 0
        approved_count = 0
        for u in all_users:
            # Check both old and new field formats
            if u.get('status') == User.STATUS_PENDING or u.get('is_approved') == False:
                pending_count += 1
            elif u.get('status') == User.STATUS_APPROVED or u.get('is_approved') == True:
                approved_count += 1
        
        stats = {
            'total_users': len(all_users),
            'pending_users': pending_count,
            'approved_users': approved_count,
            'total_cases': len(all_cases),
            'active_cases': len([c for c in all_cases if c.get('status') == Case.STATUS_ACTIVE]),
            'completed_cases': len([c for c in all_cases if c.get('status') == Case.STATUS_COMPLETED]),
            'high_risk_cases': len(high_risk_cases),
            'critical_cases': len([c for c in high_risk_cases if c.get('risk_level') == Case.RISK_CRITICAL])
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
