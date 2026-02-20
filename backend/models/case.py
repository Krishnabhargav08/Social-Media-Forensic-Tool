"""
Case Model
Handles investigation case data and operations
"""

from datetime import datetime
from database import db
from bson.objectid import ObjectId

class Case:
    """Case model for forensic investigations"""
    
    COLLECTION = 'cases'
    
    # Case status
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_ARCHIVED = 'archived'
    
    # Risk levels
    RISK_LOW = 'low'
    RISK_MEDIUM = 'medium'
    RISK_HIGH = 'high'
    RISK_CRITICAL = 'critical'
    
    @staticmethod
    def create(investigator_id, target_username, platform, description=''):
        """Create a new investigation case"""
        collection = db.get_collection(Case.COLLECTION)
        
        case_data = {
            'investigator_id': investigator_id,
            'target_username': target_username,
            'platform': platform,
            'description': description,
            'status': Case.STATUS_ACTIVE,
            'risk_level': Case.RISK_LOW,
            'risk_score': 0,
            'data_collected': [],
            'analysis_results': {},
            'evidence_hash': None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'completed_at': None
        }
        
        result = collection.insert_one(case_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_id(case_id):
        """Find case by ID"""
        collection = db.get_collection(Case.COLLECTION)
        case = collection.find_one({'_id': ObjectId(case_id)})
        if case:
            case['_id'] = str(case['_id'])
        return case
    
    @staticmethod
    def find_by_investigator(investigator_id):
        """Find all cases by investigator"""
        collection = db.get_collection(Case.COLLECTION)
        cases = list(collection.find({'investigator_id': investigator_id}))
        for case in cases:
            case['_id'] = str(case['_id'])
        return cases
    
    @staticmethod
    def update_analysis(case_id, analysis_data, risk_score, risk_level):
        """Update case with analysis results"""
        collection = db.get_collection(Case.COLLECTION)
        collection.update_one(
            {'_id': ObjectId(case_id)},
            {'$set': {
                'analysis_results': analysis_data,
                'risk_score': risk_score,
                'risk_level': risk_level,
                'updated_at': datetime.utcnow()
            }}
        )
    
    @staticmethod
    def add_collected_data(case_id, data_entry):
        """Add collected data to case"""
        collection = db.get_collection(Case.COLLECTION)
        collection.update_one(
            {'_id': ObjectId(case_id)},
            {
                '$push': {'data_collected': data_entry},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
    
    @staticmethod
    def update_evidence_hash(case_id, evidence_hash):
        """Update SHA-256 hash for evidence integrity"""
        collection = db.get_collection(Case.COLLECTION)
        collection.update_one(
            {'_id': ObjectId(case_id)},
            {'$set': {
                'evidence_hash': evidence_hash,
                'updated_at': datetime.utcnow()
            }}
        )
    
    @staticmethod
    def update_status(case_id, status):
        """Update case status"""
        collection = db.get_collection(Case.COLLECTION)
        update_data = {
            'status': status,
            'updated_at': datetime.utcnow()
        }
        if status == Case.STATUS_COMPLETED:
            update_data['completed_at'] = datetime.utcnow()
        
        collection.update_one(
            {'_id': ObjectId(case_id)},
            {'$set': update_data}
        )
    
    @staticmethod
    def get_all_cases():
        """Get all cases (admin only)"""
        collection = db.get_collection(Case.COLLECTION)
        cases = list(collection.find({}))
        for case in cases:
            case['_id'] = str(case['_id'])
        return cases
    
    @staticmethod
    def get_high_risk_cases():
        """Get all high-risk and critical cases"""
        collection = db.get_collection(Case.COLLECTION)
        cases = list(collection.find({
            'risk_level': {'$in': [Case.RISK_HIGH, Case.RISK_CRITICAL]}
        }))
        for case in cases:
            case['_id'] = str(case['_id'])
        return cases
