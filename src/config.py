"""
Configuration management for the Personalized Education Assistant.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for managing API keys and settings."""
    
    def __init__(self):
        # API Keys
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        
        # LLM Configuration
        self.default_llm = os.getenv("DEFAULT_LLM", "openrouter")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-4-scout:free")
        self.groq_model = os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
        
        # Default Parameters
        self.default_resources_per_category = int(os.getenv("DEFAULT_RESOURCES_PER_CATEGORY", "3"))
        self.default_quiz_questions = int(os.getenv("DEFAULT_QUIZ_QUESTIONS", "5"))
        self.default_project_count = int(os.getenv("DEFAULT_PROJECT_COUNT", "2"))
    
    def get_llm_config(self, llm_provider: Optional[str] = None):
        """Get LLM configuration based on provider."""
        provider = llm_provider or self.default_llm
        
        if provider == "openrouter":
            # Format model name with provider prefix for LiteLLM
            model_name = self.openrouter_model
            if not model_name.startswith("openrouter/"):
                model_name = f"openrouter/{model_name}"
            
            return {
                "api_key": self.openrouter_api_key,
                "model": model_name,
                "base_url": "https://openrouter.ai/api/v1",
                "provider": "openrouter"
            }
        elif provider == "groq":
            # Format model name with provider prefix for LiteLLM
            model_name = self.groq_model
            if not model_name.startswith("groq/"):
                model_name = f"groq/{model_name}"
            
            return {
                "api_key": self.groq_api_key,
                "model": model_name,
                "base_url": "https://api.groq.com/openai/v1",
                "provider": "groq"
            }
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
    
    def validate_api_keys(self):
        """Validate that required API keys are present."""
        missing_keys = []
        
        if not self.openrouter_api_key:
            missing_keys.append("OPENROUTER_API_KEY")
        if not self.groq_api_key:
            missing_keys.append("GROQ_API_KEY")
        if not self.serper_api_key:
            missing_keys.append("SERPER_API_KEY")
        
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
        
        return True


# Global config instance
config = Config()