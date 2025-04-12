#!/usr/bin/env python3

import sys
from pathlib import Path
import secrets
from config.secure_config import SecureConfig
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_secure_karx():
    """Initialize KARX with secure settings"""
    try:
        # Create secure configuration
        config = SecureConfig()
        
        # Generate a secure access token
        access_token = secrets.token_urlsafe(32)
        
        # Get output directory from user
        print("\nKARX Secure Setup")
        print("================")
        
        while True:
            output_dir = input("\nEnter the absolute path where KARX should write files: ").strip()
            if not output_dir:
                print("Path cannot be empty")
                continue
                
            path = Path(output_dir)
            try:
                # Ensure path is absolute
                if not path.is_absolute():
                    print("Please provide an absolute path")
                    continue
                    
                # Set and create output directory
                if config.set_output_path(path):
                    break
                else:
                    print("Failed to set output directory. Please try again.")
            except Exception as e:
                print(f"Error with path: {str(e)}")
        
        # Set access token
        if not config.set_access_token(access_token):
            print("Failed to set access token")
            return False
        
        # Set minimal permissions
        config.config["permissions"].update({
            "can_read_files": True,
            "can_write_files": True,
            "can_execute_commands": False,
            "allowed_directories": [str(path)]
        })
        
        if not config.save_config():
            print("Failed to save configuration")
            return False
        
        # Print success message and token
        print("\nKARX has been configured successfully!")
        print("\nIMPORTANT: Save this access token securely. It will not be shown again:")
        print(f"\nAccess Token: {access_token}")
        print("\nOutput Directory:", path)
        print("\nTo use KARX, run:")
        print(f"python main.py --token {access_token} [command] [arguments]")
        
        return True
        
    except KeyboardInterrupt:
        print("\nSetup cancelled by user")
        return False
    except Exception as e:
        logger.error(f"Setup failed: {str(e)}")
        return False

if __name__ == "__main__":
    sys.exit(0 if init_secure_karx() else 1) 