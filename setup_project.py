#!/usr/bin/env python3
"""
Project Setup Script
Automatically creates the project directory structure for the Multi-Agent Software Development System.
"""

import os
from pathlib import Path


def create_project_structure():
    """Create the project folder structure and necessary files."""
    
    # Define the root directory (current directory where script is run)
    root_dir = Path.cwd()
    
    # Define folder structure
    folders = [
        "agents",
        "tools",
        "utils",
        "workspace",
    ]
    
    # Create directories
    print("📁 Creating directories...")
    for folder in folders:
        folder_path = root_dir / folder
        folder_path.mkdir(exist_ok=True)
        print(f"  ✓ Created: {folder}")
    
    # Create __init__.py files in each module folder
    print("\n📝 Creating __init__.py files...")
    for folder in folders:
        init_file = root_dir / folder / "__init__.py"
        if not init_file.exists():
            init_file.write_text("")
            print(f"  ✓ Created: {folder}/__init__.py")
        else:
            print(f"  ℹ Already exists: {folder}/__init__.py")
    
    # Create main.py
    print("\n📄 Creating main.py...")
    main_py_path = root_dir / "main.py"
    if not main_py_path.exists():
        main_py_content = '''#!/usr/bin/env python3
"""
Multi-Agent Software Development System - Main Orchestrator
"""

from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.reviewer import ReviewerAgent
from config import Config


def main():
    """Main entry point for the orchestrator."""
    config = Config()
    
    # Initialize agents
    planner = PlannerAgent(config)
    coder = CoderAgent(config)
    reviewer = ReviewerAgent(config)
    
    # Example: Process user request
    user_request = "Create an arXiv CS Daily webpage"
    
    print(f"🚀 Starting Multi-Agent System")
    print(f"📋 User Request: {user_request}")
    print("-" * 50)
    
    # Step 1: Planning
    print("\\n📍 Step 1: Planning Phase...")
    plan = planner.generate_plan(user_request)
    print(f"✓ Plan generated: {plan}")
    
    # Step 2: Code Generation
    print("\\n📍 Step 2: Code Generation Phase...")
    for task in plan.get("tasks", []):
        print(f"  Executing: {task}")
        code = coder.generate_code(task)
        print(f"  ✓ Generated code for: {task}")
    
    # Step 3: Review (Optional)
    print("\\n📍 Step 3: Review Phase (Optional)...")
    print("✓ System ready for code review")
    
    print("\\n" + "=" * 50)
    print("✅ Multi-Agent System Execution Complete!")


if __name__ == "__main__":
    main()
'''
        main_py_path.write_text(main_py_content)
        print(f"  ✓ Created: main.py")
    else:
        print(f"  ℹ Already exists: main.py")
    
    # Create config.py
    print("\n📄 Creating config.py...")
    config_py_path = root_dir / "config.py"
    if not config_py_path.exists():
        config_py_content = '''"""
Configuration Module
Loads environment variables and project settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


class Config:
    """Configuration class for the Multi-Agent System."""
    
    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek")
    LLM_API_KEY = os.getenv("LLM_API_KEY", "")
    LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
    
    # Project Paths
    PROJECT_ROOT = Path(__file__).parent
    WORKSPACE_DIR = PROJECT_ROOT / "workspace"
    
    # Agent Configuration
    PLANNER_MODEL = os.getenv("PLANNER_MODEL", "deepseek-chat")
    CODER_MODEL = os.getenv("CODER_MODEL", "deepseek-chat")
    REVIEWER_MODEL = os.getenv("REVIEWER_MODEL", "deepseek-chat")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    def __init__(self):
        """Initialize configuration and validate required settings."""
        if not self.LLM_API_KEY:
            raise ValueError(
                "LLM_API_KEY not found in environment variables. "
                "Please set it in .env file."
            )
        
        # Ensure workspace directory exists
        self.WORKSPACE_DIR.mkdir(exist_ok=True)


if __name__ == "__main__":
    config = Config()
    print(f"Project Root: {config.PROJECT_ROOT}")
    print(f"Workspace Dir: {config.WORKSPACE_DIR}")
    print(f"LLM Provider: {config.LLM_PROVIDER}")
    print(f"LLM Model: {config.LLM_MODEL}")
'''
        config_py_path.write_text(config_py_content)
        print(f"  ✓ Created: config.py")
    else:
        print(f"  ℹ Already exists: config.py")
    
    # Create .env file
    print("\n📄 Creating .env file...")
    env_path = root_dir / ".env"
    if not env_path.exists():
        env_content = '''# LLM Configuration
LLM_PROVIDER=deepseek
LLM_API_KEY=your_api_key_here
LLM_MODEL=deepseek-chat
LLM_BASE_URL=https://api.deepseek.com

# Agent-specific models (optional - defaults to LLM_MODEL)
PLANNER_MODEL=deepseek-chat
CODER_MODEL=deepseek-chat
REVIEWER_MODEL=deepseek-chat

# Logging
LOG_LEVEL=INFO
'''
        env_path.write_text(env_content)
        print(f"  ✓ Created: .env")
    else:
        print(f"  ℹ Already exists: .env")
    
    print("\n" + "=" * 50)
    print("✅ Project Structure Setup Complete!")
    print("=" * 50)
    print("\nNext Steps:")
    print("1. Update .env file with your LLM API credentials")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Implement agent modules in agents/ folder")
    print("4. Run: python main.py")


if __name__ == "__main__":
    create_project_structure()
