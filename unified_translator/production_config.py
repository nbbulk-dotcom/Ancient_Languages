#!/usr/bin/env python3
"""
Production configuration for Ancient Script Universal Translator
"""

import os
from typing import Dict, Any

class ProductionConfig:
    """Production configuration settings"""
    
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    WORKERS = int(os.getenv("WORKERS", 1))
    
    TESSERACT_CMD = os.getenv("TESSERACT_CMD", "tesseract")
    TESSDATA_PREFIX = os.getenv("TESSDATA_PREFIX", "/usr/share/tesseract-ocr/4.00/tessdata")
    
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "tiff", "bmp"}
    
    CULTURAL_MODIFIERS = {
        "LinearA": 1.26,      # Minoan ceremonial amplification
        "linear_a": 1.26,
        "khitan": 1.15,       # Liao dynasty context
        "proto_elamite": 1.08, # Administrative context
        "indus_valley": 1.33   # Vedic resonance factor
    }
    
    MIN_FREQUENCY = 50.0
    MAX_FREQUENCY = 1000.0
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "/tmp/ancient_translator.log")
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            "server": {
                "host": cls.HOST,
                "port": cls.PORT,
                "workers": cls.WORKERS
            },
            "ocr": {
                "tesseract_cmd": cls.TESSERACT_CMD,
                "tessdata_prefix": cls.TESSDATA_PREFIX
            },
            "upload": {
                "max_file_size": cls.MAX_FILE_SIZE,
                "allowed_extensions": list(cls.ALLOWED_EXTENSIONS)
            },
            "brett_method": {
                "cultural_modifiers": cls.CULTURAL_MODIFIERS,
                "frequency_range": [cls.MIN_FREQUENCY, cls.MAX_FREQUENCY]
            },
            "logging": {
                "level": cls.LOG_LEVEL,
                "file": cls.LOG_FILE
            }
        }

config = ProductionConfig()
