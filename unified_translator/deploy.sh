#!/bin/bash


echo "🏛️ Deploying Ancient Script Universal Translator - Unified System"
echo "=================================================="

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "📁 Creating necessary directories..."
mkdir -p temp logs output

echo "🔨 Building and starting unified services..."
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 30

echo "🏥 Performing health checks..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend service is healthy"
else
    echo "❌ Backend service health check failed"
    docker-compose logs unified-backend
    exit 1
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend service is healthy"
else
    echo "⚠️ Frontend service may still be starting..."
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo "=================================================="
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 API Documentation: http://localhost:8000/docs"
echo "❤️ Health Check: http://localhost:8000/health"
echo ""
echo "🔍 Available endpoints:"
echo "  POST /ocr - Extract glyphs using GROK OCR"
echo "  POST /translate - Frequency analysis using MANUS"
echo "  POST /narrative - Generate cultural narrative"
echo "  POST /validate - Validate using Brett Method"
echo ""
echo "📝 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
