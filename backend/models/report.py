"""
Report Model
Handles forensic report generation and storage
"""

from datetime import datetime
from database import db
from bson.objectid import ObjectId

class Report:
    """Report model for forensic investigation reports"""
    
    COLLECTION = 'reports'
    
    @staticmethod
    def create(case_id, investigator_id, file_path, file_hash, encryption_hash):
        """Create a new report record"""
        collection = db.get_collection(Report.COLLECTION)
        
        report_data = {
            'case_id': case_id,
            'investigator_id': investigator_id,
            'file_path': file_path,
            'file_hash': file_hash,
            'encryption_hash': encryption_hash,
            'is_encrypted': True,
            'download_count': 0,
            'created_at': datetime.utcnow(),
            'last_accessed': None
        }
        
        result = collection.insert_one(report_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_id(report_id):
        """Find report by ID"""
        collection = db.get_collection(Report.COLLECTION)
        report = collection.find_one({'_id': ObjectId(report_id)})
        if report:
            report['_id'] = str(report['_id'])
        return report
    
    @staticmethod
    def find_by_case(case_id):
        """Find reports by case ID"""
        collection = db.get_collection(Report.COLLECTION)
        reports = list(collection.find({'case_id': case_id}))
        for report in reports:
            report['_id'] = str(report['_id'])
        return reports
    
    @staticmethod
    def increment_download_count(report_id):
        """Increment download counter"""
        collection = db.get_collection(Report.COLLECTION)
        collection.update_one(
            {'_id': ObjectId(report_id)},
            {
                '$inc': {'download_count': 1},
                '$set': {'last_accessed': datetime.utcnow()}
            }
        )
    
    @staticmethod
    def get_all_reports():
        """Get all reports (admin only)"""
        collection = db.get_collection(Report.COLLECTION)
        reports = list(collection.find({}))
        for report in reports:
            report['_id'] = str(report['_id'])
        return reports
