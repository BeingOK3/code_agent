"""
Planner Agent Module
Responsible for analyzing user requirements and generating project plans.
Outputs structured JSON containing file structure and development tasks.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from utils.llm_client import LLMClient
from config import Config


logger = logging.getLogger(__name__)


# System prompt for the Planner Agent
# CRITICAL: Instructs the LLM to output ONLY valid JSON without markdown formatting
PLANNER_SYSTEM_PROMPT = """You are an Expert Software Architect and Project Planner.

Your task is to analyze user requirements and generate a detailed project plan.

IMPORTANT - OUTPUT REQUIREMENTS:
1. Output ONLY valid JSON. No markdown, no code blocks, no comments.
2. Do NOT wrap JSON in triple backticks (```json or ```)
3. Do NOT add any text before or after the JSON
4. The JSON must be valid and parseable by Python's json.loads()

JSON Output Structure:
{
    "project_name": "string - descriptive project name",
    "description": "string - 2-3 sentence project overview",
    "tech_stack": ["string - technologies to use"],
    "files": [
        {
            "filename": "string - relative path like 'src/main.py'",
            "purpose": "string - brief description of file purpose",
            "priority": "string - 'critical', 'high', or 'medium'"
        }
    ],
    "dependencies": [
        "string - required Python packages or external libraries"
    ],
    "implementation_steps": [
        "string - step 1 of development plan",
        "string - step 2 of development plan"
    ],
    "summary": "string - brief summary of the entire plan"
}

Example valid output (with no extra text):
{"project_name": "Example App", "description": "A simple app", "tech_stack": ["Python", "Flask"], "files": [{"filename": "app.py", "purpose": "Main application", "priority": "critical"}], "dependencies": ["flask"], "implementation_steps": ["Setup", "Code"], "summary": "Simple app"}

Remember: Output JSON ONLY. No additional text, explanation, or markdown formatting."""


class PlannerAgent:
    """
    Planner Agent for the Multi-Agent System.
    Analyzes user requirements and generates structured project plans.
    """
    
    def __init__(self, config: Optional[Config] = None, llm_client: Optional[LLMClient] = None):
        """
        Initialize the Planner Agent.
        
        Args:
            config (Config, optional): Configuration object. If None, creates a new Config instance.
            llm_client (LLMClient, optional): LLMClient instance. If None, creates a new instance.
        """
        self.config = config or Config()
        self.llm_client = llm_client or LLMClient(config=self.config)
        
        logger.info("✓ PlannerAgent initialized")
    
    def plan_project(self, user_requirement: str) -> Dict[str, Any]:
        """
        Generate a project plan based on user requirements.
        
        Args:
            user_requirement (str): Natural language description of the project.
            
        Returns:
            Dict[str, Any]: Parsed project plan as a Python dictionary.
            
        Raises:
            ValueError: If the LLM response cannot be parsed as valid JSON.
            Exception: If the LLM API call fails.
        """
        try:
            if not user_requirement or not isinstance(user_requirement, str):
                raise ValueError("user_requirement must be a non-empty string")
            
            logger.info(f"📋 Planning project based on requirement: {user_requirement[:50]}...")
            
            # Prepare the messages for the LLM
            messages = [
                {
                    "role": "system",
                    "content": PLANNER_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"Please create a comprehensive project plan for:\n\n{user_requirement}"
                }
            ]
            
            # Call the LLM
            logger.debug("🔄 Calling LLM for project planning...")
            response = self.llm_client.chat(
                messages=messages,
                temperature=0.3,  # Lower temperature for more deterministic output
                max_tokens=2000
            )
            
            # Parse the JSON response
            logger.debug("📝 Parsing JSON response...")
            plan = self._parse_response(response)
            
            logger.info("✓ Project plan generated successfully")
            return plan
        
        except json.JSONDecodeError as e:
            error_msg = f"❌ JSON Parsing Error: Failed to parse LLM response as JSON"
            logger.error(error_msg)
            logger.error(f"   Error details: {str(e)}")
            logger.error(f"   Response preview: {response[:200]}...")
            raise ValueError(error_msg) from e
        
        except ValueError as e:
            error_msg = f"❌ Validation Error: {str(e)}"
            logger.error(error_msg)
            raise
        
        except Exception as e:
            error_msg = f"❌ Planning Error: {type(e).__name__}: {str(e)}"
            logger.error(error_msg)
            raise
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse and validate the LLM response as JSON.
        
        Args:
            response (str): Raw response from the LLM.
            
        Returns:
            Dict[str, Any]: Parsed and validated project plan.
            
        Raises:
            json.JSONDecodeError: If the response is not valid JSON.
            ValueError: If the JSON structure is invalid.
        """
        # Clean up the response (remove potential markdown formatting)
        cleaned_response = response.strip()
        
        # Remove markdown code blocks if present
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        
        cleaned_response = cleaned_response.strip()
        
        # Parse JSON
        try:
            plan = json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON. Raw response:\n{cleaned_response[:300]}")
            raise
        
        # Validate required fields
        required_fields = ["project_name", "files", "summary"]
        for field in required_fields:
            if field not in plan:
                raise ValueError(f"Missing required field in plan: '{field}'")
        
        # Validate files structure
        if not isinstance(plan["files"], list):
            raise ValueError("'files' must be a list")
        
        for file_entry in plan["files"]:
            if not isinstance(file_entry, dict):
                raise ValueError("Each file entry must be a dictionary")
            if "filename" not in file_entry or "purpose" not in file_entry:
                raise ValueError("Each file entry must have 'filename' and 'purpose'")
        
        logger.debug(f"✓ Plan validation passed")
        return plan
    
    def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """
        Validate the structure of a project plan.
        
        Args:
            plan (Dict[str, Any]): Project plan dictionary to validate.
            
        Returns:
            bool: True if the plan is valid.
            
        Raises:
            ValueError: If the plan structure is invalid.
        """
        try:
            self._validate_plan_structure(plan)
            return True
        except ValueError as e:
            logger.error(f"❌ Plan validation failed: {e}")
            raise
    
    def _validate_plan_structure(self, plan: Dict[str, Any]) -> None:
        """
        Internal method to validate plan structure.
        
        Args:
            plan (Dict[str, Any]): Plan to validate.
            
        Raises:
            ValueError: If structure is invalid.
        """
        required_fields = ["project_name", "files", "summary"]
        for field in required_fields:
            if field not in plan:
                raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(plan["files"], list) or len(plan["files"]) == 0:
            raise ValueError("'files' must be a non-empty list")
        
        for idx, file_entry in enumerate(plan["files"]):
            if not isinstance(file_entry, dict):
                raise ValueError(f"File entry {idx} is not a dictionary")
            if "filename" not in file_entry or "purpose" not in file_entry:
                raise ValueError(f"File entry {idx} missing 'filename' or 'purpose'")
    
    def get_plan_summary(self, plan: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the plan.
        
        Args:
            plan (Dict[str, Any]): Project plan dictionary.
            
        Returns:
            str: Formatted plan summary.
        """
        summary = []
        summary.append(f"📋 Project: {plan.get('project_name', 'Unknown')}")
        summary.append(f"📝 Description: {plan.get('description', 'N/A')}")
        
        tech_stack = plan.get('tech_stack', [])
        if tech_stack:
            summary.append(f"🛠️  Tech Stack: {', '.join(tech_stack)}")
        
        files = plan.get('files', [])
        summary.append(f"📂 Files ({len(files)}):")
        for file_entry in files:
            priority = file_entry.get('priority', 'medium')
            summary.append(f"   - {file_entry['filename']} [{priority}]: {file_entry['purpose']}")
        
        dependencies = plan.get('dependencies', [])
        if dependencies:
            summary.append(f"📦 Dependencies: {', '.join(dependencies)}")
        
        steps = plan.get('implementation_steps', [])
        if steps:
            summary.append(f"📌 Implementation Steps:")
            for idx, step in enumerate(steps, 1):
                summary.append(f"   {idx}. {step}")
        
        summary.append(f"\n📄 Summary: {plan.get('summary', 'N/A')}")
        
        return "\n".join(summary)


if __name__ == "__main__":
    # Test the Planner Agent
    try:
        print("=" * 60)
        print("🧪 Testing Planner Agent")
        print("=" * 60)
        
        # Initialize Planner Agent
        planner = PlannerAgent()
        
        # Test requirement
        requirement = """
        Create a simple Python web scraper that:
        1. Fetches data from a public API
        2. Saves the data to a JSON file
        3. Has basic error handling
        4. Includes unit tests
        """
        
        print(f"\n📋 User Requirement:")
        print(requirement)
        
        print(f"\n🔄 Generating project plan...")
        plan = planner.plan_project(requirement)
        
        print(f"\n✓ Plan generated successfully!")
        
        # Display the plan
        print("\n" + planner.get_plan_summary(plan))
        
        # Validate the plan
        planner.validate_plan(plan)
        print(f"\n✓ Plan structure validation passed")
        
        print("\n" + "=" * 60)
        print("✅ Planner Agent Test Successful!")
        print("=" * 60)
    
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
