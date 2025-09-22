#!/bin/bash


set -e

echo "🏺 Ancient Script Universal Translator - Production Deployment"
echo "=============================================================="

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if [ ! -f "main.py" ] || [ ! -f "Dockerfile" ]; then
    echo "❌ Please run this script from the unified_translator directory"
    exit 1
fi

echo "📋 Pre-deployment checks..."

echo "🔍 Testing Python dependencies..."
python3 -c "import fastapi, uvicorn, cv2, pytesseract, easyocr, numpy" || {
    echo "❌ Missing Python dependencies. Installing..."
    pip install -r requirements.txt
}

echo "🔍 Testing OCR functionality..."
python3 -c "
import pytesseract
import cv2
import numpy as np
print('✅ OCR libraries working')
"

echo "🐳 Building Docker image..."
docker build -t ancient-script-translator:latest .

echo "🧪 Testing Docker image..."
docker run --rm -d --name test-translator -p 8001:8000 ancient-script-translator:latest

sleep 10

echo "🏥 Testing health endpoint..."
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    docker logs test-translator
    docker stop test-translator
    exit 1
fi

docker stop test-translator

echo "✅ All tests passed!"
echo ""
echo "🚀 Ready for deployment!"
echo ""
echo "Deployment options:"
echo "1. Local: docker run -p 8000:8000 ancient-script-translator:latest"
echo "2. Fly.io: fly deploy"
echo "3. Cloud: Use the Docker image ancient-script-translator:latest"
echo ""
echo "📊 System Features:"
echo "   • OCR processing for ancient scripts"
echo "   • Brett Method frequency analysis"
echo "   • Multi-language narrative generation"
echo "   • Academic documentation integration"
echo "   • Production-ready Docker deployment"
echo ""
echo "🎓 Academic Use: https://github.com/nbbulk-dotcom/Ancient_Languages"
echo "📧 Contact: tribunal@plebeian.academy"
