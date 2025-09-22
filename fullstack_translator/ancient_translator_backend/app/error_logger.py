import logging
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class ErrorLogger:
    def __init__(self, log_file_path: str = "error_log.json"):
        self.log_file_path = Path(log_file_path)
        self.cache_file_path = Path("error_cache.json")
        self.setup_logging()
        
    def setup_logging(self):
        """Initialize logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('system.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def log_error(self, error_type: str, error_message: str, context: Dict[str, Any] = None, severity: str = "ERROR"):
        """Log an error with timestamp and context"""
        timestamp = datetime.utcnow().isoformat()
        
        error_entry = {
            "timestamp": timestamp,
            "error_type": error_type,
            "error_message": error_message,
            "severity": severity,
            "context": context or {},
            "status": "UNRESOLVED",
            "resolution_notes": None,
            "resolved_timestamp": None
        }
        
        self._add_to_cache(error_entry)
        
        self._add_to_log(error_entry)
        
        self.logger.error(f"[{error_type}] {error_message} | Context: {context}")
        
        return error_entry
        
    def log_ocr_error(self, script_type: str, error_message: str, image_info: Dict[str, Any] = None):
        """Specialized OCR error logging"""
        context = {
            "script_type": script_type,
            "image_info": image_info or {},
            "component": "OCR_CONVERSION"
        }
        return self.log_error("OCR_ERROR", error_message, context)
        
    def log_deployment_error(self, service: str, error_message: str, deployment_info: Dict[str, Any] = None):
        """Specialized deployment error logging"""
        context = {
            "service": service,
            "deployment_info": deployment_info or {},
            "component": "DEPLOYMENT"
        }
        return self.log_error("DEPLOYMENT_ERROR", error_message, context)
        
    def log_frontend_error(self, component: str, error_message: str, user_action: str = None):
        """Specialized frontend error logging"""
        context = {
            "component": component,
            "user_action": user_action,
            "frontend_component": "UI"
        }
        return self.log_error("FRONTEND_ERROR", error_message, context)
        
    def resolve_error(self, error_id: str, resolution_notes: str):
        """Mark an error as resolved and move from cache to permanent log"""
        cache_data = self._load_cache()
        
        for error in cache_data:
            if error.get("timestamp") == error_id:
                error["status"] = "RESOLVED"
                error["resolution_notes"] = resolution_notes
                error["resolved_timestamp"] = datetime.utcnow().isoformat()
                
                self._update_log_entry(error)
                
                cache_data.remove(error)
                self._save_cache(cache_data)
                
                self.logger.info(f"Error resolved: {error_id} | Resolution: {resolution_notes}")
                return True
                
        return False
        
    def get_unresolved_errors(self) -> list:
        """Get all unresolved errors from cache"""
        return self._load_cache()
        
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors by type and severity"""
        cache_data = self._load_cache()
        log_data = self._load_log()
        
        summary = {
            "total_unresolved": len(cache_data),
            "total_logged": len(log_data),
            "by_type": {},
            "by_severity": {},
            "recent_errors": cache_data[-5:] if cache_data else []
        }
        
        for error in cache_data:
            error_type = error.get("error_type", "UNKNOWN")
            severity = error.get("severity", "UNKNOWN")
            
            summary["by_type"][error_type] = summary["by_type"].get(error_type, 0) + 1
            summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1
            
        return summary
        
    def clear_resolved_cache(self):
        """Clear cache of resolved errors only"""
        cache_data = self._load_cache()
        unresolved = [error for error in cache_data if error.get("status") != "RESOLVED"]
        self._save_cache(unresolved)
        
        resolved_count = len(cache_data) - len(unresolved)
        self.logger.info(f"Cleared {resolved_count} resolved errors from cache")
        
    def export_error_report(self, output_file: str = "error_report.json"):
        """Export comprehensive error report"""
        summary = self.get_error_summary()
        log_data = self._load_log()
        
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "summary": summary,
            "all_errors": log_data,
            "unresolved_errors": self._load_cache()
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        self.logger.info(f"Error report exported to {output_file}")
        return output_file
        
    def _add_to_cache(self, error_entry: Dict[str, Any]):
        """Add error to cache file"""
        cache_data = self._load_cache()
        cache_data.append(error_entry)
        self._save_cache(cache_data)
        
    def _add_to_log(self, error_entry: Dict[str, Any]):
        """Add error to permanent log file"""
        log_data = self._load_log()
        log_data.append(error_entry)
        self._save_log(log_data)
        
    def _load_cache(self) -> list:
        """Load cache file"""
        if self.cache_file_path.exists():
            try:
                with open(self.cache_file_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
        
    def _save_cache(self, data: list):
        """Save cache file"""
        with open(self.cache_file_path, 'w') as f:
            json.dump(data, f, indent=2)
            
    def _load_log(self) -> list:
        """Load permanent log file"""
        if self.log_file_path.exists():
            try:
                with open(self.log_file_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
        
    def _save_log(self, data: list):
        """Save permanent log file"""
        with open(self.log_file_path, 'w') as f:
            json.dump(data, f, indent=2)
            
    def _update_log_entry(self, updated_error: Dict[str, Any]):
        """Update an entry in the permanent log"""
        log_data = self._load_log()
        
        for i, error in enumerate(log_data):
            if error.get("timestamp") == updated_error.get("timestamp"):
                log_data[i] = updated_error
                break
                
        self._save_log(log_data)

error_logger = ErrorLogger()
