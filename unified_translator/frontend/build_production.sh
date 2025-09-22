#!/bin/bash


set -e

echo "⚛️ Building React Frontend for Production"
echo "========================================"

if [ ! -f "package.json" ]; then
    echo "❌ Please run this script from the frontend directory"
    exit 1
fi

echo "📦 Installing dependencies..."
npm install

echo "🏗️ Building for production..."
npm run build

if [ -d "build" ]; then
    echo "✅ Production build completed successfully!"
    echo "📁 Build files are in the 'build' directory"
    echo ""
    echo "📊 Build statistics:"
    du -sh build/
    echo ""
    echo "🚀 Ready for deployment!"
    echo ""
    echo "Deployment options:"
    echo "1. Static hosting: Upload 'build' folder contents"
    echo "2. Docker: Use build folder in Dockerfile"
    echo "3. CDN: Deploy build folder to CDN"
else
    echo "❌ Build failed!"
    exit 1
fi
