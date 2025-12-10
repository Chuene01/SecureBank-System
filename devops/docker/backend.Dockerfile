# Use Python 3.11 slim image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the entire backend code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 80

# Run the FastAPI application
# The app is in main.py and the FastAPI instance is named "app"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
