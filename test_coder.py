#!/usr/bin/env python3
"""
Test Script for Coder Agent
Tests code generation with mock LLM responses to verify extraction logic.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.coder import CoderAgent
from tools.file_tools import FileTools
import re


def test_code_extraction():
    """Test the markdown code extraction functionality."""
    print("=" * 70)
    print("🧪 Testing Coder Agent Code Extraction")
    print("=" * 70)
    
    coder = CoderAgent()
    
    # Test cases with different markdown formats
    test_cases = [
        {
            "name": "Python code block with language specified",
            "input": '''```python
def hello_world():
    """Print hello world."""
    print("Hello, World!")
```''',
            "language": "python",
            "should_contain": "def hello_world"
        },
        {
            "name": "Generic code block",
            "input": '''```
def greet(name):
    return f"Hello, {name}"
```''',
            "language": "python",
            "should_contain": "def greet"
        },
        {
            "name": "Code with explanation before",
            "input": '''Here's a simple function:

```python
def add(a, b):
    """Add two numbers."""
    return a + b
```''',
            "language": "python",
            "should_contain": "def add"
        },
        {
            "name": "HTML code block",
            "input": '''```html
<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>Hello</body>
</html>
```''',
            "language": "html",
            "should_contain": "<!DOCTYPE html>"
        },
        {
            "name": "JavaScript code block",
            "input": '''```javascript
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```''',
            "language": "javascript",
            "should_contain": "function fibonacci"
        }
    ]
    
    print("\n📝 Running extraction tests...")
    passed = 0
    failed = 0
    
    for idx, test_case in enumerate(test_cases, 1):
        print(f"\n  Test {idx}: {test_case['name']}")
        try:
            extracted = coder._extract_code_from_markdown(
                test_case["input"],
                test_case["language"]
            )
            
            if test_case["should_contain"] in extracted:
                print(f"    ✓ PASSED")
                passed += 1
            else:
                print(f"    ✗ FAILED: Expected '{test_case['should_contain']}' not found")
                print(f"      Got: {extracted[:50]}...")
                failed += 1
        
        except Exception as e:
            print(f"    ✗ FAILED: {e}")
            failed += 1
    
    print(f"\n  Results: {passed} passed, {failed} failed")
    
    return passed, failed


def test_code_generation_simulation():
    """Simulate code generation by manually testing the save functionality."""
    print("\n" + "=" * 70)
    print("🧪 Testing Code Generation & File Saving")
    print("=" * 70)
    
    coder = CoderAgent()
    
    # Simulated generated code samples
    test_files = [
        {
            "filename": "utils/arxiv_client.py",
            "code": '''"""
arXiv API Client Module
Handles communication with arXiv API.
"""

import requests
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ArxivClient:
    """Client for fetching papers from arXiv."""
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    def __init__(self, max_retries: int = 3):
        """Initialize the ArXiv client."""
        self.max_retries = max_retries
        self.session = requests.Session()
    
    def search_by_category(
        self, 
        category: str, 
        days: int = 1, 
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for papers in a specific category.
        
        Args:
            category: arXiv category (e.g., 'cs.AI')
            days: Number of days back to search
            max_results: Maximum results to return
            
        Returns:
            List of paper data dictionaries
        """
        try:
            # Build query
            date_from = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
            query = f'cat:{category} AND submittedDate:[{date_from}000000 TO 9999999999]'
            
            # Make request
            params = {
                'search_query': query,
                'start': 0,
                'max_results': max_results,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }
            
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse response (simplified)
            papers = []
            # TODO: Parse XML response and extract paper data
            
            return papers
        
        except Exception as e:
            logger.error(f"Error searching arXiv: {e}")
            raise


if __name__ == "__main__":
    client = ArxivClient()
    papers = client.search_by_category("cs.AI", days=1)
    print(f"Found {len(papers)} papers")
'''
        },
        {
            "filename": "models.py",
            "code": '''"""
Database Models
Defines SQLAlchemy models for the application.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Paper(db.Model):
    """Model for arXiv papers."""
    
    __tablename__ = 'papers'
    
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.String(1000), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    published_date = db.Column(db.DateTime, nullable=False)
    pdf_url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Paper {self.id}: {self.title}>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'summary': self.summary,
            'published_date': self.published_date.isoformat(),
            'pdf_url': self.pdf_url,
            'category': self.category,
        }


class Category(db.Model):
    """Model for arXiv categories."""
    
    __tablename__ = 'categories'
    
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f"<Category {self.id}: {self.name}>"
'''
        }
    ]
    
    print("\n📝 Simulating code generation and file saving...")
    
    for test_file in test_files:
        try:
            print(f"\n  Saving: {test_file['filename']}")
            FileTools.save_code(test_file['filename'], test_file['code'])
            
            # Verify file was saved
            if FileTools.file_exists(test_file['filename']):
                # Read back and verify
                saved_code = FileTools.read_code(test_file['filename'])
                if saved_code == test_file['code']:
                    print(f"    ✓ File saved and verified ({len(saved_code)} bytes)")
                else:
                    print(f"    ✗ Saved code doesn't match original")
            else:
                print(f"    ✗ File not found after saving")
        
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    # List all generated files
    print("\n  📂 Generated files in workspace:")
    files = FileTools.list_files()
    for file in sorted(files):
        if file != "__init__.py":  # Skip init
            print(f"      ✓ {file}")
    
    print(f"\n  Total files: {len(files)}")


def main():
    try:
        # Test 1: Code extraction
        passed, failed = test_code_extraction()
        
        # Test 2: Code generation simulation
        test_code_generation_simulation()
        
        # Summary
        print("\n" + "=" * 70)
        if failed == 0:
            print("✅ All Coder Agent Tests PASSED!")
        else:
            print(f"⚠️  {failed} test(s) failed")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
