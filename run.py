"""Main entry point for running the TilbudsFinder web application."""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from web_interface.app import app

if __name__ == '__main__':
    print("Starting TilbudsFinder application...")
    print("Server will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
