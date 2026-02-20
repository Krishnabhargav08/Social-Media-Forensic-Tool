"""
Authentication Routes
Handles user registration, login, and token management
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models.user import User
from models.audit_log import AuditLog
from middleware.validation import validate_request, validate_email, validate_password
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@validate_request('email', 'password', 'full_name', 'badge_number', 'department')
def register():
    """Register a new investigator (requires admin approval)"""
    try:
        data = request.get_json()
        
        # Validate email format
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        is_valid, message = validate_password(data['password'])
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Check if user already exists
        existing_user = User.find_by_email(data['email'])
        if existing_user:
            return jsonify({'error': 'User already exists'}), 409
        
        # Validate proof document if provided
        proof_document = data.get('proof_document')
        if proof_document:
            # Validate base64 format and size (limit to 5MB)
            if len(proof_document) > 7000000:  # ~5MB in base64
                return jsonify({'error': 'Proof document too large (max 5MB)'}), 400
        
        # Create user (status will be pending)
        user_id = User.create(
            email=data['email'],
            password=data['password'],
            full_name=data['full_name'],
            badge_number=data['badge_number'],
            department=data['department'],
            role='investigator',
            proof_document=proof_document
        )
        
        # Log registration
        AuditLog.log(
            user_id=user_id,
            action=AuditLog.ACTION_REGISTER,
            details={'email': data['email'], 'has_proof': bool(proof_document)},
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Registration successful. Awaiting admin approval.',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
@validate_request('email', 'password')
def login():
    """Login user and return JWT tokens"""
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        
        # Find user
        user = User.find_by_email(email)
        if not user:
            AuditLog.log(
                user_id=None,
                action=AuditLog.ACTION_FAILED_LOGIN,
                details={'email': email, 'reason': 'User not found'},
                ip_address=request.remote_addr
            )
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check if account is locked
        if user.get('account_locked'):
            if user.get('locked_until') and datetime.utcnow() > user['locked_until']:
                # Unlock account
                User.update_login_attempts(user['_id'], 0, False, None)
            else:
                return jsonify({'error': 'Account locked. Try again later.'}), 403
        
        # Verify password
        if not User.verify_password(user['password'], password):
            # Increment failed attempts
            attempts = user.get('login_attempts', 0) + 1
            locked = attempts >= 5
            locked_until = datetime.utcnow() + timedelta(minutes=30) if locked else None
            
            User.update_login_attempts(user['_id'], attempts, locked, locked_until)
            
            AuditLog.log(
                user_id=user['_id'],
                action=AuditLog.ACTION_FAILED_LOGIN,
                details={'attempts': attempts},
                ip_address=request.remote_addr
            )
            
            if locked:
                return jsonify({'error': 'Account locked due to multiple failed attempts'}), 403
            
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check user status (handle both old and new field formats)
        user_status = user.get('status')
        is_approved = user.get('is_approved')
        
        # Check if pending (either status='pending' or is_approved=False)
        if user_status == User.STATUS_PENDING or (is_approved is False and user_status is None):
            return jsonify({'error': 'Account pending approval'}), 403
        
        if user_status == User.STATUS_REJECTED:
            return jsonify({'error': 'Account rejected'}), 403
        
        if user_status == User.STATUS_SUSPENDED:
            return jsonify({'error': 'Account suspended'}), 403
        
        # Update last login and reset attempts
        User.update_last_login(user['_id'])
        
        # Create JWT tokens
        access_token = create_access_token(identity=user['_id'])
        refresh_token = create_refresh_token(identity=user['_id'])
        
        # Log successful login
        AuditLog.log(
            user_id=user['_id'],
            action=AuditLog.ACTION_LOGIN,
            details={'email': email},
            ip_address=request.remote_addr
        )
        
        # Remove sensitive data
        user.pop('password', None)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token"""
    try:
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify():
    """Verify JWT token and return user info"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Remove sensitive data
        user.pop('password', None)
        
        return jsonify({
            'valid': True,
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
