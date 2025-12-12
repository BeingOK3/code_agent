"""
Coder Agent Module
Responsible for generating complete, executable code based on project plans and requirements.
"""

import re
import logging
from typing import Optional, Dict, Any
from utils.llm_client import LLMClient
from tools.file_tools import FileTools
from config import Config


logger = logging.getLogger(__name__)


# System prompt for the Coder Agent
CODER_SYSTEM_PROMPT = """You are a Senior Developer with 10+ years of experience.

Your task is to write COMPLETE, PRODUCTION-READY code that is:
1. Fully functional and executable
2. Well-documented with docstrings
3. Following best practices and design patterns
4. Including error handling where appropriate
5. Compatible with the specified dependencies

IMPORTANT - OUTPUT FORMAT REQUIREMENTS:
1. Wrap ALL code in markdown code blocks with the language specified
2. Example for Python: ```python\\n<code>\\n```
3. Example for JavaScript: ```javascript\\n<code>\\n```
4. Example for HTML: ```html\\n<code>\\n```
5. You may include brief explanatory comments BEFORE the code block
6. Do NOT include code outside of markdown blocks
7. Only output ONE code block

GUIDELINES:
- Write complete, importable modules (don't write fragments)
- Include all necessary imports
- Add comprehensive docstrings and comments
- Handle edge cases and errors gracefully
- Follow PEP 8 (Python), ESLint (JavaScript), or standard conventions
- Include example usage if appropriate

Remember: Output must be immediately executable when extracted from the code block."""


class CoderAgent:
    """
    Coder Agent for the Multi-Agent System.
    Generates complete, production-ready code based on project requirements.
    """
    
    def __init__(self, config: Optional[Config] = None, llm_client: Optional[LLMClient] = None):
        """
        Initialize the Coder Agent.
        
        Args:
            config (Config, optional): Configuration object.
            llm_client (LLMClient, optional): LLMClient instance.
        """
        self.config = config or Config()
        self.llm_client = llm_client or LLMClient(config=self.config)
        
        logger.info("✓ CoderAgent initialized")
    
    def generate_code(
        self,
        filename: str,
        task_description: str,
        full_plan_context: Optional[str] = None,
        language: str = "python"
    ) -> str:
        """
        Generate code for a specific file based on task description.
        
        Args:
            filename (str): Target filename (e.g., 'app.py', 'index.html')
            task_description (str): Detailed description of what this file should do
            full_plan_context (str, optional): Project context and related information
            language (str): Programming language (python, javascript, html, etc.)
            
        Returns:
            str: Generated code
            
        Raises:
            ValueError: If code cannot be extracted from response
            Exception: If LLM call fails
        """
        try:
            if not filename or not task_description:
                raise ValueError("filename and task_description are required")
            
            logger.info(f"📝 Generating code for: {filename}")
            
            # Build the prompt
            prompt = self._build_prompt(filename, task_description, full_plan_context, language)
            
            # Call LLM
            logger.debug("🔄 Calling LLM for code generation...")
            response = self.llm_client.chat(
                messages=[
                    {
                        "role": "system",
                        "content": CODER_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more deterministic code
                max_tokens=3000
            )
            
            # Extract code from markdown
            logger.debug("🔍 Extracting code from markdown response...")
            code = self._extract_code_from_markdown(response, language)
            
            # Validate extracted code
            if not code or code.strip() == "":
                raise ValueError("No code could be extracted from LLM response")
            
            # Save code to file
            logger.debug(f"💾 Saving code to workspace...")
            FileTools.save_code(filename, code)
            
            logger.info(f"✓ Code generated and saved for: {filename}")
            return code
        
        except ValueError as e:
            error_msg = f"❌ Validation Error: {str(e)}"
            logger.error(error_msg)
            raise
        
        except Exception as e:
            error_msg = f"❌ Code Generation Error: {type(e).__name__}: {str(e)}"
            logger.error(error_msg)
            raise
    
    def _build_prompt(
        self,
        filename: str,
        task_description: str,
        full_plan_context: Optional[str] = None,
        language: str = "python"
    ) -> str:
        """
        Build the prompt for code generation.
        
        Args:
            filename: Target filename
            task_description: What the file should do
            full_plan_context: Project context
            language: Programming language
            
        Returns:
            str: Complete prompt for the LLM
        """
        prompt = f"""Generate code for: {filename}

File Purpose:
{task_description}

Programming Language: {language}
"""
        
        if full_plan_context:
            prompt += f"""
Project Context:
{full_plan_context}
"""
        
        prompt += """
Requirements:
1. Write COMPLETE, executable code
2. Include all necessary imports
3. Add comprehensive docstrings
4. Follow language conventions and best practices
5. Wrap the code in a markdown code block
6. Do NOT include explanatory text outside the code block

Generate the code now:"""
        
        return prompt
    
    def _extract_code_from_markdown(self, response: str, language: str = "python") -> str:
        """
        Extract clean code from markdown-formatted response.
        
        Handles various markdown code block formats:
        - ```python ... ```
        - ```python\\n ... \\n```
        - ``` ... ```
        - No markdown (plain code)
        
        Args:
            response (str): Raw response from LLM
            language (str): Expected language hint
            
        Returns:
            str: Extracted clean code
            
        Raises:
            ValueError: If no code block can be found
        """
        try:
            # Normalize the response
            lines = response.split('\n')
            
            # Pattern 1: Try to find markdown code blocks with language specified
            code_block_pattern = rf"```{language}\s*(.*?)```"
            match = re.search(code_block_pattern, response, re.DOTALL)
            if match:
                code = match.group(1).strip()
                if code:
                    logger.debug("✓ Code extracted from ```<language> block")
                    return code
            
            # Pattern 2: Try to find generic markdown code blocks
            generic_pattern = r"```\s*(.*?)```"
            match = re.search(generic_pattern, response, re.DOTALL)
            if match:
                code = match.group(1).strip()
                if code:
                    logger.debug("✓ Code extracted from generic ``` block")
                    return code
            
            # Pattern 3: Look for code lines (indented or otherwise structured)
            # This handles cases where the LLM might not use markdown
            code_lines = []
            in_code = False
            
            for line in lines:
                # Start of code section
                if line.strip().startswith("```"):
                    in_code = not in_code
                    continue
                
                if in_code or (len(line) > 0 and (line[0] == ' ' or line[0] == '\t')):
                    code_lines.append(line)
            
            if code_lines:
                code = '\n'.join(code_lines).strip()
                if code:
                    logger.debug("✓ Code extracted from indented block")
                    return code
            
            # Pattern 4: If nothing found, check if the entire response is code
            # (e.g., if LLM didn't use markdown despite instructions)
            if response.strip() and not response.strip().startswith('#'):
                # Check if it looks like code (contains keywords)
                code_keywords = ['def ', 'class ', 'import ', 'function ', 'const ', 'let ', '<html', '<?php']
                if any(keyword in response for keyword in code_keywords):
                    logger.debug("✓ Response appears to be code without markdown")
                    return response.strip()
            
            # No code found
            raise ValueError(
                f"Could not extract code block from response. "
                f"Response preview: {response[:100]}..."
            )
        
        except ValueError as e:
            raise
        except Exception as e:
            logger.error(f"❌ Code Extraction Error: {str(e)}")
            raise ValueError(f"Failed to extract code: {str(e)}") from e
    
    def generate_multiple(
        self,
        file_specs: list,
        full_plan_context: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate code for multiple files.
        
        Args:
            file_specs (list): List of dicts with 'filename', 'description', 'language' keys
            full_plan_context (str, optional): Shared project context
            
        Returns:
            Dict[str, str]: Mapping of filename to generated code
        """
        results = {}
        
        for spec in file_specs:
            try:
                filename = spec.get("filename")
                description = spec.get("description")
                language = spec.get("language", "python")
                
                code = self.generate_code(
                    filename=filename,
                    task_description=description,
                    full_plan_context=full_plan_context,
                    language=language
                )
                
                results[filename] = code
                logger.info(f"✓ Generated: {filename}")
            
            except Exception as e:
                logger.error(f"❌ Failed to generate {spec.get('filename')}: {e}")
                results[filename] = None
        
        return results


if __name__ == "__main__":
    # Test the Coder Agent
    try:
        print("=" * 70)
        print("🧪 Testing Coder Agent")
        print("=" * 70)
        
        # Initialize Coder Agent
        coder = CoderAgent()
        
        # Test 1: Generate a simple Python module
        print("\n📍 Test 1: Generating Python module...")
        
        task1 = """Create a Python utility module for handling arXiv API interactions.
Include:
1. A function to fetch papers from arXiv by category
2. Error handling for network issues
3. Data parsing and formatting
4. Comprehensive docstrings"""
        
        code1 = coder.generate_code(
            filename="arxiv_utils.py",
            task_description=task1,
            full_plan_context="arXiv CS Daily website project",
            language="python"
        )
        
        print(f"\n✓ Generated Python code ({len(code1)} chars)")
        print("Code preview:")
        print(code1[:200] + "...\n")
        
        # Test 2: Generate HTML template
        print("📍 Test 2: Generating HTML template...")
        
        task2 = """Create an HTML template for the paper detail page.
Include:
1. Paper title, authors, abstract
2. PDF download link
3. Citation information (BibTeX format)
4. Related papers suggestion
5. Responsive design structure"""
        
        code2 = coder.generate_code(
            filename="templates/paper_detail.html",
            task_description=task2,
            full_plan_context="arXiv CS Daily website using Flask",
            language="html"
        )
        
        print(f"\n✓ Generated HTML code ({len(code2)} chars)")
        print("Code preview:")
        print(code2[:200] + "...\n")
        
        print("=" * 70)
        print("✅ Coder Agent Test Successful!")
        print("=" * 70)
    
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
