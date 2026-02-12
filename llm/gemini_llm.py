"""
Google Gemini provider implementation.

Integration with Google's Gemini AI models.
"""

from typing import List, Dict, Optional, Any
from .base import LLMProvider

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Run: pip install google-generativeai")


class GeminiProvider(LLMProvider):
    """Google Gemini provider."""
    
    def __init__(self,
                 api_key: Optional[str] = None,
                 model: Optional[str] = None,
                 temperature: Optional[float] = None,
                 max_tokens: Optional[int] = None):
        """
        Initialize Gemini provider.
        
        Args:
            api_key: Google API key (if None, loads from config)
            model: Model name (e.g., 'gemini-pro', 'gemini-pro-vision')
            temperature: Generation temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
        """
        if not GEMINI_AVAILABLE:
            raise ImportError(
                "google-generativeai is required. Install with: pip install google-generativeai"
            )
        
        from config import get_config
        config = get_config()
        
        self.api_key = api_key or config.gemini_api_key
        self.model_name = model or config.llm_model
        self.temperature = temperature if temperature is not None else config.llm_temperature
        self.max_tokens = max_tokens or config.llm_max_tokens
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize model with generation config
        self.generation_config = {
            'temperature': self.temperature,
            'max_output_tokens': self.max_tokens,
        }
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config
        )
    
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
            # Override generation config if kwargs provided
            if 'temperature' in kwargs or 'max_tokens' in kwargs:
                temp_config = self.generation_config.copy()
                if 'temperature' in kwargs:
                    temp_config['temperature'] = kwargs['temperature']
                if 'max_tokens' in kwargs:
                    temp_config['max_output_tokens'] = kwargs['max_tokens']
                
                temp_model = genai.GenerativeModel(
                    model_name=self.model_name,
                    generation_config=temp_config
                )
                response = temp_model.generate_content(prompt)
            else:
                response = self.model.generate_content(prompt)
            
            return response.text
            
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
    
    def generate_stream(self, prompt: str, **kwargs):
        """
        Generate text with streaming.
        
        Args:
            prompt: The prompt text
            **kwargs: Override temperature, max_tokens, etc.
            
        Yields:
            Text chunks as they're generated
        """
        try:
            response = self.model.generate_content(prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            print(f"Error streaming text: {e}")


# Convenience function
def create_gemini_client(api_key: Optional[str] = None, **kwargs) -> GeminiProvider:
    """
    Create a Gemini client.
    
    Args:
        api_key: Optional API key (uses config if not provided)
        **kwargs: Additional initialization parameters
        
    Returns:
        Configured GeminiProvider instance
    """
    return GeminiProvider(api_key=api_key, **kwargs)


# For testing
if __name__ == '__main__':
    try:
        provider = GeminiProvider()
        print("Gemini provider initialized successfully!")
        print(f"Model: {provider.model_name}")
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
