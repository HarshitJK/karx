import os
from pathlib import Path
from typing import Optional
import json
import hashlib
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SecureConfig:
    def __init__(self, config_file: Optional[Path] = None):
        self.config_file = config_file or Path("config/karx_secure.json")
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        """Load or create secure configuration"""
        if not self.config_file.exists():
            return self._create_default_config()
        try:
            return json.loads(self.config_file.read_text(encoding='utf-8'))
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            return self._create_default_config()
    
    def _create_default_config(self) -> dict:
        """Create default secure configuration"""
        config = {
            "output_path": None,  # Will be set by set_output_path
            "access_token": None,  # Will be set by set_access_token
            "last_modified": str(datetime.now()),
            "permissions": {
                "can_read_files": False,
                "can_write_files": False,
                "can_execute_commands": False,
                "allowed_directories": []
            }
        }
        return config
    
    def save_config(self) -> bool:
        """Save configuration securely"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            self.config["last_modified"] = str(datetime.now())
            self.config_file.write_text(json.dumps(self.config, indent=2), encoding='utf-8')
            os.chmod(self.config_file, 0o600)  # Read/write for owner only
            return True
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")
            return False
    
    def set_output_path(self, path: Path) -> bool:
        """Set the secure output path"""
        try:
            abs_path = path.resolve()
            if not abs_path.exists():
                abs_path.mkdir(parents=True, exist_ok=True)
            os.chmod(abs_path, 0o700)  # Read/write/execute for owner only
            self.config["output_path"] = str(abs_path)
            return self.save_config()
        except Exception as e:
            logger.error(f"Error setting output path: {str(e)}")
            return False
    
    def set_access_token(self, token: str) -> bool:
        """Set access token (hashed)"""
        try:
            hashed = hashlib.sha256(token.encode()).hexdigest()
            self.config["access_token"] = hashed
            return self.save_config()
        except Exception as e:
            logger.error(f"Error setting access token: {str(e)}")
            return False
    
    def verify_access(self, token: str) -> bool:
        """Verify access token"""
        try:
            if not self.config["access_token"]:
                return False
            hashed = hashlib.sha256(token.encode()).hexdigest()
            return hashed == self.config["access_token"]
        except Exception:
            return False
    
    def get_output_path(self) -> Optional[Path]:
        """Get the configured output path"""
        try:
            path_str = self.config.get("output_path")
            return Path(path_str) if path_str else None
        except Exception:
            return None
    
    def is_path_allowed(self, path: Path) -> bool:
        """Check if path is within allowed directories"""
        try:
            abs_path = path.resolve()
            allowed_dirs = [Path(d) for d in self.config["permissions"]["allowed_directories"]]
            return any(abs_path.is_relative_to(d) for d in allowed_dirs)
        except Exception:
            return False