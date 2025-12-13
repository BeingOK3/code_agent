#!/usr/bin/env python3
"""
Interactive Code Agent CLI
A multi-turn conversational interface for the Code Agent System.
Allows users to interact with Code Agent like ChatGPT in the terminal.
"""

import sys
import logging
from pathlib import Path
from typing import Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.conversation_manager import ConversationManager
from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from tools.file_tools import FileTools
from utils.llm_client import LLMClient
from config import Config


# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Reduce noise for CLI
    format='%(message)s'
)
logger = logging.getLogger(__name__)


class InteractiveCodeAgent:
    """Interactive multi-turn Code Agent."""
    
    def __init__(self):
        """Initialize the interactive agent."""
        self.config = Config()
        self.llm_client = LLMClient(config=self.config)
        self.planner = PlannerAgent(config=self.config)
        self.coder = CoderAgent(config=self.config)
        self.conversation_manager = ConversationManager()
        
        print("✓ Code Agent initialized (conversation-aware mode)")
    
    def process_user_input(self, user_input: str) -> str:
        """
        Process user input and generate response.
        
        Args:
            user_input: User message
            
        Returns:
            Agent response
        """
        try:
            # Save user message
            self.conversation_manager.add_user_message(user_input)
            
            # Get conversation context
            context = self.conversation_manager.get_full_context()
            
            # Check user intent
            # Keywords for code generation
            generate_keywords = ['generate', 'create', 'build', 'make', 'write', 'implement', 
                                '生成', '创建', '编写', '实现', '构建', '开发']
            
            if any(keyword in user_input.lower() for keyword in generate_keywords):
                return self._handle_generation_request(user_input, context)
            
            elif any(keyword in user_input.lower() for keyword in ['modify', 'change', 'improve', 'fix', 'update']):
                return self._handle_modification_request(user_input, context)
            
            elif any(keyword in user_input.lower() for keyword in ['status', 'info', 'show', 'list', 'what']):
                return self._handle_info_request(user_input)
            
            elif any(keyword in user_input.lower() for keyword in ['clear', 'reset', 'new']):
                return self._handle_clear_request()
            
            elif any(keyword in user_input.lower() for keyword in ['help', '?']):
                return self._show_help()
            
            else:
                # Default: ask LLM to help figure out intent, or assume generation if code-related
                # If the input contains code-related terms, treat as generation request
                code_related_terms = ['算法', '代码', 'code', 'algorithm', 'function', 'class', 'method', 
                                     '函数', '类', '方法', 'api', 'library', '库', 'framework', '框架',
                                     'app', '应用', '应用程序', '系统', 'system', 'tool', '工具']
                
                if any(term in user_input.lower() for term in code_related_terms):
                    # Likely a code generation request
                    return self._handle_generation_request(user_input, context)
                
                # Otherwise ask LLM for advice
                return self._ask_llm_advice(user_input, context)
        
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.conversation_manager.add_assistant_message(error_msg)
            return error_msg
    
    def _handle_generation_request(self, user_input: str, context: str) -> str:
        """Handle project generation requests."""
        response = "🔄 Generating project based on your request...\n\n"
        
        try:
            # Use user input as requirement
            print(f"\n📝 Planning phase...")
            plan = self.planner.plan_project(user_input)
            
            # Start a new generation session with project name
            project_name = plan.get('project_name', 'project').replace(" ", "_")[:30]
            from tools.file_tools import FileTools
            session_dir = FileTools.start_generation_session(project_name)
            
            response += f"📋 **Project Plan:**\n"
            response += f"- Name: {plan.get('project_name', 'Unknown')}\n"
            response += f"- Files to generate: {len(plan.get('files', []))}\n"
            response += f"- Tech Stack: {', '.join(plan.get('tech_stack', []))}\n"
            response += f"- Session: 📁 `{project_name}` folder in workspace\n\n"
            
            print(f"💻 Generating code...")
            generated_count = 0
            files = plan.get("files", [])
            
            for file_entry in files[:3]:  # Generate first 3 files for demo
                filename = file_entry.get("filename")
                purpose = file_entry.get("purpose")
                
                try:
                    code = self.coder.generate_code(
                        filename=filename,
                        task_description=purpose,
                        full_plan_context=self.conversation_manager.get_full_context(),
                        language=self._detect_language(filename)
                    )
                    generated_count += 1
                except Exception as e:
                    print(f"⚠️  Failed to generate {filename}: {e}")
            
            response += f"✅ **Generated {generated_count} files successfully!**\n"
            response += f"📁 Files saved to: `workspace/{project_name}/`\n"
            
            # Update context
            self.conversation_manager.update_project_context('project_name', plan.get('project_name'))
            self.conversation_manager.update_project_context('files_generated', generated_count)
            
        except Exception as e:
            response = f"❌ Generation failed: {str(e)}"
        
        self.conversation_manager.add_assistant_message(response)
        return response
    
    def _handle_modification_request(self, user_input: str, context: str) -> str:
        """Handle code modification requests."""
        response = "🔧 Processing modification request...\n\n"
        
        try:
            # Ask LLM what to modify
            advice = self._ask_llm_advice(
                f"User wants to modify code: {user_input}. Based on our conversation context, what files should we modify?",
                context
            )
            response += advice
        except Exception as e:
            response = f"❌ Modification failed: {str(e)}"
        
        self.conversation_manager.add_assistant_message(response)
        return response
    
    def _handle_info_request(self, user_input: str) -> str:
        """Handle information requests."""
        workspace_info = FileTools.get_workspace_info()
        
        response = "📊 **Project Information:**\n\n"
        response += self.conversation_manager.get_summary()
        response += f"\n📁 **Workspace Files ({workspace_info['file_count']} total):**\n"
        
        for file in sorted(workspace_info['files'])[:10]:  # Show first 10
            response += f"  - {file}\n"
        
        if len(workspace_info['files']) > 10:
            response += f"  ... and {len(workspace_info['files']) - 10} more files\n"
        
        self.conversation_manager.add_assistant_message(response)
        return response
    
    def _handle_clear_request(self) -> str:
        """Handle clear/reset requests."""
        self.conversation_manager.clear_history()
        response = "🔄 Conversation history cleared. Starting fresh!\n"
        self.conversation_manager.add_assistant_message(response)
        return response
    
    def _ask_llm_advice(self, user_input: str, context: str) -> str:
        """Ask LLM for advice based on conversation."""
        messages = [
            {
                "role": "system",
                "content": """You are an intelligent Code Generation Assistant. 
You help users generate, modify, and improve code based on their requirements.
Provide helpful, concise responses. When suggesting code, be specific about what to do.
Remember the conversation context and refer to previous decisions."""
            },
            {
                "role": "user",
                "content": f"Previous context:\n{context}\n\nNew request: {user_input}"
            }
        ]
        
        response = self.llm_client.chat(messages=messages, temperature=0.7)
        self.conversation_manager.add_assistant_message(response)
        return response
    
    def _detect_language(self, filename: str) -> str:
        """Detect programming language from filename."""
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.java': 'java',
            '.go': 'go',
        }
        
        for ext, lang in extension_map.items():
            if filename.endswith(ext):
                return lang
        return 'python'
    
    def _show_help(self) -> str:
        """Show help message."""
        help_text = """
🚀 **Code Agent - Interactive Commands**

**Generation Commands:**
  - "Generate a [project type]" - Create a new project
  - "Create a Flask API for..." - Specify a project
  - "Build a [description]" - Generate code

**Modification Commands:**
  - "Improve the [filename]" - Enhance existing file
  - "Fix the error in [filename]" - Fix bugs
  - "Add [feature] to [file]" - Add new features

**Information Commands:**
  - "Status" or "Info" - Show project info
  - "List files" - List workspace files
  - "What's been done?" - Show summary

**System Commands:**
  - "Clear" or "Reset" - Clear conversation
  - "Help" - Show this message
  - "Quit" or "Exit" - Exit the program

**Example Conversation:**
  User: Generate a Flask REST API for user management
  Agent: [Plans and generates code]
  User: Can you add JWT authentication?
  Agent: [Modifies code based on previous context]
  User: Show status
  Agent: [Displays current state]

💡 Tip: I remember your entire conversation, so you can iterate on ideas!
"""
        self.conversation_manager.add_assistant_message(help_text)
        return help_text


def main():
    """Main interactive loop."""
    print("\n" + "=" * 70)
    print("🚀 Code Agent - Interactive Multi-Turn Conversation Mode")
    print("=" * 70)
    print("\nWelcome! I can generate code, modify files, and remember our conversation.")
    print("Type 'help' for commands or start chatting!\n")
    
    agent = InteractiveCodeAgent()
    
    try:
        while True:
            try:
                # Read user input
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Goodbye! Your conversation has been saved.")
                    break
                
                # Process input
                print("\n🤖 Agent: ", end="", flush=True)
                response = agent.process_user_input(user_input)
                print(response)
                print()
            
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
    
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
