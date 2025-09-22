#!/usr/bin/env python3
"""
Production monitoring and logging for Ancient Script Universal Translator
"""

import logging
import time
import json
from datetime import datetime
from typing import Dict, Any
import psutil
import os

class SystemMonitor:
    """Monitor system resources and application health"""
    
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
        
    def log_request(self, endpoint: str, duration: float, status: str):
        """Log API request metrics"""
        self.request_count += 1
        if status == "error":
            self.error_count += 1
            
        logging.info(f"API_REQUEST: {endpoint} | Duration: {duration:.3f}s | Status: {status}")
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        return {
            "uptime_seconds": time.time() - self.start_time,
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.request_count, 1),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        metrics = self.get_system_metrics()
        
        health_issues = []
        if metrics["cpu_percent"] > 90:
            health_issues.append("High CPU usage")
        if metrics["memory_percent"] > 90:
            health_issues.append("High memory usage")
        if metrics["error_rate"] > 0.1:
            health_issues.append("High error rate")
            
        status = "healthy" if not health_issues else "degraded"
        
        return {
            "status": status,
            "issues": health_issues,
            "metrics": metrics
        }

monitor = SystemMonitor()

def setup_logging():
    """Setup production logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('/tmp/ancient_translator.log') if os.access('/tmp', os.W_OK) else logging.NullHandler()
        ]
    )
