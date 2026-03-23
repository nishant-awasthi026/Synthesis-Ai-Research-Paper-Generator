"""
Ollama client for local LLM inference
"""
import requests
from typing import Dict, Any, Optional
from backend.config import settings

class OllamaClient:
    def __init__(self):
        """Initialize Ollama client"""
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        print(f"🤖 Ollama client initialized: {self.model}")
    
    def generate(
        self, 
        prompt: str, 
        temperature: float = None,
        max_tokens: int = None,
        system_prompt: str = None
    ) -> Dict[str, Any]:
        """
        Generate text using Ollama
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            system_prompt: Optional system prompt
            
        Returns:
            Generated response dictionary
        """
        temperature = temperature or settings.OLLAMA_TEMPERATURE
        max_tokens = max_tokens or settings.OLLAMA_MAX_TOKENS
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False,
            "options": {
                "num_predict": max_tokens
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            return {
                "error": "Ollama is not running. Please start Ollama and ensure the model is available.",
                "response": ""
            }
        except Exception as e:
            return {
                "error": str(e),
                "response": ""
            }
    
    def generate_stream(self, prompt: str):
        """Generate text with streaming (for real-time UI updates)"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=120
            )
            
            for line in response.iter_lines():
                if line:
                    yield line.decode('utf-8')
        except Exception as e:
            yield f'{{"error": "{str(e)}"}}'
    
    def check_health(self) -> Dict[str, Any]:
        """Check if Ollama is running and model is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            data = response.json()
            
            # Check if our model is available
            models = [m['name'] for m in data.get('models', [])]
            model_available = self.model in models
            
            return {
                "status": "healthy" if model_available else "model_not_found",
                "ollama_running": True,
                "model": self.model,
                "model_available": model_available,
                "available_models": models
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "offline",
                "ollama_running": False,
                "model": self.model,
                "model_available": False,
                "error": "Ollama is not running"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

# Singleton instance
_ollama_client = None

def get_ollama_client() -> OllamaClient:
    """Get or create Ollama client singleton"""
    global _ollama_client
    if _ollama_client is None:
        _ollama_client = OllamaClient()
    return _ollama_client
