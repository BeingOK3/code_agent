"""
LLM Client Module
Handles all communication with LLM APIs (DeepSeek, OpenAI, etc.)
Provides a unified interface for calling language models.
"""

import logging
from typing import Optional, List, Dict, Any
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from config import Config


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMClient:
    """
    Unified LLM Client for interacting with various LLM providers.
    Currently supports DeepSeek (via OpenAI-compatible API) and OpenAI.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the LLM Client.
        
        Args:
            config (Config, optional): Configuration object. If None, creates a new Config instance.
            
        Raises:
            ValueError: If configuration is invalid or API key is missing.
        """
        self.config = config or Config()
        
        # Initialize OpenAI-compatible client
        self.client = OpenAI(
            api_key=self.config.LLM_API_KEY,
            base_url=self.config.LLM_BASE_URL,
        )
        
        self.model = self.config.LLM_MODEL
        self.provider = self.config.LLM_PROVIDER
        
        logger.info(f"✓ LLMClient initialized with {self.provider.upper()} ({self.model})")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        model: Optional[str] = None,
    ) -> str:
        """
        Send a chat request to the LLM and return the response content.
        
        Args:
            messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content'.
                Example: [{"role": "system", "content": "You are..."}, 
                          {"role": "user", "content": "Hello"}]
            temperature (float): Controls randomness (0.0-2.0). Default: 0.7
            max_tokens (int, optional): Maximum tokens in response. If None, uses API default.
            model (str, optional): Specific model to use. If None, uses configured default.
            
        Returns:
            str: The response content from the LLM.
            
        Raises:
            ValueError: If messages format is invalid.
            APIError: If the API call fails (caught and logged).
        """
        try:
            # Validate messages format
            if not isinstance(messages, list) or len(messages) == 0:
                raise ValueError("messages must be a non-empty list of dictionaries")
            
            # Validate each message
            for msg in messages:
                if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                    raise ValueError(
                        "Each message must be a dict with 'role' and 'content' keys"
                    )
            
            # Use provided model or default
            model_to_use = model or self.model
            
            logger.debug(f"🔄 Calling {self.provider} API...")
            logger.debug(f"   Messages: {len(messages)} messages")
            logger.debug(f"   Temperature: {temperature}")
            logger.debug(f"   Max tokens: {max_tokens}")
            
            # Prepare API call parameters
            api_params = {
                "model": model_to_use,
                "messages": messages,
                "temperature": temperature,
            }
            
            if max_tokens is not None:
                api_params["max_tokens"] = max_tokens
            
            # Call the API
            response = self.client.chat.completions.create(**api_params)
            
            # Extract response content
            content = response.choices[0].message.content
            
            logger.debug(f"✓ Response received ({len(content)} characters)")
            return content
        
        except APIConnectionError as e:
            error_msg = f"❌ Connection Error: Failed to connect to {self.config.LLM_BASE_URL}"
            logger.error(error_msg)
            logger.error(f"   Details: {str(e)}")
            raise
        
        except RateLimitError as e:
            error_msg = f"❌ Rate Limit Error: API rate limit exceeded"
            logger.error(error_msg)
            logger.error(f"   Details: {str(e)}")
            logger.info("   💡 Tip: Wait a moment and try again")
            raise
        
        except APIError as e:
            error_msg = f"❌ API Error: {str(e)}"
            logger.error(error_msg)
            if hasattr(e, "status_code"):
                logger.error(f"   Status Code: {e.status_code}")
            raise
        
        except ValueError as e:
            error_msg = f"❌ Validation Error: {str(e)}"
            logger.error(error_msg)
            raise
        
        except Exception as e:
            error_msg = f"❌ Unexpected Error: {type(e).__name__}: {str(e)}"
            logger.error(error_msg)
            raise
    
    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        model: Optional[str] = None,
    ):
        """
        Send a chat request with streaming response.
        
        Args:
            messages (List[Dict[str, str]]): List of message dictionaries.
            temperature (float): Controls randomness. Default: 0.7
            max_tokens (int, optional): Maximum tokens in response.
            model (str, optional): Specific model to use.
            
        Yields:
            str: Streamed response chunks.
        """
        try:
            model_to_use = model or self.model
            
            logger.debug(f"🔄 Calling {self.provider} API (streaming)...")
            
            api_params = {
                "model": model_to_use,
                "messages": messages,
                "temperature": temperature,
                "stream": True,
            }
            
            if max_tokens is not None:
                api_params["max_tokens"] = max_tokens
            
            response = self.client.chat.completions.create(**api_params)
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            logger.error(f"❌ Streaming Error: {str(e)}")
            raise
    
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for a given text.
        
        Note: This is a rough estimate. Actual token count may vary.
        
        Args:
            text (str): Text to estimate tokens for.
            
        Returns:
            int: Estimated token count.
        """
        # Simple estimation: ~1 token per 4 characters
        return len(text) // 4
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get current model information.
        
        Returns:
            dict: Model configuration and metadata.
        """
        return {
            "provider": self.provider,
            "model": self.model,
            "base_url": self.config.LLM_BASE_URL,
            "api_key_preview": f"{self.config.LLM_API_KEY[:10]}...{self.config.LLM_API_KEY[-10:]}",
        }


if __name__ == "__main__":
    # Test the LLM Client
    try:
        print("="*50)
        print("🧪 Testing LLM Client")
        print("="*50)
        
        # Initialize client
        client = LLMClient()
        print(f"\n✓ Client initialized")
        print(f"  Info: {client.get_model_info()}")
        
        # Test chat method
        print(f"\n🔄 Testing chat method...")
        response = client.chat(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Keep responses concise.",
                },
                {"role": "user", "content": "Say 'Hello, World!' and nothing else."},
            ],
            temperature=0.5,
        )
        
        print(f"\n✓ Response received:")
        print(f"  {response}")
        
        print(f"\n✓ Token estimate: {client.count_tokens(response)} tokens")
        print("\n" + "="*50)
        print("✅ LLM Client Test Successful!")
        print("="*50)
    
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
