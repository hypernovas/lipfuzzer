"""
LLM module for LipFuzzer.

Provides abstraction for different LLM providers to generate voice commands.
"""

from .base import LLMProvider

# Import providers with graceful fallbacks
try:
    from .litellm_provider import LiteLLMProvider
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False

try:
    from .openai_llm import OpenAIProvider
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from .gemini_llm import GeminiProvider
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from .prompts import PromptManager, PromptTemplate
    PROMPTS_AVAILABLE = True
except ImportError:
    PROMPTS_AVAILABLE = False


__all__ = ['LLMProvider', 'PromptManager', 'PromptTemplate']

# Conditionally add available providers
if LITELLM_AVAILABLE:
    __all__.append('LiteLLMProvider')
if OPENAI_AVAILABLE:
    __all__.append('OpenAIProvider')
if GEMINI_AVAILABLE:
    __all__.append('GeminiProvider')


def create_llm_client(provider: str = None, **kwargs):
    """
    Factory function to create an LLM client.
    
    Args:
        provider: Provider name ('litellm', 'openai', 'gemini')
                 If None, uses config default
        **kwargs: Additional initialization parameters
        
    Returns:
        Configured LLM provider instance
        
    Raises:
        ImportError: If required provider is not available
        ValueError: If provider is invalid
    """
    from config import get_config
    
    config = get_config()
    provider = provider or config.llm_provider
    
    if provider == 'litellm':
        if not LITELLM_AVAILABLE:
            raise ImportError(
                "LiteLLM not available. Install with: pip install litellm"
            )
        return LiteLLMProvider(**kwargs)
    
    elif provider == 'openai':
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI not available. Install with: pip install openai"
            )
        return OpenAIProvider(**kwargs)
    
    elif provider == 'gemini':
        if not GEMINI_AVAILABLE:
            raise ImportError(
                "Gemini not available. Install with: pip install google-generativeai"
            )
        return GeminiProvider(**kwargs)
    
    else:
        raise ValueError(
            f"Unknown provider '{provider}'. "
            f"Choose from: litellm, openai, gemini"
        )
