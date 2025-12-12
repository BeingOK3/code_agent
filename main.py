#!/usr/bin/env python3
"""
Multi-Agent Software Development System - Main Orchestrator

This is the central orchestration point that coordinates all agents:
- PlannerAgent: Analyzes requirements and generates project plans
- CoderAgent: Generates code based on the plan
- FileTools: Manages generated files in the workspace

Workflow:
1. Parse user requirement
2. Generate project plan (file structure, tech stack, tasks)
3. Generate code for each file
4. Save all files to workspace
5. Report completion
"""

import logging
from typing import Optional, Dict, Any
from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from tools.file_tools import FileTools
from config import Config


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Orchestrator:
    """Main orchestrator for the Multi-Agent System."""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the orchestrator with all agents.
        
        Args:
            config (Config, optional): Configuration object.
        """
        self.config = config or Config()
        self.planner = PlannerAgent(config=self.config)
        self.coder = CoderAgent(config=self.config)
        self.stats = {
            "files_planned": 0,
            "files_generated": 0,
            "files_saved": 0,
            "errors": 0,
        }
        
        logger.info("✓ Orchestrator initialized")
    
    def orchestrate(self, user_requirement: str) -> Dict[str, Any]:
        """
        Main orchestration workflow.
        
        Args:
            user_requirement (str): Natural language project requirement.
            
        Returns:
            Dict[str, Any]: Results summary including plan and generated files.
        """
        try:
            print("=" * 70)
            print("🚀 Multi-Agent Software Development System")
            print("=" * 70)
            
            # ========== Phase 1: Planning ==========
            print("\n" + "=" * 70)
            print("📍 PHASE 1: PROJECT PLANNING")
            print("=" * 70)
            
            print(f"\n📋 User Requirement:")
            print(f"{user_requirement}")
            
            print(f"\n🔄 Analyzing requirements and generating project plan...")
            plan = self.planner.plan_project(user_requirement)
            
            # Display plan summary
            print("\n" + self.planner.get_plan_summary(plan))
            
            self.stats["files_planned"] = len(plan.get("files", []))
            
            # ========== Phase 2: Code Generation ==========
            print("\n" + "=" * 70)
            print("📍 PHASE 2: CODE GENERATION")
            print("=" * 70)
            
            files = plan.get("files", [])
            print(f"\n🔄 Generating code for {len(files)} files...")
            
            generated_files = {}
            for idx, file_entry in enumerate(files, 1):
                filename = file_entry.get("filename")
                purpose = file_entry.get("purpose")
                priority = file_entry.get("priority", "medium")
                
                print(f"\n  [{idx}/{len(files)}] Generating {filename}...")
                print(f"       Purpose: {purpose}")
                print(f"       Priority: {priority}")
                
                try:
                    # Prepare context for code generation
                    plan_context = self._prepare_context(plan)
                    
                    # Generate code
                    code = self.coder.generate_code(
                        filename=filename,
                        task_description=purpose,
                        full_plan_context=plan_context,
                        language=self._detect_language(filename)
                    )
                    
                    generated_files[filename] = code
                    self.stats["files_generated"] += 1
                    self.stats["files_saved"] += 1
                    print(f"       ✓ Generated ({len(code)} bytes)")
                
                except Exception as e:
                    logger.error(f"❌ Failed to generate {filename}: {e}")
                    self.stats["errors"] += 1
                    print(f"       ✗ Error: {type(e).__name__}")
                    print(f"         {str(e)[:60]}...")
            
            # ========== Phase 3: Summary ==========
            print("\n" + "=" * 70)
            print("📍 PHASE 3: COMPLETION SUMMARY")
            print("=" * 70)
            
            self._print_summary(plan, generated_files)
            
            # ========== Return Results ==========
            return {
                "success": self.stats["errors"] == 0,
                "plan": plan,
                "generated_files": generated_files,
                "statistics": self.stats,
                "workspace_path": str(FileTools.WORKSPACE_DIR),
            }
        
        except Exception as e:
            logger.error(f"❌ Orchestration failed: {e}")
            raise
    
    def _prepare_context(self, plan: Dict[str, Any]) -> str:
        """
        Prepare project context for code generation.
        
        Args:
            plan (Dict): Project plan.
            
        Returns:
            str: Formatted context string.
        """
        context_parts = [
            f"Project: {plan.get('project_name', 'Unknown')}",
            f"Description: {plan.get('description', 'N/A')}",
        ]
        
        tech_stack = plan.get('tech_stack', [])
        if tech_stack:
            context_parts.append(f"Tech Stack: {', '.join(tech_stack)}")
        
        dependencies = plan.get('dependencies', [])
        if dependencies:
            context_parts.append(f"Dependencies: {', '.join(dependencies)}")
        
        return "\n".join(context_parts)
    
    def _detect_language(self, filename: str) -> str:
        """
        Detect programming language from filename.
        
        Args:
            filename (str): Target filename.
            
        Returns:
            str: Detected language.
        """
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
        }
        
        for ext, lang in extension_map.items():
            if filename.endswith(ext):
                return lang
        
        return 'python'  # Default to python
    
    def _print_summary(self, plan: Dict[str, Any], generated_files: Dict[str, str]) -> None:
        """
        Print final summary of the orchestration.
        
        Args:
            plan: Project plan.
            generated_files: Generated code mapping.
        """
        print(f"\n✅ Project Generation Complete!")
        print(f"\n📊 Statistics:")
        print(f"   Files Planned: {self.stats['files_planned']}")
        print(f"   Files Generated: {self.stats['files_generated']}")
        print(f"   Files Saved: {self.stats['files_saved']}")
        print(f"   Errors: {self.stats['errors']}")
        
        if self.stats['errors'] == 0:
            print(f"\n✨ All files generated successfully!")
        
        # Get workspace info
        workspace_info = FileTools.get_workspace_info()
        print(f"\n📁 Workspace Information:")
        print(f"   Location: {workspace_info['workspace_path']}")
        print(f"   Total Files: {workspace_info['file_count']}")
        
        print(f"\n📂 Generated Files:")
        for file in sorted(workspace_info['files']):
            if file != "__init__.py":  # Skip __init__
                file_path = FileTools.WORKSPACE_DIR / file
                size = file_path.stat().st_size
                print(f"   ✓ {file:40s} ({size:6d} bytes)")
        
        print("\n" + "=" * 70)
        print("🎉 Ready to use! Start developing with the generated files.")
        print("=" * 70)


def main():
    """
    Main entry point for the orchestrator.
    
    Define your project requirement here.
    """
    # ========== USER REQUIREMENT ==========
    user_requirement = """
Build a simple arXiv CS Daily website. 
The website should:
1. Display the latest computer science papers from arXiv
2. Support category navigation (cs.AI, cs.CV, cs.NLP)
3. Show paper details including title, authors, abstract, PDF link
4. Provide citation formatting (BibTeX)
5. Have a responsive design for mobile and desktop
6. Use Flask for backend and SQLite for data storage
    """
    
    try:
        # Initialize orchestrator
        orchestrator = Orchestrator()
        
        # Run orchestration
        results = orchestrator.orchestrate(user_requirement)
        
        # Check success
        if results["success"]:
            print("\n✨ Orchestration completed successfully!")
        else:
            print("\n⚠️  Orchestration completed with some errors")
        
        return results
    
    except Exception as e:
        logger.error(f"❌ Fatal error in orchestration: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    results = main()
