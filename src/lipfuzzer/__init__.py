"""
LipFuzzer - Linguistic-model-guided fuzzing for Voice Assistant security testing.
"""

from .lip_engine import lipEngine
from .nlp_engine import NLPEngine

__all__ = ['lipEngine', 'NLPEngine']
__version__ = '2.0.0'
__author__ = 'Yangyong Zhang'
__license__ = 'MIT'
