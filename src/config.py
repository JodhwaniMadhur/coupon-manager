from os import environ, path
import logging
from logging.handlers import RotatingFileHandler

class Config:
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or 'mysql://root:password@localhost/coupon_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
    
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Logging configuration
    LOG_DIR = 'logs'
    LOG_FILE = 'coupon_api.log'
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s [%(levelname)s] - %(message)s - [in %(pathname)s:%(lineno)d]'
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    