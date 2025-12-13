"""
File Tools Module
Provides utilities for managing file operations in the workspace.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime
from config import Config


logger = logging.getLogger(__name__)


class FileTools:
    """
    File management utilities for the Multi-Agent System.
    Handles saving generated code to the workspace directory.
    """
    
    # Get workspace directory from config
    WORKSPACE_DIR = Config.WORKSPACE_DIR
    
    # Current generation session ID (set when starting a new generation)
    CURRENT_SESSION_ID = None
    CURRENT_SESSION_DIR = None
    
    @staticmethod
    def start_generation_session(session_name: str = None) -> str:
        """
        Create a new session directory for code generation.
        Each generation gets its own timestamped folder.
        
        Args:
            session_name (str): Optional custom name for the session
            
        Returns:
            str: Path to the new session directory
        """
        # Generate session ID with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if session_name:
            # Sanitize session name
            session_name = session_name.replace(" ", "_").replace("/", "_")[:30]
            session_id = f"{timestamp}_{session_name}"
        else:
            session_id = f"session_{timestamp}"
        
        # Create session directory
        session_dir = FileTools.WORKSPACE_DIR / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # Update class variables
        FileTools.CURRENT_SESSION_ID = session_id
        FileTools.CURRENT_SESSION_DIR = session_dir
        
        logger.info(f"✓ Started generation session: {session_id}")
        print(f"\n📁 New generation session: {session_id}")
        print(f"   Location: {session_dir}\n")
        
        return str(session_dir)
    
    @staticmethod
    def get_current_session_dir() -> Path:
        """
        Get the current session directory.
        If no session is active, create one.
        
        Returns:
            Path: Current session directory
        """
        if FileTools.CURRENT_SESSION_DIR is None:
            FileTools.start_generation_session()
        
        return FileTools.CURRENT_SESSION_DIR
    
    @staticmethod
    def save_code(filename: str, code: str, encoding: str = "utf-8") -> str:
        """
        Save generated code to a file in the current session directory.
        
        Args:
            filename (str): Relative path within session (e.g., 'app.py' or 'src/main.py')
            code (str): The code content to save
            encoding (str): File encoding. Default: 'utf-8'
            
        Returns:
            str: Absolute path to the saved file
            
        Raises:
            ValueError: If filename is empty or invalid
            IOError: If file cannot be written
        """
        try:
            # Validate inputs
            if not filename or not isinstance(filename, str):
                raise ValueError("filename must be a non-empty string")
            
            if not isinstance(code, str):
                raise ValueError("code must be a string")
            
            # Get current session directory (create if needed)
            session_dir = FileTools.get_current_session_dir()
            
            # Construct full file path within session
            file_path = session_dir / filename
            
            # Ensure parent directories exist
            parent_dir = file_path.parent
            parent_dir.mkdir(parents=True, exist_ok=True)
            
            # Write code to file
            with open(file_path, "w", encoding=encoding) as f:
                f.write(code)
            
            # Calculate relative path for display
            relative_path = file_path.relative_to(FileTools.WORKSPACE_DIR.parent)
            
            # Log success
            logger.info(f"✓ Saved file: {relative_path}")
            print(f"✓ Saved file: {relative_path}")
            
            return str(file_path)
        
        except ValueError as e:
            error_msg = f"❌ Validation Error: {str(e)}"
            logger.error(error_msg)
            raise
        
        except IOError as e:
            error_msg = f"❌ File Write Error: Failed to write to {filename}"
            logger.error(error_msg)
            logger.error(f"   Details: {str(e)}")
            raise
        
        except Exception as e:
            error_msg = f"❌ Unexpected Error: {type(e).__name__}: {str(e)}"
            logger.error(error_msg)
            raise
    
    @staticmethod
    def save_code_to_workspace(filename: str, code: str, encoding: str = "utf-8") -> str:
        """
        Save generated code directly to workspace root (legacy behavior).
        This is kept for backwards compatibility.
        
        Args:
            filename (str): Relative path within workspace
            code (str): The code content to save
            encoding (str): File encoding. Default: 'utf-8'
            
        Returns:
            str: Absolute path to the saved file
        """
        try:
            # Validate inputs
            if not filename or not isinstance(filename, str):
                raise ValueError("filename must be a non-empty string")
            
            if not isinstance(code, str):
                raise ValueError("code must be a string")
            
            # Construct full file path directly in workspace
            file_path = FileTools.WORKSPACE_DIR / filename
            
            # Ensure parent directories exist
            parent_dir = file_path.parent
            parent_dir.mkdir(parents=True, exist_ok=True)
            
            # Write code to file
            with open(file_path, "w", encoding=encoding) as f:
                f.write(code)
            
            # Calculate relative path for display
            relative_path = file_path.relative_to(FileTools.WORKSPACE_DIR.parent)
            
            # Log success
            logger.info(f"✓ Saved file: {relative_path}")
            print(f"✓ Saved file: {relative_path}")
            
            return str(file_path)
        
        except Exception as e:
            error_msg = f"❌ Error: {type(e).__name__}: {str(e)}"
            logger.error(error_msg)
            raise
    
    @staticmethod
    def read_code(filename: str, encoding: str = "utf-8") -> str:
        """
        Read code from a file in the workspace directory.
        
        Args:
            filename (str): Relative path within workspace
            encoding (str): File encoding. Default: 'utf-8'
            
        Returns:
            str: File content
            
        Raises:
            FileNotFoundError: If file does not exist
            IOError: If file cannot be read
        """
        try:
            file_path = FileTools.WORKSPACE_DIR / filename
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {filename}")
            
            with open(file_path, "r", encoding=encoding) as f:
                content = f.read()
            
            logger.debug(f"✓ Read file: {filename}")
            return content
        
        except FileNotFoundError as e:
            logger.error(f"❌ File Not Found: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(f"❌ File Read Error: {str(e)}")
            raise
    
    @staticmethod
    def create_directory(directory_path: str) -> str:
        """
        Create a directory in the workspace.
        
        Args:
            directory_path (str): Relative path within workspace
            
        Returns:
            str: Absolute path to the created directory
            
        Raises:
            ValueError: If path is invalid
            IOError: If directory cannot be created
        """
        try:
            if not directory_path or not isinstance(directory_path, str):
                raise ValueError("directory_path must be a non-empty string")
            
            dir_path = FileTools.WORKSPACE_DIR / directory_path
            dir_path.mkdir(parents=True, exist_ok=True)
            
            relative_path = dir_path.relative_to(FileTools.WORKSPACE_DIR.parent)
            logger.info(f"✓ Created directory: {relative_path}")
            print(f"✓ Created directory: {relative_path}")
            
            return str(dir_path)
        
        except ValueError as e:
            logger.error(f"❌ Validation Error: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(f"❌ Directory Creation Error: {str(e)}")
            raise
    
    @staticmethod
    def list_files(directory: str = ".") -> list:
        """
        List all files in a workspace directory.
        
        Args:
            directory (str): Relative path within workspace. Default: '.'
            
        Returns:
            list: List of file paths (relative to workspace)
        """
        try:
            dir_path = FileTools.WORKSPACE_DIR / directory
            
            if not dir_path.exists():
                raise FileNotFoundError(f"Directory not found: {directory}")
            
            files = []
            for file_path in dir_path.rglob("*"):
                if file_path.is_file():
                    relative = file_path.relative_to(FileTools.WORKSPACE_DIR)
                    files.append(str(relative))
            
            return sorted(files)
        
        except Exception as e:
            logger.error(f"❌ List Files Error: {str(e)}")
            raise
    
    @staticmethod
    def file_exists(filename: str) -> bool:
        """
        Check if a file exists in the workspace.
        
        Args:
            filename (str): Relative path within workspace
            
        Returns:
            bool: True if file exists, False otherwise
        """
        file_path = FileTools.WORKSPACE_DIR / filename
        return file_path.exists()
    
    @staticmethod
    def delete_file(filename: str) -> bool:
        """
        Delete a file from the workspace.
        
        Args:
            filename (str): Relative path within workspace
            
        Returns:
            bool: True if file was deleted, False if file didn't exist
            
        Raises:
            IOError: If file cannot be deleted
        """
        try:
            file_path = FileTools.WORKSPACE_DIR / filename
            
            if not file_path.exists():
                logger.warning(f"⚠️  File not found: {filename}")
                return False
            
            file_path.unlink()
            logger.info(f"✓ Deleted file: {filename}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Delete File Error: {str(e)}")
            raise
    
    @staticmethod
    def get_workspace_info() -> dict:
        """
        Get information about the workspace.
        
        Returns:
            dict: Workspace metadata including path and file count
        """
        try:
            files = FileTools.list_files()
            return {
                "workspace_path": str(FileTools.WORKSPACE_DIR),
                "file_count": len(files),
                "files": files,
                "exists": FileTools.WORKSPACE_DIR.exists(),
            }
        except Exception as e:
            logger.error(f"❌ Workspace Info Error: {str(e)}")
            raise


if __name__ == "__main__":
    # Test the File Tools
    try:
        print("=" * 60)
        print("🧪 Testing File Tools")
        print("=" * 60)
        
        # Test 1: Save a simple Python file
        print("\n📍 Test 1: Saving a Python file...")
        sample_code = '''"""
Sample Python Module
"""

def hello_world():
    """Print hello world."""
    return "Hello, World!"

if __name__ == "__main__":
    print(hello_world())
'''
        
        saved_path = FileTools.save_code("sample.py", sample_code)
        print(f"   Saved to: {saved_path}")
        
        # Test 2: Create nested directory and save file
        print("\n📍 Test 2: Saving file in nested directory...")
        nested_code = """# Nested file in templates
HTML_TEMPLATE = '''
<html>
<body>Hello</body>
</html>
'''
"""
        FileTools.save_code("templates/index.html.py", nested_code)
        
        # Test 3: Read file
        print("\n📍 Test 3: Reading saved file...")
        content = FileTools.read_code("sample.py")
        print(f"   Read {len(content)} characters")
        print(f"   First 50 chars: {content[:50]}...")
        
        # Test 4: List files
        print("\n📍 Test 4: Listing workspace files...")
        files = FileTools.list_files()
        print(f"   Total files: {len(files)}")
        for file in files[:5]:  # Show first 5
            print(f"     - {file}")
        
        # Test 5: Check file existence
        print("\n📍 Test 5: Checking file existence...")
        exists = FileTools.file_exists("sample.py")
        print(f"   sample.py exists: {exists}")
        
        # Test 6: Get workspace info
        print("\n📍 Test 6: Getting workspace information...")
        info = FileTools.get_workspace_info()
        print(f"   Workspace: {info['workspace_path']}")
        print(f"   Total files: {info['file_count']}")
        
        print("\n" + "=" * 60)
        print("✅ File Tools Test Successful!")
        print("=" * 60)
    
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
