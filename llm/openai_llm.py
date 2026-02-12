"""
OpenAI provider implementation.

Direct integration with OpenAI's API for GPT models.
"""

from typing import List, Dict, Optional, Any
from .base import LLMProvider

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: openai not installed. Run: pip install openai")


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""
    
    def __init__(self,
                 api_key: Optional[str] = None,
                 model: Optional[str] = None,
                 temperature: Optional[float] = None,
                 max_tokens: Optional[int] = None):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key (if None, loads from config)
            model: Model name (e.g., 'gpt-4', 'gpt-3.5-turbo')
            temperature: Generation temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "openai is required. Install with: pip install openai"
            )
        
        from config import get_config
        config = get_config()
        
        self.api_key = api_key or config.openai_api_key
        self.model = model or config.llm_model
        self.temperature = temperature if temperature is not None else config.llm_temperature
        self.max_tokens = max_tokens or config.llm_max_tokens
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)
    
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
            response = self.client.chat.completions.create(
                model=kwargs.get('model', self.model),
                messages=[
                    {"role": "user", "content": prompt}
                ],
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
        
        # OpenAI doesn't have native batch API for chat completions
        # Process sequentially
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
    
    def generate_stream(self, prompt: str, **kwargs):
        """
        Generate text with streaming (useful for long responses).
        
        Args:
            prompt: The prompt text
            **kwargs: Override temperature, max_tokens, etc.
            
        Yields:
            Text chunks as they're generated
        """
        try:
            stream = self.client.chat.completions.create(
                model=kwargs.get('model', self.model),
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get('temperature', self.temperature),
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            print(f"Error streaming text: {e}")


# Convenience function
def create_openai_client(api_key: Optional[str] = None, **kwargs) -> OpenAIProvider:
    """
    Create an OpenAI client.
    
    Args:
        api_key: Optional API key (uses config if not provided)
        **kwargs: Additional initialization parameters
        
    Returns:
        Configured OpenAIProvider instance
    """
    return OpenAIProvider(api_key=api_key, **kwargs)


# For testing
if __name__ == '__main__':
    try:
        provider = OpenAIProvider()
        print("OpenAI provider initialized successfully!")
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
