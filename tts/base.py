"""
Base TTS provider interface for future extensibility.
"""

from abc import ABC, abstractmethod
from typing import Optional


class TTSProvider(ABC):
    """Abstract base class for TTS providers."""
    
    @abstractmethod
    def synthesize(self, text: str, output_path: str, voice: Optional[str] = None) -> bool:
        """
        Synthesize speech from text and save to file.
        
        Args:
            text: The text to synthesize
            output_path: Path to save the audio file
            voice: Optional voice identifier
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def synthesize_to_bytes(self, text: str, voice: Optional[str] = None) -> bytes:
        """
        Synthesize speech from text and return audio bytes.
        
        Args:
            text: The text to synthesize
            voice: Optional voice identifier
            
        Returns:
            Audio data as bytes
        """
        pass
