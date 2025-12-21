#!/bin/bash

# Start FastAPI backend in the background
uvicorn backend.agents.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit frontend
streamlit run frontend/frontend.py --server.port 8501 --server.headless true
