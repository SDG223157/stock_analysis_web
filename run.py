# run.py

import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Configuration for development server
    port = int(os.environ.get('PORT', 3000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=True
    )