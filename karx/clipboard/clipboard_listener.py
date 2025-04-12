import pyperclip
import time
import logging
from pathlib import Path
from typing import Optional, Callable
import threading

logger = logging.getLogger(__name__)

class ClipboardListener:
    def __init__(self, 
                 callback: Optional[Callable[[str], None]] = None,
                 check_interval: float = 0.5):
        self.callback = callback
        self.check_interval = check_interval
        self.last_content = ""
        self.is_running = False
        self.thread = None
        
    def start_watching(self):
        """Start watching the clipboard in a background thread"""
        if self.is_running:
            logger.warning("Clipboard listener is already running")
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._watch_clipboard)
        self.thread.daemon = True
        self.thread.start()
        
        logger.info("Started watching clipboard")
    
    def stop_watching(self):
        """Stop watching the clipboard"""
        self.is_running = False
        if self.thread:
            self.thread.join()
            self.thread = None
        logger.info("Stopped watching clipboard")
    
    def _watch_clipboard(self):
        """Background thread function to watch clipboard"""
        while self.is_running:
            try:
                current_content = pyperclip.paste()
                
                if current_content != self.last_content:
                    logger.info("New content detected in clipboard")
                    self.last_content = current_content
                    
                    if self.callback:
                        self.callback(current_content)
                    
            except Exception as e:
                logger.error(f"Error watching clipboard: {str(e)}")
                
            time.sleep(self.check_interval)
    
    def get_last_content(self) -> str:
        """Get the last content seen in the clipboard"""
        return self.last_content 