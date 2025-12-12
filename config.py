"""
Configuration Module
Loads environment variables and project settings from .env file.
Manages LLM API credentials, model selection, and project paths.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env file
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)


class Config:
    """
    Configuration class for the Multi-Agent Software Development System.
    Handles LLM API settings, agent models, and project paths.
    """
    
    # ===== LLM Configuration =====
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek").lower()
    LLM_API_KEY = os.getenv("LLM_API_KEY", "").strip()
    LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com").rstrip("/")
    
    # ===== Project Paths =====
    PROJECT_ROOT = Path(__file__).parent
    WORKSPACE_DIR = PROJECT_ROOT / "workspace"
    
    # ===== Agent-Specific Models =====
    PLANNER_MODEL = os.getenv("PLANNER_MODEL", "deepseek-chat")
    CODER_MODEL = os.getenv("CODER_MODEL", "deepseek-chat")
    REVIEWER_MODEL = os.getenv("REVIEWER_MODEL", "deepseek-chat")
    
    # ===== Logging Configuration =====
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    
    def __init__(self):
        """
        Initialize configuration and validate required settings.
        
        Raises:
            ValueError: If LLM_API_KEY is not set in environment variables.
            FileNotFoundError: If .env file is not found.
        """
        # Validate .env file exists
        if not dotenv_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {dotenv_path}\n"
                "Please ensure .env file exists in project root."
            )
        
        # Validate API Key
        if not self.LLM_API_KEY:
            raise ValueError(
                "❌ LLM_API_KEY is not configured!\n"
                f"Please set LLM_API_KEY in: {dotenv_path}"
            )
        
        # Validate provider
        supported_providers = ["deepseek", "openai", "anthropic"]
        if self.LLM_PROVIDER not in supported_providers:
            raise ValueError(
                f"❌ Unsupported LLM_PROVIDER: {self.LLM_PROVIDER}\n"
                f"Supported: {', '.join(supported_providers)}"
            )
        
        # Ensure workspace directory exists
        self.WORKSPACE_DIR.mkdir(exist_ok=True, parents=True)
        print(f"✓ Workspace directory ready: {self.WORKSPACE_DIR}")
    
    def get_llm_config(self):
        """
        Get complete LLM configuration as a dictionary.
        
        Returns:
            dict: LLM configuration including provider, API key, model, and base URL.
        """
        return {
            "provider": self.LLM_PROVIDER,
            "api_key": self.LLM_API_KEY,
            "model": self.LLM_MODEL,
            "base_url": self.LLM_BASE_URL,
        }
    
    def get_agent_models(self):
        """
        Get agent-specific model assignments.
        
        Returns:
            dict: Model names for each agent type.
        """
        return {
            "planner": self.PLANNER_MODEL,
            "coder": self.CODER_MODEL,
            "reviewer": self.REVIEWER_MODEL,
        }
    
    def validate_api_connection(self):
        """
        Validate that the LLM API is accessible (basic check).
        
        Returns:
            bool: True if configuration appears valid, False otherwise.
        """
        # Basic validation checks
        checks = [
            ("API Key set", len(self.LLM_API_KEY) > 10),
            ("Provider valid", self.LLM_PROVIDER in ["deepseek", "openai", "anthropic"]),
            ("Base URL valid", self.LLM_BASE_URL.startswith("https://")),
            ("Model name set", bool(self.LLM_MODEL)),
        ]
        
        all_valid = True
        for check_name, is_valid in checks:
            status = "✓" if is_valid else "✗"
            print(f"{status} {check_name}")
            all_valid = all_valid and is_valid
        
        return all_valid


if __name__ == "__main__":
    # Test configuration loading
    try:
        config = Config()
        print("\n" + "="*50)
        print("✅ Configuration Loaded Successfully!")
        print("="*50)
        print(f"\n📍 Project Root: {config.PROJECT_ROOT}")
        print(f"📁 Workspace Dir: {config.WORKSPACE_DIR}")
        print(f"\n🔧 LLM Configuration:")
        print(f"   Provider: {config.LLM_PROVIDER.upper()}")
        print(f"   Model: {config.LLM_MODEL}")
        print(f"   Base URL: {config.LLM_BASE_URL}")
        print(f"   API Key: {config.LLM_API_KEY[:10]}...{config.LLM_API_KEY[-10:]}")
        print(f"\n🤖 Agent Models:")
        agent_models = config.get_agent_models()
        for agent, model in agent_models.items():
            print(f"   {agent.capitalize()}: {model}")
        print(f"\n📊 API Connection Validation:")
        config.validate_api_connection()
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
