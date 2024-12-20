from flask import Flask
from flask.logging import create_logger
import logging

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    app.logger = create_logger(app)
    
    # Set configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['JSON_SORT_KEYS'] = False  # Preserve JSON key order
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app