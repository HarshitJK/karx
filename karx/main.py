#!/usr/bin/env python3

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional, NoReturn
import platform

# Check Python version
if sys.version_info < (3, 7):
    sys.exit("Python 3.7 or higher is required to run KARX")

from core.code_writer import CodeWriter
from core.smartfix import SmartFix
from core.explainer import Explainer
from core.linker import Linker
from memory.memory_manager import MemoryManager
from monitor.guardian_angel import GuardianAngel
from clipboard.clipboard_listener import ClipboardListener

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

class KarxController:
    def __init__(self):
        try:
            self.code_writer = CodeWriter()
            self.smart_fix = SmartFix()
            self.explainer = Explainer()
            self.linker = Linker()
            self.memory_manager = MemoryManager()
            self.guardian = GuardianAngel()
            self.clipboard = ClipboardListener()
        except Exception as e:
            logger.error(f"Failed to initialize KARX components: {str(e)}")
            raise
        
    def generate_code(self, prompt: str, output_dir: Optional[Path] = None) -> Optional[Path]:
        """Generate code from a prompt"""
        try:
            self.guardian.check_resources()
            return self.code_writer.generate(prompt, output_dir)
        except Exception as e:
            logger.error(f"Error generating code: {str(e)}")
            return None
    
    def fix_code(self, file_path: Path) -> bool:
        """Fix common errors in code"""
        try:
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return False
                
            self.guardian.check_resources()
            return self.smart_fix.fix(file_path)
        except Exception as e:
            logger.error(f"Error fixing code: {str(e)}")
            return False
    
    def explain_code(self, file_path: Path) -> bool:
        """Explain code line by line"""
        try:
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return False
                
            explanations = self.explainer.explain(file_path)
            if explanations:
                for line_num, code, explanation in explanations:
                    print(f"Line {line_num}: {code}")
                    print(f"Explanation: {explanation}\n")
                return True
            return False
        except Exception as e:
            logger.error(f"Error explaining code: {str(e)}")
            return False
    
    def fix_imports(self, file_path: Path) -> bool:
        """Fix import paths"""
        try:
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return False
                
            return self.linker.fix_imports(file_path)
        except Exception as e:
            logger.error(f"Error fixing imports: {str(e)}")
            return False
    
    def watch_clipboard(self) -> None:
        """Start watching clipboard for prompts"""
        try:
            self.clipboard.start_watching()
        except Exception as e:
            logger.error(f"Error watching clipboard: {str(e)}")

def main() -> int:
    setup_logging()
    
    # Log system information
    logger.info(f"Python version: {platform.python_version()}")
    logger.info(f"Operating system: {platform.system()} {platform.release()}")
    
    parser = argparse.ArgumentParser(description='KARX - AI Code Assistant')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate code from prompt')
    gen_parser.add_argument('prompt', help='Prompt text or file path')
    gen_parser.add_argument('--output', '-o', help='Output directory')
    
    # Fix command
    fix_parser = subparsers.add_parser('fix', help='Fix code issues')
    fix_parser.add_argument('file', help='File to fix')
    
    # Explain command
    explain_parser = subparsers.add_parser('explain', help='Explain code')
    explain_parser.add_argument('file', help='File to explain')
    
    # Import fix command
    import_parser = subparsers.add_parser('imports', help='Fix imports')
    import_parser.add_argument('file', help='File to fix imports')
    
    # Clipboard command
    subparsers.add_parser('watch', help='Watch clipboard for prompts')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        controller = KarxController()
        
        if args.command == 'generate':
            prompt_path = Path(args.prompt)
            prompt = prompt_path.read_text() if prompt_path.exists() else args.prompt
            output_dir = Path(args.output) if args.output else None
            result = controller.generate_code(prompt, output_dir)
            if not result:
                return 1
        
        elif args.command == 'fix':
            if not controller.fix_code(Path(args.file)):
                return 1
        
        elif args.command == 'explain':
            if not controller.explain_code(Path(args.file)):
                return 1
        
        elif args.command == 'imports':
            if not controller.fix_imports(Path(args.file)):
                return 1
        
        elif args.command == 'watch':
            controller.watch_clipboard()
            # Keep the main thread running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Stopping clipboard watcher...")
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 