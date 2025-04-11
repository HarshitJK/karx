import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

logger = logging.getLogger(__name__)

def ensure_directory(path: Path) -> Path:
    """Ensure a directory exists and create it if it doesn't"""
    path.mkdir(parents=True, exist_ok=True)
    return path

def load_json_file(file_path: Path) -> Dict[str, Any]:
    """Load and parse a JSON file"""
    try:
        if file_path.exists():
            return json.loads(file_path.read_text())
        return {}
    except Exception as e:
        logger.error(f"Error loading JSON file {file_path}: {str(e)}")
        return {}

def save_json_file(file_path: Path, data: Dict[str, Any]):
    """Save data to a JSON file"""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(data, indent=2))
    except Exception as e:
        logger.error(f"Error saving JSON file {file_path}: {str(e)}")

def get_file_type(file_path: Path) -> str:
    """Get the type of a file based on its extension"""
    return file_path.suffix.lower()[1:] if file_path.suffix else ""

def list_files(directory: Path, pattern: str = "*") -> List[Path]:
    """List all files in a directory matching a pattern"""
    try:
        return list(directory.glob(pattern))
    except Exception as e:
        logger.error(f"Error listing files in {directory}: {str(e)}")
        return []

def get_relative_path(path: Path, relative_to: Optional[Path] = None) -> Path:
    """Get a path relative to another path or the current working directory"""
    try:
        if relative_to is None:
            relative_to = Path.cwd()
        return path.relative_to(relative_to)
    except Exception:
        return path

def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters"""
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename 