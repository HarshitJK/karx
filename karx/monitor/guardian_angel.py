import psutil
import logging
import threading
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ResourceThresholdError(Exception):
    """Exception raised when resource usage exceeds thresholds"""
    pass

class GuardianAngel:
    def __init__(self, 
                 max_cpu_percent: float = 90.0,
                 max_memory_percent: float = 85.0,
                 check_interval: float = 1.0,
                 history_file: Optional[Path] = None):
        self.max_cpu_percent = max_cpu_percent
        self.max_memory_percent = max_memory_percent
        self.check_interval = check_interval
        self.history_file = history_file or Path("monitor/resource_history.json")
        self.snapshots: List[Dict[str, float]] = self._load_history()
        self.lock = threading.Lock()
        
    def _load_history(self) -> List[Dict[str, float]]:
        """Load resource history from file"""
        try:
            if self.history_file.exists():
                data = json.loads(self.history_file.read_text(encoding='utf-8'))
                return data.get('snapshots', [])
        except Exception as e:
            logger.error(f"Error loading resource history: {str(e)}")
        return []
    
    def _save_history(self) -> None:
        """Save resource history to file"""
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with self.lock:
                data = {
                    'snapshots': self.snapshots[-100:],  # Keep last 100 snapshots
                    'last_updated': str(datetime.now())
                }
                self.history_file.write_text(json.dumps(data, indent=2), encoding='utf-8')
        except Exception as e:
            logger.error(f"Error saving resource history: {str(e)}")
    
    def check_resources(self) -> Dict[str, float]:
        """
        Check current system resource usage
        
        Returns:
            Dict containing current CPU and memory usage percentages
            
        Raises:
            ResourceThresholdError: If resource usage exceeds thresholds
        """
        try:
            # Get CPU usage with timeout
            cpu_percent = psutil.cpu_percent(interval=min(self.check_interval, 1.0))
            
            # Get memory info
            memory = psutil.virtual_memory()
            
            status = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "timestamp": datetime.now().timestamp()
            }
            
            with self.lock:
                self.snapshots.append(status)
                if len(self.snapshots) > 100:
                    self.snapshots = self.snapshots[-100:]
            
            # Save history periodically (every 10 snapshots)
            if len(self.snapshots) % 10 == 0:
                self._save_history()
            
            # Check thresholds and raise error if exceeded
            self._check_thresholds(status)
            
            return status
            
        except Exception as e:
            logger.error(f"Error checking resources: {str(e)}")
            return {"cpu_percent": 0.0, "memory_percent": 0.0, "timestamp": datetime.now().timestamp()}
    
    def _check_thresholds(self, status: Dict[str, float]) -> None:
        """
        Check if resource usage exceeds thresholds
        
        Raises:
            ResourceThresholdError: If thresholds are exceeded
        """
        messages = []
        
        if status["cpu_percent"] > self.max_cpu_percent:
            messages.append(f"CPU usage too high: {status['cpu_percent']}%")
            
        if status["memory_percent"] > self.max_memory_percent:
            messages.append(f"Memory usage too high: {status['memory_percent']}%")
        
        if messages:
            raise ResourceThresholdError("\n".join(messages))
    
    def get_average_usage(self, last_n: Optional[int] = None) -> Dict[str, float]:
        """Get average resource usage over the last n snapshots"""
        with self.lock:
            if not self.snapshots:
                return {
                    "cpu_percent": 0.0,
                    "memory_percent": 0.0,
                    "timestamp": datetime.now().timestamp()
                }
                
            if last_n is None:
                last_n = len(self.snapshots)
                
            snapshots = self.snapshots[-last_n:]
            
            avg_cpu = sum(s["cpu_percent"] for s in snapshots) / len(snapshots)
            avg_mem = sum(s["memory_percent"] for s in snapshots) / len(snapshots)
            
            return {
                "cpu_percent": avg_cpu,
                "memory_percent": avg_mem,
                "timestamp": datetime.now().timestamp()
            }
    
    def get_peak_usage(self, last_n: Optional[int] = None) -> Dict[str, float]:
        """Get peak resource usage over the last n snapshots"""
        with self.lock:
            if not self.snapshots:
                return {
                    "cpu_percent": 0.0,
                    "memory_percent": 0.0,
                    "timestamp": datetime.now().timestamp()
                }
                
            if last_n is None:
                last_n = len(self.snapshots)
                
            snapshots = self.snapshots[-last_n:]
            
            peak_cpu = max(s["cpu_percent"] for s in snapshots)
            peak_mem = max(s["memory_percent"] for s in snapshots)
            
            return {
                "cpu_percent": peak_cpu,
                "memory_percent": peak_mem,
                "timestamp": datetime.now().timestamp()
            } 