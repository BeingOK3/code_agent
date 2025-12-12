#!/usr/bin/env python3
"""
Quick API Connection Test
Verifies that the LLMClient can successfully connect to and communicate with the LLM API.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.llm_client import LLMClient


def main():
    print("=" * 60)
    print("🧪 Testing LLM API Connection")
    print("=" * 60)
    
    try:
        # Step 1: Initialize LLM Client
        print("\n📍 Step 1: Initializing LLMClient...")
        client = LLMClient()
        print("✓ LLMClient initialized successfully")
        
        # Step 2: Get model info
        print("\n📍 Step 2: Model Information:")
        info = client.get_model_info()
        print(f"   Provider: {info['provider'].upper()}")
        print(f"   Model: {info['model']}")
        print(f"   Base URL: {info['base_url']}")
        print(f"   API Key: {info['api_key_preview']}")
        
        # Step 3: Send test message
        print("\n📍 Step 3: Sending test message...")
        response = client.chat(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Respond concisely."
                },
                {
                    "role": "user",
                    "content": "Hello, represent yourself"
                }
            ],
            temperature=0.7
        )
        
        print("✓ Response received successfully!")
        
        # Step 4: Display response
        print("\n📍 Step 4: LLM Response:")
        print("-" * 60)
        print(response)
        print("-" * 60)
        
        # Step 5: Summary
        print("\n📍 Step 5: Summary:")
        print(f"   Response length: {len(response)} characters")
        print(f"   Estimated tokens: {client.count_tokens(response)}")
        
        print("\n" + "=" * 60)
        print("✅ API Connection Test PASSED!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test FAILED!")
        print(f"Error: {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
