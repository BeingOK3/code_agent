"""
LLM Client Usage Examples
Demonstrates how to use the LLMClient class.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.llm_client import LLMClient
from config import Config


def example_basic_chat():
    """Example: Basic chat interaction."""
    print("📍 Example 1: Basic Chat")
    print("-" * 50)
    
    client = LLMClient()
    
    response = client.chat(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful Python expert.",
            },
            {
                "role": "user",
                "content": "What is a list comprehension in Python? (One sentence)",
            },
        ],
        temperature=0.5,
    )
    
    print(f"Response:\n{response}\n")


def example_system_prompt():
    """Example: Using different system prompts."""
    print("📍 Example 2: Different System Prompts")
    print("-" * 50)
    
    client = LLMClient()
    
    # Code generator prompt
    code_response = client.chat(
        messages=[
            {
                "role": "system",
                "content": "You are a senior Python developer. Write clean, efficient code with docstrings.",
            },
            {
                "role": "user",
                "content": "Write a function to check if a number is prime.",
            },
        ],
        temperature=0.3,
        max_tokens=200,
    )
    
    print(f"Generated Code:\n{code_response}\n")


def example_multi_turn():
    """Example: Multi-turn conversation."""
    print("📍 Example 3: Multi-turn Conversation")
    print("-" * 50)
    
    client = LLMClient()
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant specializing in web development.",
        },
        {
            "role": "user",
            "content": "What is React?",
        },
    ]
    
    # First turn
    response1 = client.chat(messages=messages, temperature=0.7)
    print(f"Assistant (Turn 1):\n{response1}\n")
    
    # Add assistant response to messages
    messages.append({
        "role": "assistant",
        "content": response1,
    })
    
    # Second turn
    messages.append({
        "role": "user",
        "content": "How is it different from Vue.js?",
    })
    
    response2 = client.chat(messages=messages, temperature=0.7)
    print(f"Assistant (Turn 2):\n{response2}\n")


def example_error_handling():
    """Example: Error handling."""
    print("📍 Example 4: Error Handling")
    print("-" * 50)
    
    client = LLMClient()
    
    try:
        # Invalid messages format
        response = client.chat(
            messages=[],  # Empty messages will raise error
        )
    except ValueError as e:
        print(f"✓ Caught expected error: {e}\n")


if __name__ == "__main__":
    print("=" * 50)
    print("🧪 LLM Client Usage Examples")
    print("=" * 50)
    print()
    
    try:
        example_basic_chat()
        example_system_prompt()
        example_multi_turn()
        example_error_handling()
        
        print("=" * 50)
        print("✅ All examples completed successfully!")
        print("=" * 50)
    except Exception as e:
        print(f"❌ Error: {e}")
