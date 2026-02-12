"""
Base LLM provider interface for future extensibility.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text from a single prompt.
        
        Args:
            prompt: The prompt text to send to the LLM
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated text string
        """
        pass
    
    @abstractmethod
    def generate_batch(self, prompts: List[str], **kwargs) -> List[str]:
        """
        Generate text from multiple prompts efficiently.
        
        Args:
            prompts: List of prompt texts
            **kwargs: Additional provider-specific parameters
            
        Returns:
            List of generated text strings
        """
        pass
    
    @abstractmethod
    def generate_commands(self, context: Dict[str, Any], template: str, count: int = 10, **kwargs) -> List[str]:
        """
        Generate voice commands using a template and context.
        
        Args:
            context: Dictionary containing template variables
            template: Template name or prompt string
            count: Number of commands to generate
            **kwargs: Additional provider-specific parameters
            
        Returns:
            List of generated voice command strings
        """
        pass
    
    def parse_commands_from_response(self, response: str) -> List[str]:
        """
        Parse individual commands from LLM response.
        
        Many LLMs return numbered lists or multiple lines.
        This helper extracts individual commands.
        
        Args:
            response: Raw LLM response text
            
        Returns:
            List of parsed command strings
        """
        commands = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Remove common numbering patterns
            # e.g., "1. ", "1) ", "- ", "* "
            import re
            cleaned = re.sub(r'^[\d]+[\.\)]\s*', '', line)
            cleaned = re.sub(r'^[-\*•]\s*', '', cleaned)
            cleaned = cleaned.strip('"\'')
            
            if cleaned:
                commands.append(cleaned)
        
        return commands
