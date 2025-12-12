#!/usr/bin/env python3
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
    print("\n📍 Step 1: Planning Phase...")
    plan = planner.generate_plan(user_request)
    print(f"✓ Plan generated: {plan}")
    
    # Step 2: Code Generation
    print("\n📍 Step 2: Code Generation Phase...")
    for task in plan.get("tasks", []):
        print(f"  Executing: {task}")
        code = coder.generate_code(task)
        print(f"  ✓ Generated code for: {task}")
    
    # Step 3: Review (Optional)
    print("\n📍 Step 3: Review Phase (Optional)...")
    print("✓ System ready for code review")
    
    print("\n" + "=" * 50)
    print("✅ Multi-Agent System Execution Complete!")


if __name__ == "__main__":
    main()
