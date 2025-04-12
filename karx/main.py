#!/usr/bin/env python3

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional, NoReturn
import platform
from config.secure_config import SecureConfig
from datetime import datetime

# Check Python version
if sys.version_info < (3, 7):
    sys.exit("Python 3.7 or higher is required to run KARX")

# Setup logging with file output
def setup_logging() -> None:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_dir / "karx.log")
        ]
    )

logger = logging.getLogger(__name__)

class SecureKarxController:
    def __init__(self, token: str):
        self.config = SecureConfig()
        if not self.config.verify_access(token):
            raise PermissionError("Invalid access token")
            
        self.output_path = self.config.get_output_path()
        if not self.output_path:
            raise ValueError("Output path not configured")
    
    def generate_code(self, prompt: str) -> Optional[Path]:
        """Generate code from a prompt"""
        try:
            # Create a unique file for this generation
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_path / f"generated_{timestamp}.py"
            
            # Write the generated code
            output_file.write_text(f"# Generated from prompt at {timestamp}\n\n{prompt}\n\n# TODO: Implement generated code")
            logger.info(f"Code generated at: {output_file}")
            
            return output_file
            
        except Exception as e:
            logger.error(f"Error generating code: {str(e)}")
            return None
    
    def explain_code(self, content: str) -> bool:
        """Explain the provided code content"""
        try:
            # Write explanation to output directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_path / f"explanation_{timestamp}.txt"
            
            explanation = f"Code Explanation ({timestamp}):\n\n{content}\n\n# TODO: Implement explanation"
            output_file.write_text(explanation)
            
            logger.info(f"Explanation written to: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error explaining code: {str(e)}")
            return False

def main() -> int:
    setup_logging()
    
    # Log system information
    logger.info(f"Python version: {platform.python_version()}")
    logger.info(f"Operating system: {platform.system()} {platform.release()}")
    
    parser = argparse.ArgumentParser(description='KARX - Secure AI Code Assistant')
    parser.add_argument('--token', required=True, help='Access token for authentication')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate code from prompt')
    gen_parser.add_argument('prompt', help='Prompt text or content')
    
    # Explain command
    explain_parser = subparsers.add_parser('explain', help='Explain code')
    explain_parser.add_argument('content', help='Code content to explain')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        controller = SecureKarxController(args.token)
        
        if args.command == 'generate':
            result = controller.generate_code(args.prompt)
            if not result:
                return 1
            print(f"\nCode generated successfully at: {result}")
        
        elif args.command == 'explain':
            if not controller.explain_code(args.content):
                return 1
            print("\nExplanation generated successfully")
        
    except PermissionError as e:
        logger.error(f"Access denied: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 