"""
Conversation Manager Module
Manages multi-turn conversation history and context for the Code Agent.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class ConversationManager:
    """Manages conversation history and context."""
    
    def __init__(self, history_dir: Optional[Path] = None):
        """
        Initialize conversation manager.
        
        Args:
            history_dir: Directory to store conversation history
        """
        if history_dir is None:
            history_dir = Path.cwd() / ".conversation_history"
        
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(exist_ok=True)
        
        self.conversation_file = self.history_dir / "current_session.json"
        self.messages = []
        self.project_context = {}
        
        self._load_history()
        logger.info("✓ ConversationManager initialized")
    
    def _load_history(self) -> None:
        """Load conversation history from file."""
        if self.conversation_file.exists():
            try:
                with open(self.conversation_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.messages = data.get('messages', [])
                    self.project_context = data.get('project_context', {})
                logger.info(f"✓ Loaded {len(self.messages)} messages from history")
            except Exception as e:
                logger.warning(f"Could not load history: {e}")
                self.messages = []
                self.project_context = {}
        else:
            self.messages = []
            self.project_context = {}
    
    def _save_history(self) -> None:
        """Save conversation history to file."""
        try:
            data = {
                'messages': self.messages,
                'project_context': self.project_context,
                'last_updated': datetime.now().isoformat(),
            }
            with open(self.conversation_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
    
    def add_user_message(self, content: str) -> None:
        """
        Add a user message to conversation.
        
        Args:
            content: User message content
        """
        self.messages.append({
            'role': 'user',
            'content': content,
            'timestamp': datetime.now().isoformat(),
        })
        self._save_history()
    
    def add_assistant_message(self, content: str) -> None:
        """
        Add an assistant message to conversation.
        
        Args:
            content: Assistant message content
        """
        self.messages.append({
            'role': 'assistant',
            'content': content,
            'timestamp': datetime.now().isoformat(),
        })
        self._save_history()
    
    def get_full_context(self) -> str:
        """
        Get full conversation context for LLM.
        
        Returns:
            Formatted conversation context
        """
        context = "## Conversation History\n\n"
        
        for msg in self.messages[-10:]:  # Last 10 messages for context
            role = msg['role'].upper()
            content = msg['content'][:200]  # Truncate long messages
            context += f"**{role}:** {content}...\n\n"
        
        if self.project_context:
            context += "\n## Project Context\n"
            context += json.dumps(self.project_context, indent=2, ensure_ascii=False)
        
        return context
    
    def update_project_context(self, key: str, value: Any) -> None:
        """
        Update project context information.
        
        Args:
            key: Context key
            value: Context value
        """
        self.project_context[key] = value
        self._save_history()
    
    def get_project_context(self, key: str, default: Any = None) -> Any:
        """
        Get project context information.
        
        Args:
            key: Context key
            default: Default value if key not found
            
        Returns:
            Context value
        """
        return self.project_context.get(key, default)
    
    def clear_history(self) -> None:
        """Clear all conversation history."""
        self.messages = []
        self.project_context = {}
        if self.conversation_file.exists():
            self.conversation_file.unlink()
        logger.info("✓ Conversation history cleared")
    
    def get_summary(self) -> str:
        """Get conversation summary."""
        return f"""
Conversation Summary:
- Messages: {len(self.messages)}
- Project: {self.project_context.get('project_name', 'Unknown')}
- Files Generated: {self.project_context.get('files_generated', 0)}
- Last Updated: {self.project_context.get('last_updated', 'Never')}
"""


if __name__ == "__main__":
    # Test
    manager = ConversationManager()
    manager.add_user_message("Generate a Flask app")
    manager.add_assistant_message("I'll generate a Flask app with...")
    manager.update_project_context('project_name', 'Flask Web App')
    print(manager.get_summary())
