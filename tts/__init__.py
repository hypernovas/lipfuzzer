"""
Text-to-Speech module for LipFuzzer.

Provides abstraction for different TTS providers.
"""

from .base import TTSProvider
from .deepgram_tts import DeepgramTTS

__all__ = ['TTSProvider', 'DeepgramTTS']
