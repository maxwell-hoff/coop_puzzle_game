#!/bin/bash

# Start the Hex Puzzle Game backend server
echo "Starting Hex Puzzle Game backend..."

# Activate virtual environment
source venv/bin/activate

# Check if port 5000 is already in use
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
    echo "Port 5001 is already in use. Stopping existing process..."
    lsof -ti:5001 | xargs kill -9
fi

# Start the Flask application
echo "Starting Flask server on http://localhost:5001"
echo "Press Ctrl+C to stop the server"
python run.py 