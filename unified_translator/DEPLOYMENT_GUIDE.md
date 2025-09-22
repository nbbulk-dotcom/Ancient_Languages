# Ancient Script Universal Translator - Deployment Guide

## Overview

The Ancient Script Universal Translator is a production-ready system that combines the GROK OCR engine with the MANUS frequency analysis system, implementing the Brett Method for deciphering ancient scripts.

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │  OCR Processing │
│                 │────│                  │────│                 │
│ • Upload UI     │    │ • /ocr endpoint  │    │ • EasyOCR       │
│ • Results View  │    │ • /translate     │    │ • Tesseract     │
│ • Academic Docs │    │ • /narrative     │    │ • Image Proc.   │
└─────────────────┘    │ • /validate      │    └─────────────────┘
                       └──────────────────┘
```

## Quick Start

### Local Development

1. **Backend Setup**
```bash
cd unified_translator
pip install -r requirements.txt
python main.py
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

3. **Health Check**
```bash
python health_check.py
```

### Docker Deployment

1. **Build and Run**
```bash
./deploy_production.sh
```

2. **Manual Docker Commands**
```bash
docker build -t ancient-script-translator .
docker run -p 8000:8000 ancient-script-translator
```

### Cloud Deployment (Fly.io)

1. **Deploy to Fly.io**
```bash
fly deploy
```

2. **Monitor Deployment**
```bash
fly logs
fly status
```

## API Endpoints

### POST /ocr
Upload ancient script image for OCR processing.

**Request:**
- `file`: Image file (JPG, PNG)

**Response:**
```json
{
  "extracted_text": "RE ZA KU RO"
}
```

### POST /translate
Convert text to frequency analysis using Brett Method.

**Request:**
- `text`: Ancient script text
- `script`: Script type (LinearA, khitan, proto_elamite, indus_valley)

**Response:**
```json
{
  "frequency_vector": [
    {"glyph": "RE", "frequency": 210.42},
    {"glyph": "ZA", "frequency": 126.22}
  ]
}
```

### POST /narrative
Generate cultural narrative interpretation.

**Request:**
- `text`: Ancient script text
- `context`: Cultural context (ceremonial, administrative, religious)

**Response:**
```json
{
  "narrative": "Linear A sequence suggests Minoan ceremonial invocation..."
}
```

### POST /validate
Validate frequency patterns using harmonic mean calculation.

**Request:**
```json
[210.42, 126.22, 157.79, 99.41]
```

**Response:**
```json
{
  "mean_frequency": 157.89,
  "valid": true
}
```

## Frontend Features

- **Upload Interface**: Drag-and-drop image upload
- **Script Selection**: Choose from 4 ancient scripts
- **Real-time Processing**: Live OCR and analysis
- **Multi-language Output**: 8 supported languages
- **Academic Documentation**: Integrated citation guides
- **Responsive Design**: Mobile-friendly interface

## Production Configuration

### Environment Variables
```bash
PORT=8000
PYTHONPATH=/app
TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata
```

### Health Monitoring
- Health endpoint: `GET /health`
- Automated health checks every 30 seconds
- Docker health check integration
- Fly.io monitoring configuration

### Security Features
- Non-root Docker user
- Minimal attack surface
- Input validation
- Error handling

## Academic Usage

### Citation Format
```
Brett, N. (2025). "Frequency-Based Decipherment of Ancient Scripts via Symbolic Resonance." 
International Plebeian Tribunal Academy. 
Available at: https://github.com/nbbulk-dotcom/Ancient_Languages
```

### License
- Academic use: Freely permitted
- Commercial use: Requires written consent
- Attribution: Required for all uses

## Troubleshooting

### Common Issues

1. **OCR Not Working**
   - Check Tesseract installation
   - Verify image format support
   - Review error logs

2. **Docker Build Fails**
   - Ensure sufficient disk space
   - Check network connectivity
   - Verify Docker version

3. **Frontend Not Loading**
   - Check build process
   - Verify static file serving
   - Review browser console

### Debug Commands
```bash
# Check logs
docker logs <container_id>

# Test endpoints
curl http://localhost:8000/health

# Validate configuration
python test_unified_system.py
```

## Support

- **GitHub**: https://github.com/nbbulk-dotcom/Ancient_Languages
- **Email**: tribunal@plebeian.academy
- **Documentation**: See ACADEMIC_METHODOLOGY.md
- **License**: See COPYRIGHT_AND_LICENSE.md

---

**Version**: 1.0.0  
**Last Updated**: September 22, 2025  
**Maintainer**: Nicolas Brett, International Plebeian Tribunal Academy
