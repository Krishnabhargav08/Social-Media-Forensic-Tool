"""
Database initialization and connection management
Handles MongoDB connection using PyMongo
"""

from pymongo import MongoClient
from flask import current_app, g

class Database:
    """MongoDB database wrapper"""
    
    def __init__(self):
        self.client = None
        self.db = None
    
    def init_app(self, app):
        """Initialize database connection with Flask app"""
        app.teardown_appcontext(self.teardown)
    
    def connect(self):
        """Establish MongoDB connection"""
        if 'db' not in g:
            self.client = MongoClient(current_app.config['MONGO_URI'])
            db_name = current_app.config['MONGO_URI'].split('/')[-1]
            g.db = self.client[db_name]
        return g.db
    
    def teardown(self, exception):
        """Close database connection"""
        db = g.pop('db', None)
        if db is not None and self.client is not None:
            self.client.close()
    
    def get_collection(self, collection_name):
        """Get a specific collection from database"""
        db = self.connect()
        return db[collection_name]

# Global database instance
db = Database()
