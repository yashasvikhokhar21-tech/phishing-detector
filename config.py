"""
Configuration file for Phishing Detector Application
"""

import os


class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # File upload
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB
    
    # Model
    MODEL_PATH = 'models/phishing_model.pkl'
    SCALER_PATH = 'models/scaler.pkl'
    
    # Batch prediction
    MAX_BATCH_SIZE = 100
    
    # MongoDB Atlas Configuration
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017'
    MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME') or 'phishing_detector'
    MONGODB_COLLECTION_PREDICTIONS = os.environ.get('MONGODB_COLLECTION_PREDICTIONS') or 'predictions'
    MONGODB_COLLECTION_BLACKLIST = os.environ.get('MONGODB_COLLECTION_BLACKLIST') or 'phishing_domains'
    MONGODB_COLLECTION_CONFIG = os.environ.get('MONGODB_COLLECTION_CONFIG') or 'app_config'
    
    # Use MongoDB for logging (set to True to enable)
    USE_MONGODB_LOGGING = os.environ.get('USE_MONGODB_LOGGING', 'True').lower() == 'true'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
