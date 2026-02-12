"""
Deepgram TTS provider implementation.
"""

import os
from typing import Optional
from pathlib import Path

try:
    from deepgram import DeepgramClient, SpeakOptions
    DEEPGRAM_AVAILABLE = True
except ImportError:
    DEEPGRAM_AVAILABLE = False
    print("Warning: deepgram-sdk not installed. Run: pip install deepgram-sdk")

from .base import TTSProvider
from config import get_config


class DeepgramTTS(TTSProvider):
    """Deepgram Text-to-Speech provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Deepgram TTS client.
        
        Args:
            api_key: Deepgram API key (if None, loads from config)
            model: TTS model to use (if None, uses config default)
        """
        if not DEEPGRAM_AVAILABLE:
            raise ImportError(
                "deepgram-sdk is required. Install with: pip install deepgram-sdk"
            )
        
        # Load configuration
        config = get_config()
        
        self.api_key = api_key or config.deepgram_api_key
        self.model = model or config.deepgram_model
        self.encoding = config.deepgram_encoding
        self.sample_rate = config.deepgram_sample_rate
        
        # Initialize Deepgram client
        self.client = DeepgramClient(self.api_key)
    
    def synthesize(self, text: str, output_path: str, voice: Optional[str] = None) -> bool:
        """
        Synthesize speech from text and save to file.
        
        Args:
            text: The text to synthesize
            output_path: Path to save the audio file
            voice: Optional voice/model override (e.g., 'aura-luna-en')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure output directory exists
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Prepare options
            model = voice or self.model
            options = SpeakOptions(
                model=model,
                encoding=self.encoding,
                sample_rate=self.sample_rate
            )
            
            # Synthesize speech
            response = self.client.speak.v("1").save(
                output_path,
                {"text": text},
                options
            )
            
            return True
            
        except Exception as e:
            print(f"Error synthesizing speech: {e}")
            return False
    
    def synthesize_to_bytes(self, text: str, voice: Optional[str] = None) -> bytes:
        """
        Synthesize speech from text and return audio bytes.
        
        Args:
            text: The text to synthesize
            voice: Optional voice/model override
            
        Returns:
            Audio data as bytes
        """
        try:
            # Prepare options
            model = voice or self.model
            options = SpeakOptions(
                model=model,
                encoding=self.encoding,
                sample_rate=self.sample_rate
            )
            
            # Synthesize speech
            response = self.client.speak.v("1").stream(
                {"text": text},
                options
            )
            
            # Collect audio data
            audio_data = b''
            for chunk in response:
                audio_data += chunk
            
            return audio_data
            
        except Exception as e:
            print(f"Error synthesizing speech: {e}")
            return b''
    
    def synthesize_batch(self, texts: list, output_dir: str, prefix: str = "audio", 
                        voice: Optional[str] = None) -> list:
        """
        Synthesize multiple texts to audio files.
        
        Args:
            texts: List of texts to synthesize
            output_dir: Directory to save audio files
            prefix: Prefix for output filenames
            voice: Optional voice/model override
            
        Returns:
            List of output file paths
        """
        output_files = []
        
        for idx, text in enumerate(texts):
            output_path = os.path.join(output_dir, f"{prefix}_{idx}.mp3")
            if self.synthesize(text, output_path, voice):
                output_files.append(output_path)
            else:
                output_files.append(None)
        
        return output_files


# Convenience function for backward compatibility
def create_tts_client(api_key: Optional[str] = None) -> DeepgramTTS:
    """
    Create a Deepgram TTS client.
    
    Args:
        api_key: Optional API key (uses config if not provided)
        
    Returns:
        Configured DeepgramTTS instance
    """
    return DeepgramTTS(api_key=api_key)


# For testing
if __name__ == '__main__':
    try:
        tts = DeepgramTTS()
        print("Deepgram TTS client initialized successfully!")
        print(f"Model: {tts.model}")
        print(f"Encoding: {tts.encoding}")
        print(f"Sample Rate: {tts.sample_rate}")
        
        # Test synthesis
        test_text = "Hello, this is a test of Deepgram text to speech."
        test_output = "test_output.mp3"
        
        print(f"\nSynthesizing: '{test_text}'")
        success = tts.synthesize(test_text, test_output)
        
        if success:
            print(f"Success! Audio saved to {test_output}")
        else:
            print("Synthesis failed.")
            
    except Exception as e:
        print(f"Error: {e}")
