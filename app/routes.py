# app/routes.py

from flask import Blueprint, render_template, request, jsonify
from app.analyzer.stock_analyzer import create_stock_visualization
import traceback

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        ticker = data.get('ticker', '').upper()
        end_date = data.get('endDate')
        lookback_days = int(data.get('lookbackDays', 365))
        crossover_days = int(data.get('crossoverDays', 180))

        if not end_date:
            end_date = None

        # Create visualization
        fig = create_stock_visualization(
            ticker=ticker,
            end_date=end_date,
            lookback_days=lookback_days,
            crossover_days=crossover_days
        )

        # Convert to HTML
        html_content = fig.to_html(
            full_html=True,
            include_plotlyjs=True,
            config={'responsive': True}
        )

        return jsonify({'success': True, 'html': html_content})

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500