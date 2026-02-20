"""
Case Routes
Investigation case management endpoints
"""

from flask import Blueprint, request, jsonify
from middleware.auth import jwt_required_custom, investigator_required
from middleware.validation import validate_request
from models.case import Case
from models.audit_log import AuditLog
from services.scraper_service import ScraperService
from services.analysis_service import AnalysisService
from utils.hash_utils import generate_evidence_hash

case_bp = Blueprint('case', __name__)

@case_bp.route('/', methods=['POST'])
@investigator_required
@validate_request('target_username', 'platform')
def create_case():
    """Create a new investigation case"""
    try:
        data = request.get_json()
        user_id = request.current_user['_id']
        
        # Create case
        case_id = Case.create(
            investigator_id=user_id,
            target_username=data['target_username'],
            platform=data['platform'],
            description=data.get('description', '')
        )
        
        # Log action
        AuditLog.log(
            user_id=user_id,
            action=AuditLog.ACTION_CREATE_CASE,
            details={
                'case_id': case_id,
                'target_username': data['target_username'],
                'platform': data['platform']
            },
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Case created successfully',
            'case_id': case_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_bp.route('/', methods=['GET'])
@investigator_required
def get_my_cases():
    """Get all cases for current investigator"""
    try:
        user_id = request.current_user['_id']
        cases = Case.find_by_investigator(user_id)
        
        return jsonify({
            'cases': cases,
            'count': len(cases)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_bp.route('/<case_id>', methods=['GET'])
@jwt_required_custom
def get_case(case_id):
    """Get case details"""
    try:
        case = Case.find_by_id(case_id)
        
        if not case:
            return jsonify({'error': 'Case not found'}), 404
        
        # Verify ownership (investigators can only see their own cases)
        if request.current_user['role'] == 'investigator':
            if case['investigator_id'] != request.current_user['_id']:
                return jsonify({'error': 'Unauthorized access'}), 403
        
        return jsonify({
            'case': case
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_bp.route('/<case_id>/scrape', methods=['POST'])
@investigator_required
def scrape_data(case_id):
    """Scrape data for a case"""
    try:
        case = Case.find_by_id(case_id)
        
        if not case:
            return jsonify({'error': 'Case not found'}), 404
        
        # Verify ownership
        if case['investigator_id'] != request.current_user['_id']:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        # Scrape data
        scraper = ScraperService()
        scraped_data = scraper.scrape_profile(
            platform=case['platform'],
            username=case['target_username']
        )
        
        # Add to case
        Case.add_collected_data(case_id, scraped_data)
        
        # Generate evidence hash
        evidence_hash = generate_evidence_hash(scraped_data)
        Case.update_evidence_hash(case_id, evidence_hash)
        
        # Log action
        AuditLog.log(
            user_id=request.current_user['_id'],
            action=AuditLog.ACTION_DATA_SCRAPE,
            details={'case_id': case_id},
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Data scraped successfully',
            'data': scraped_data,
            'evidence_hash': evidence_hash
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_bp.route('/<case_id>/analyze', methods=['POST'])
@investigator_required
def analyze_case(case_id):
    """Analyze case data for fraud and cyberbullying"""
    try:
        case = Case.find_by_id(case_id)
        
        if not case:
            return jsonify({'error': 'Case not found'}), 404
        
        # Verify ownership
        if case['investigator_id'] != request.current_user['_id']:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        # Check if data is collected
        if not case.get('data_collected'):
            return jsonify({'error': 'No data collected yet'}), 400
        
        # Perform analysis
        analyzer = AnalysisService()
        analysis_results = analyzer.analyze_all(case['data_collected'])
        
        # Calculate risk score and level
        risk_score = analysis_results['risk_score']
        risk_level = Case.RISK_LOW
        if risk_score >= 75:
            risk_level = Case.RISK_CRITICAL
        elif risk_score >= 50:
            risk_level = Case.RISK_HIGH
        elif risk_score >= 25:
            risk_level = Case.RISK_MEDIUM
        
        # Update case with analysis
        Case.update_analysis(case_id, analysis_results, risk_score, risk_level)
        
        # Log action
        AuditLog.log(
            user_id=request.current_user['_id'],
            action=AuditLog.ACTION_ANALYSIS,
            details={'case_id': case_id, 'risk_score': risk_score, 'risk_level': risk_level},
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Analysis completed',
            'analysis': analysis_results,
            'risk_score': risk_score,
            'risk_level': risk_level
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_bp.route('/<case_id>/complete', methods=['POST'])
@investigator_required
def complete_case(case_id):
    """Mark case as completed"""
    try:
        case = Case.find_by_id(case_id)
        
        if not case:
            return jsonify({'error': 'Case not found'}), 404
        
        # Verify ownership
        if case['investigator_id'] != request.current_user['_id']:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        Case.update_status(case_id, Case.STATUS_COMPLETED)
        
        # Log action
        AuditLog.log(
            user_id=request.current_user['_id'],
            action=AuditLog.ACTION_UPDATE_CASE,
            details={'case_id': case_id, 'status': 'completed'},
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Case marked as completed'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_bp.route('/<case_id>', methods=['DELETE'])
@investigator_required
def delete_case(case_id):
    """Delete a case"""
    try:
        case = Case.find_by_id(case_id)
        
        if not case:
            return jsonify({'error': 'Case not found'}), 404
        
        # Verify ownership (only case owner or admin can delete)
        if request.current_user['role'] != 'admin':
            if case['investigator_id'] != request.current_user['_id']:
                return jsonify({'error': 'Unauthorized access'}), 403
        
        # Delete the case
        Case.delete(case_id)
        
        # Log action
        AuditLog.log(
            user_id=request.current_user['_id'],
            action='DELETE_CASE',
            details={'case_id': case_id, 'target_username': case['target_username']},
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Case deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
