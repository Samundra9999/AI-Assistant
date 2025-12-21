#!/bin/bash

echo "Starting FastAPI backend..."
uvicorn backend.agents.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait 5 seconds for backend to start
sleep 5

# Check if FastAPI died
if ! kill -0 "$BACKEND_PID" > /dev/null 2>&1; then
    echo "❌ FastAPI crashed — stopping deployment!"
    exit 1
fi

echo "Backend OK. Starting Streamlit..."
streamlit run frontend/frontend.py --server.port 8501 --server.headless true
