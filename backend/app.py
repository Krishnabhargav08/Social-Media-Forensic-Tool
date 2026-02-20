"""
Social Media Forensic Tool - Main Flask Application
A secure forensic investigation platform for verified officials
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import db
import os

# Import routes
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.case_routes import case_bp
from routes.report_routes import report_bp
from routes.admin_routes import admin_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Enable CORS for frontend
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize database connection
    db.init_app(app)
    
    # Create upload directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(case_bp, url_prefix='/api/cases')
    app.register_blueprint(report_bp, url_prefix='/api/reports')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'online',
            'message': 'Social Media Forensic Tool API is running',
            'version': '1.0.0'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
