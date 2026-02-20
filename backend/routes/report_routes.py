"""
Report Routes
Forensic report generation and download endpoints
"""

from flask import Blueprint, request, jsonify, send_file
from middleware.auth import investigator_required
from middleware.validation import validate_request
from models.case import Case
from models.report import Report
from models.audit_log import AuditLog
from services.report_service import ReportService
import os

report_bp = Blueprint('report', __name__)

@report_bp.route('/generate', methods=['POST'])
@investigator_required
@validate_request('case_id', 'encryption_password')
def generate_report():
    """Generate encrypted forensic PDF report"""
    try:
        data = request.get_json()
        case_id = data['case_id']
        encryption_password = data['encryption_password']
        
        case = Case.find_by_id(case_id)
        
        if not case:
            return jsonify({'error': 'Case not found'}), 404
        
        # Verify ownership (unless admin)
        if request.current_user['role'] != 'admin':
            if case['investigator_id'] != request.current_user['_id']:
                return jsonify({'error': 'Unauthorized access'}), 403
        
        # Check if data is collected
        if not case.get('data_collected'):
            return jsonify({'error': 'No data collected yet. Please scrape data first.'}), 400
        
        # Generate report
        report_service = ReportService()
        report_data = report_service.generate_pdf_report(case, encryption_password)
        
        # Save report record
        report_id = Report.create(
            case_id=case_id,
            investigator_id=request.current_user['_id'],
            file_path=report_data['file_path'],
            file_hash=report_data['file_hash'],
            encryption_hash=report_data['encryption_hash']
        )
        
        # Log action
        AuditLog.log(
            user_id=request.current_user['_id'],
            action=AuditLog.ACTION_GENERATE_REPORT,
            details={'case_id': case_id, 'report_id': report_id},
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Report generated successfully',
            'report_id': report_id,
            'file_hash': report_data['file_hash']
        }), 201
        
    except Exception as e:
        print(f"Report generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@report_bp.route('/<report_id>/download', methods=['POST'])
@investigator_required
@validate_request('decryption_password')
def download_report(report_id):
    """Download encrypted report (requires password verification)"""
    try:
        data = request.get_json()
        decryption_password = data['decryption_password']
        
        report = Report.find_by_id(report_id)
        
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        
        # Verify ownership
        if report['investigator_id'] != request.current_user['_id']:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        # Verify password (hash comparison)
        from utils.hash_utils import verify_password_hash
        if not verify_password_hash(decryption_password, report['encryption_hash']):
            return jsonify({'error': 'Invalid decryption password'}), 403
        
        # Check if file exists
        if not os.path.exists(report['file_path']):
            return jsonify({'error': 'Report file not found'}), 404
        
        # Increment download count
        Report.increment_download_count(report_id)
        
        # Log action
        AuditLog.log(
            user_id=request.current_user['_id'],
            action=AuditLog.ACTION_DOWNLOAD_REPORT,
            details={'report_id': report_id},
            ip_address=request.remote_addr
        )
        
        return send_file(
            report['file_path'],
            as_attachment=True,
            download_name=f"forensic_report_{report_id}.pdf"
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@report_bp.route('/case/<case_id>', methods=['GET'])
@investigator_required
def get_case_reports(case_id):
    """Get all reports for a case"""
    try:
        case = Case.find_by_id(case_id)
        
        if not case:
            return jsonify({'error': 'Case not found'}), 404
        
        # Verify ownership
        if case['investigator_id'] != request.current_user['_id']:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        reports = Report.find_by_case(case_id)
        
        # Remove file paths for security
        for report in reports:
            report.pop('file_path', None)
        
        return jsonify({
            'reports': reports,
            'count': len(reports)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
