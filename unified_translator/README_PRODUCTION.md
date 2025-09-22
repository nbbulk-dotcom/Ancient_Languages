# Ancient Script Universal Translator - Production Deployment

## Quick Start

### Local Production Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python run_tests.py

# Start production server
python start_production.py
```

### Docker Production Deployment
```bash
# Build and test
./deploy_production.sh

# Run with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Monitor logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Cloud Deployment (Fly.io)
```bash
# Deploy to Fly.io
fly deploy

# Monitor deployment
fly logs
fly status
```

## System Architecture

The unified system combines:
- **GROK OCR Engine**: Enhanced image processing and glyph extraction
- **MANUS Frequency Analysis**: Brett Method harmonic calculations
- **Academic Framework**: Comprehensive documentation and citation support

## API Documentation

### Endpoints
- `POST /ocr` - Process ancient script images
- `POST /translate` - Frequency analysis using Brett Method
- `POST /narrative` - Generate cultural narratives
- `POST /validate` - Validate frequency patterns
- `GET /health` - System health check

### Frontend Features
- Multi-script support (Linear A, Khitan, Proto-Elamite, Indus Valley)
- Real-time OCR processing
- Interactive frequency visualization
- Academic documentation integration
- Multi-language narrative generation

## Monitoring and Maintenance

### Health Checks
```bash
# Check system health
curl http://localhost:8000/health

# Run comprehensive tests
python health_check.py
```

### Logs and Monitoring
- Application logs: `/tmp/ancient_translator.log`
- Docker logs: `docker logs <container_id>`
- System metrics: Available via monitoring endpoints

## Academic Usage

### Citation
```
Brett, N. (2025). "Frequency-Based Decipherment of Ancient Scripts via Symbolic Resonance." 
International Plebeian Tribunal Academy. 
Available at: https://github.com/nbbulk-dotcom/Ancient_Languages
```

### License
- Academic use: Freely permitted with attribution
- Commercial use: Requires written consent
- Research collaboration: Contact tribunal@plebeian.academy

## Support

- **GitHub**: https://github.com/nbbulk-dotcom/Ancient_Languages
- **Documentation**: See DEPLOYMENT_GUIDE.md
- **Issues**: Create GitHub issues for bugs or feature requests
- **Academic Inquiries**: tribunal@plebeian.academy

---

**Version**: 1.0.0  
**System**: Unified MANUS & GROK  
**Methodology**: Brett Method - Frequency-Based Analysis
