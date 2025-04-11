from pathlib import Path
import json
import logging
import os
import shutil
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, memory_file: Path = Path("memory/code_map.json")):
        self.memory_file = memory_file
        self.backup_file = memory_file.with_suffix('.json.bak')
        self.code_map = self._load_memory()
        
    def _load_memory(self) -> Dict[str, Any]:
        """Load the code map from disk with backup handling"""
        try:
            # Try to load the main file
            if self.memory_file.exists():
                try:
                    return json.loads(self.memory_file.read_text(encoding='utf-8'))
                except json.JSONDecodeError:
                    logger.warning("Main memory file corrupted, trying backup...")
            
            # Try to load the backup file
            if self.backup_file.exists():
                try:
                    data = json.loads(self.backup_file.read_text(encoding='utf-8'))
                    # Restore from backup
                    self.memory_file.write_text(json.dumps(data, indent=2), encoding='utf-8')
                    logger.info("Successfully restored from backup")
                    return data
                except json.JSONDecodeError:
                    logger.error("Backup file also corrupted")
            
            # Create new memory map if neither file exists or both are corrupted
            return {
                "files": {},
                "functions": {},
                "classes": {},
                "variables": {},
                "last_updated": str(datetime.now())
            }
        except Exception as e:
            logger.error(f"Error loading memory: {str(e)}")
            return self._create_empty_memory()
    
    def _create_empty_memory(self) -> Dict[str, Any]:
        """Create a new empty memory structure"""
        return {
            "files": {},
            "functions": {},
            "classes": {},
            "variables": {},
            "last_updated": str(datetime.now())
        }
    
    def save_memory(self) -> bool:
        """Save the current code map to disk with backup"""
        try:
            # Create directory if it doesn't exist
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Create backup of existing file if it exists
            if self.memory_file.exists():
                shutil.copy2(self.memory_file, self.backup_file)
            
            # Update timestamp
            self.code_map["last_updated"] = str(datetime.now())
            
            # Write new content
            temp_file = self.memory_file.with_suffix('.tmp')
            temp_file.write_text(json.dumps(self.code_map, indent=2), encoding='utf-8')
            
            # Atomic replace
            temp_file.replace(self.memory_file)
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving memory: {str(e)}")
            return False
    
    def add_file(self, file_path: Path, content: str) -> bool:
        """Add or update a file in the code map"""
        try:
            if not file_path.exists():
                logger.error(f"File does not exist: {file_path}")
                return False
                
            rel_path = str(file_path.resolve())
            
            # Extract file information
            file_info = {
                "last_modified": str(datetime.fromtimestamp(file_path.stat().st_mtime)),
                "size": len(content),
                "functions": self._extract_functions(content),
                "classes": self._extract_classes(content),
                "variables": self._extract_variables(content)
            }
            
            # Update the code map
            self.code_map["files"][rel_path] = file_info
            
            return self.save_memory()
            
        except Exception as e:
            logger.error(f"Error adding file to memory: {str(e)}")
            return False
    
    def get_suggestions(self, context: str) -> List[str]:
        """Get code suggestions based on the current context"""
        try:
            # TODO: Implement smart suggestion logic
            return []
        except Exception as e:
            logger.error(f"Error getting suggestions: {str(e)}")
            return []
    
    def _extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """Extract function definitions from code"""
        try:
            # TODO: Implement function extraction
            return []
        except Exception as e:
            logger.error(f"Error extracting functions: {str(e)}")
            return []
    
    def _extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract class definitions from code"""
        try:
            # TODO: Implement class extraction
            return []
        except Exception as e:
            logger.error(f"Error extracting classes: {str(e)}")
            return []
    
    def _extract_variables(self, content: str) -> List[Dict[str, Any]]:
        """Extract variable definitions from code"""
        try:
            # TODO: Implement variable extraction
            return []
        except Exception as e:
            logger.error(f"Error extracting variables: {str(e)}")
            return [] 