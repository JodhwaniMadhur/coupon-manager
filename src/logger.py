import logging
import os
from logging.handlers import RotatingFileHandler
from flask import has_request_context, request
from config import Config

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.method = request.method
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.method = None
            record.remote_addr = None

        return super().format(record)

def setup_logger(app):
    # Create logs directory if it doesn't exist
    if not os.path.exists(Config.LOG_DIR):
        os.makedirs(Config.LOG_DIR)

    # Set up file handler
    file_handler = RotatingFileHandler(
        os.path.join(Config.LOG_DIR, Config.LOG_FILE),
        maxBytes=Config.LOG_MAX_SIZE,
        backupCount=Config.LOG_BACKUP_COUNT
    )
    
    # Custom formatter with request information
    formatter = RequestFormatter(
        '%(asctime)s [%(levelname)s] - %(remote_addr)s - %(method)s %(url)s\n'
        '%(message)s - [in %(pathname)s:%(lineno)d]\n'
    )
    
    file_handler.setFormatter(formatter)
    file_handler.setLevel(Config.LOG_LEVEL)

    # Add handler to app logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(Config.LOG_LEVEL)

    # Also log SQLAlchemy queries in debug mode
    if app.debug:
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    app.logger.info('Logger initialized')