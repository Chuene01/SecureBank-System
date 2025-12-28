#!/bin/bash
# Install dependencies if needed
pip install -r requirements.txt

# Run database migrations if you have them
# alembic upgrade head

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port $PORT