#!/usr/bin/env python3
"""
Simple script to run the Hex Puzzle Game backend
"""
from app import app

if __name__ == '__main__':
    print("Starting Hex Puzzle Game backend...")
    print("Open your browser to: http://localhost:5001")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5001) 