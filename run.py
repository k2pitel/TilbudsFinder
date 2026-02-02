"""Main entry point for running the TilbudsFinder web application."""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from web_interface.app import app

if __name__ == '__main__':
    print("Starting TilbudsFinder application...")
    print("Server will be available at: http://localhost:5000")
    # Debug mode should only be enabled in development
    # Set FLASK_DEBUG=1 environment variable to enable debug mode
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
