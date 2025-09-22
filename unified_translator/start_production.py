#!/usr/bin/env python3
"""
Production startup script for Ancient Script Universal Translator
"""

import uvicorn
import os
import sys
from production_config import config
from monitoring import setup_logging, monitor

def main():
    """Start the production server"""
    setup_logging()
    
    print("🏺 Ancient Script Universal Translator - Production Server")
    print("=" * 60)
    print(f"Version: 1.0.0")
    print(f"System: Unified MANUS & GROK")
    print(f"Methodology: Brett Method - Frequency-Based Analysis")
    print(f"Host: {config.HOST}")
    print(f"Port: {config.PORT}")
    print(f"Workers: {config.WORKERS}")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "main:app",
            host=config.HOST,
            port=config.PORT,
            workers=config.WORKERS,
            log_level=config.LOG_LEVEL.lower(),
            access_log=True,
            reload=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
