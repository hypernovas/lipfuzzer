"""
LiteLLM provider implementation.

LiteLLM provides a unified interface to 100+ LLM providers including
OpenAI, Anthropic, Google, Azure, local models, and more.
"""

from typing import List, Dict, Optional, Any
from .base import LLMProvider

try:
    import litellm
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False
    print("Warning: litellm not installed. Run: pip install litellm")


class LiteLLMProvider(LLMProvider):
    """LiteLLM unified interface provider."""
    
    def __init__(self, 
                 model: Optional[str] = None,
                 api_key: Optional[str] = None,
                 temperature: Optional[float] = None,
                 max_tokens: Optional[int] = None):
        """
        Initialize LiteLLM provider.
        
        Args:
            model: Model name (e.g., 'gpt-3.5-turbo', 'claude-3', 'gemini-pro')
            api_key: API key (if None, loads from config or environment)
            temperature: Generation temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
        """
        if not LITELLM_AVAILABLE:
            raise ImportError(
                "litellm is required. Install with: pip install litellm"
            )
        
        from config import get_config
        config = get_config()
        
        self.model = model or config.llm_model
        self.temperature = temperature if temperature is not None else config.llm_temperature
        self.max_tokens = max_tokens or config.llm_max_tokens
        
        # Set API key based on model provider
        # LiteLLM automatically reads from environment, but we can set explicitly
        if api_key:
            if 'gpt' in self.model or 'openai' in self.model:
                import os
                os.environ['OPENAI_API_KEY'] = api_key
            elif 'claude' in self.model or 'anthropic' in self.model:
                import os
                os.environ['ANTHROPIC_API_KEY'] = api_key
            elif 'gemini' in self.model:
                import os
                os.environ['GEMINI_API_KEY'] = api_key
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text from a single prompt.
        
        Args:
            prompt: The prompt text
            **kwargs: Override temperature, max_tokens, etc.
            
        Returns:
            Generated text string
        """
        try:
            response = litellm.completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get('temperature', self.temperature),
                max_tokens=kwargs.get('max_tokens', self.max_tokens)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating text: {e}")
            return ""
    
    def generate_batch(self, prompts: List[str], **kwargs) -> List[str]:
        """
        Generate text from multiple prompts.
        
        Args:
            prompts: List of prompt texts
            **kwargs: Override temperature, max_tokens, etc.
            
        Returns:
            List of generated text strings
        """
        results = []
        
        for prompt in prompts:
            result = self.generate(prompt, **kwargs)
            results.append(result)
        
        return results
    
    def generate_commands(self, 
                         context: Dict[str, Any], 
                         template: str, 
                         count: int = 10,
                         **kwargs) -> List[str]:
        """
        Generate voice commands using a template and context.
        
        Args:
            context: Dictionary with template variables
            template: Template name or prompt string
            count: Number of commands to generate
            **kwargs: Additional parameters
            
        Returns:
            List of generated voice command strings
        """
        try:
            # Load prompt manager to render template
            from .prompts import PromptManager
            
            pm = PromptManager()
            
            # Add count to context
            context['count'] = count
            
            # Try to render as template first
            try:
                prompt = pm.render_template(template, context)
            except (KeyError, FileNotFoundError):
                # If template not found, use as raw prompt with context substitution
                prompt = template.format(**context)
            
            # Generate response
            response = self.generate(prompt, **kwargs)
            
            # Parse commands from response
            commands = self.parse_commands_from_response(response)
            
            return commands[:count]  # Return requested number
            
        except Exception as e:
            print(f"Error generating commands: {e}")
            return []


# Convenience function
def create_litellm_client(model: Optional[str] = None, **kwargs) -> LiteLLMProvider:
    """
    Create a LiteLLM client.
    
    Args:
        model: Optional model override
        **kwargs: Additional initialization parameters
        
    Returns:
        Configured LiteLLMProvider instance
    """
    return LiteLLMProvider(model=model, **kwargs)


# For testing
if __name__ == '__main__':
    try:
        provider = LiteLLMProvider()
        print("LiteLLM provider initialized successfully!")
        print(f"Model: {provider.model}")
        print(f"Temperature: {provider.temperature}")
        print(f"Max Tokens: {provider.max_tokens}")
        
        # Test generation
        test_prompt = "Generate 3 voice commands for Alexa to control smart home devices."
        print(f"\nTest prompt: {test_prompt}")
        
        response = provider.generate(test_prompt)
        print(f"\nResponse:\n{response}")
        
        commands = provider.parse_commands_from_response(response)
        print(f"\nParsed commands:")
        for i, cmd in enumerate(commands, 1):
            print(f"{i}. {cmd}")
            
    except Exception as e:
        print(f"Error: {e}")
