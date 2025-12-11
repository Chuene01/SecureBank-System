#!/bin/bash
echo " Setting up Banking App..."

if ! command -v docker &> /dev/null; then
    echo " Docker not installed"
    exit 1
fi

if [ ! -f .env ]; then
    echo " Creating .env file..."
    cat > .env << EOF
MONGODB_URL=mongodb://mongo:27017/
MONGODB_DATABASE=bankingdb
PYTHONUNBUFFERED=1
EOF
fi

echo " Building and starting containers..."
docker-compose up --build -d

sleep 10

docker-compose ps

echo ""
echo " Banking App is running!"
echo " Frontend: http://localhost:3000"
echo " Backend: http://localhost:8000"
echo " API Docs: http://localhost:8000/docs"