# app/routes.py

import traceback
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, current_app
from app.analyzer.stock_analyzer import (
    create_stock_visualization,
    analyze_signals,
    format_analysis_summary
)
from app.config.metrics_config import ANALYSIS_DEFAULTS

# Create blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Render the main page"""
    try:
        return render_template('index.html')
    except Exception as e:
        current_app.logger.error(f"Error rendering index: {str(e)}")
        return "An error occurred", 500

@main.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze stock data and return visualization
    
    Expected JSON payload:
    {
        "ticker": "AAPL",
        "endDate": "2024-12-20",  # Optional
        "lookbackDays": 365,      # Optional
        "crossoverDays": 180      # Optional
    }
    """
    request_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
    print(f"Starting analysis request {request_id}")  # Add request ID to track
    try:
        # Get and validate request data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400

        # Extract and validate ticker
        ticker = data.get('ticker', '').upper()
        if not ticker:
            return jsonify({
                'success': False,
                'error': 'Ticker symbol is required'
            }), 400

        # Extract other parameters with defaults
        end_date = data.get('endDate')
        if not end_date:
            end_date = None
        lookback_days = int(data.get('lookbackDays', ANALYSIS_DEFAULTS['lookback_days']))
        crossover_days = int(data.get('crossoverDays', ANALYSIS_DEFAULTS['crossover_days']))

        # Validate numeric parameters
        if lookback_days < 1 or crossover_days < 1:
            return jsonify({
                'success': False,
                'error': 'Lookback and crossover days must be positive numbers'
            }), 400

        # Log analysis request
        current_app.logger.info(
            f"Analyzing {ticker} with parameters: "
            f"end_date={end_date}, "
            f"lookback_days={lookback_days}, "
            f"crossover_days={crossover_days}"
        )

        # Create visualization
        fig = create_stock_visualization(
            ticker=ticker,
            end_date=end_date,
            lookback_days=lookback_days,
            crossover_days=crossover_days
        )

        # Convert to HTML with configuration
        html_content = fig.to_html(
            full_html=True,
            include_plotlyjs=True,
            config={
                'responsive': True,
                'displayModeBar': True,
                'scrollZoom': True,
                'showLink': False,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': f'{ticker}_analysis',
                    'height': 1080,
                    'width': 1920,
                    'scale': 2
                }
            }
        )

        return jsonify({
            'success': True,
            'html': html_content,
            'timestamp': datetime.now().isoformat()
        })

    except ValueError as ve:
        # Handle validation errors
        error_msg = str(ve)
        current_app.logger.warning(f"Validation error: {error_msg}")
        return jsonify({
            'success': False,
            'error': error_msg
        }), 400

    except Exception as e:
        # Handle unexpected errors
        error_msg = str(e)
        current_app.logger.error(f"Error processing request: {error_msg}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': "An unexpected error occurred while processing your request.",
            'details': error_msg if current_app.debug else None
        }), 500

@main.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@main.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

@main.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    current_app.logger.error(f"Internal server error: {str(error)}")
    current_app.logger.error(traceback.format_exc())
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# Register before request handler
@main.before_request
def before_request():
    """Log incoming requests"""
    if not request.path == '/health':  # Skip logging health checks
        current_app.logger.info(
            f"Request: {request.method} {request.path} "
            f"from {request.remote_addr}"
        )

# Register after request handler
@main.after_request
def after_request(response):
    """Add security headers and CORS"""
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    
    return response