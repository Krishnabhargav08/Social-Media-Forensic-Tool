"""
Configuration settings for the application
Handles environment variables and security settings
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)  # Increased for development
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # MongoDB settings
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/forensic_tool')
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    REPORT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reports')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Social Media API Keys (Optional - falls back to simulated mode if not set)
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', None)
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET', None)
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', None)
    TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET', None)
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', None)
    
    INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN', None)
    INSTAGRAM_CLIENT_ID = os.getenv('INSTAGRAM_CLIENT_ID', None)
    INSTAGRAM_CLIENT_SECRET = os.getenv('INSTAGRAM_CLIENT_SECRET', None)
    
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', None)
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', None)
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'ForensicTool/1.0')
    
    # AI Analysis API Keys (Optional - falls back to basic analysis if not set)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', None)
    USE_ADVANCED_AI = os.getenv('USE_ADVANCED_AI', 'False') == 'True'
    
    # Feature Flags
    USE_REAL_SCRAPING = os.getenv('USE_REAL_SCRAPING', 'False') == 'True'
    
    # Security settings
    BCRYPT_LOG_ROUNDS = 12
    MAX_LOGIN_ATTEMPTS = 5
    ACCOUNT_LOCK_DURATION = timedelta(minutes=30)
    
    # Email settings (for alerts)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@forensictool.com')
    
    # Encryption settings
    ENCRYPTION_ALGORITHM = 'AES-256'
    HASH_ALGORITHM = 'SHA-256'
    
    # API rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "100 per hour"
