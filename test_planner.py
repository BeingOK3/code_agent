#!/usr/bin/env python3
"""
Test Script for Planner Agent
Tests the project planning functionality with the arXiv CS Daily website requirement.
"""

import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.planner import PlannerAgent


def main():
    print("=" * 70)
    print("🧪 Testing Planner Agent with arXiv CS Daily Requirement")
    print("=" * 70)
    
    try:
        # Step 1: Initialize Planner Agent
        print("\n📍 Step 1: Initializing Planner Agent...")
        planner = PlannerAgent()
        print("✓ PlannerAgent initialized")
        
        # Step 2: Define the requirement
        requirement = """Build a simple arXiv CS Daily website. 
It needs a home page with category navigation (cs.AI, cs.CV, cs.NLP), 
and a detail page for papers with links to PDFs and citation information."""
        
        print("\n📍 Step 2: User Requirement:")
        print("-" * 70)
        print(requirement)
        print("-" * 70)
        
        # Step 3: Generate project plan
        print("\n📍 Step 3: Generating Project Plan...")
        plan = planner.plan_project(requirement)
        print("✓ Project plan generated successfully")
        
        # Step 4: Display the JSON object
        print("\n📍 Step 4: Generated Project Plan (JSON):")
        print("-" * 70)
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        print("-" * 70)
        
        # Step 5: Verify file list
        print("\n📍 Step 5: File List Verification:")
        files = plan.get("files", [])
        print(f"Total files: {len(files)}")
        for idx, file_entry in enumerate(files, 1):
            filename = file_entry.get("filename", "Unknown")
            purpose = file_entry.get("purpose", "No description")
            priority = file_entry.get("priority", "unknown")
            print(f"  {idx}. [{priority:8s}] {filename:30s} → {purpose[:40]}...")
        
        # Step 6: Display human-readable summary
        print("\n📍 Step 6: Project Summary:")
        print("-" * 70)
        print(planner.get_plan_summary(plan))
        print("-" * 70)
        
        # Step 7: Validate plan
        print("\n📍 Step 7: Validating Plan Structure...")
        planner.validate_plan(plan)
        print("✓ Plan structure validation passed")
        
        # Step 8: Display project metadata
        print("\n📍 Step 8: Project Metadata:")
        print(f"   Project Name: {plan.get('project_name', 'N/A')}")
        print(f"   Description: {plan.get('description', 'N/A')[:60]}...")
        
        tech_stack = plan.get('tech_stack', [])
        if tech_stack:
            print(f"   Tech Stack: {', '.join(tech_stack)}")
        
        dependencies = plan.get('dependencies', [])
        if dependencies:
            print(f"   Dependencies: {', '.join(dependencies)}")
        
        steps = plan.get('implementation_steps', [])
        if steps:
            print(f"   Implementation Steps: {len(steps)} steps")
        
        print("\n" + "=" * 70)
        print("✅ Planner Agent Test PASSED!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Test FAILED!")
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
