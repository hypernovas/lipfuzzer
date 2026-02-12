"""
Configuration loader with direnv-style precedence.

Priority order:
1. Environment variables
2. .env file
3. .secrets file

Usage:
    from config import get_config
    
    config = get_config()
    api_key = config.deepgram_api_key
"""

import os
import json
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class Config:
    """Configuration data structure for LipFuzzer."""
    deepgram_api_key: str
    deepgram_model: str = "aura-asteria-en"
    deepgram_encoding: str = "mp3"
    deepgram_sample_rate: int = 24000
    

class ConfigLoader:
    """Loads configuration with direnv-style precedence."""
    
    _instance: Optional['ConfigLoader'] = None
    _config: Optional[Config] = None
    
    def __new__(cls):
        """Singleton pattern to ensure config is loaded once."""
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the config loader."""
        if self._config is None:
            self._config = self._load_config()
    
    def _load_from_env(self) -> dict:
        """Load configuration from environment variables."""
        config = {}
        
        if 'DEEPGRAM_API_KEY' in os.environ:
            config['deepgram_api_key'] = os.environ['DEEPGRAM_API_KEY']
        
        if 'DEEPGRAM_MODEL' in os.environ:
            config['deepgram_model'] = os.environ['DEEPGRAM_MODEL']
        
        if 'DEEPGRAM_ENCODING' in os.environ:
            config['deepgram_encoding'] = os.environ['DEEPGRAM_ENCODING']
        
        if 'DEEPGRAM_SAMPLE_RATE' in os.environ:
            try:
                config['deepgram_sample_rate'] = int(os.environ['DEEPGRAM_SAMPLE_RATE'])
            except ValueError:
                pass
        
        return config
    
    def _load_from_dotenv(self) -> dict:
        """Load configuration from .env file."""
        config = {}
        env_path = Path('.env')
        
        if not env_path.exists():
            return config
        
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse key=value
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        
                        if key == 'DEEPGRAM_API_KEY':
                            config['deepgram_api_key'] = value
                        elif key == 'DEEPGRAM_MODEL':
                            config['deepgram_model'] = value
                        elif key == 'DEEPGRAM_ENCODING':
                            config['deepgram_encoding'] = value
                        elif key == 'DEEPGRAM_SAMPLE_RATE':
                            try:
                                config['deepgram_sample_rate'] = int(value)
                            except ValueError:
                                pass
        except Exception as e:
            print(f"Warning: Error reading .env file: {e}")
        
        return config
    
    def _load_from_secrets(self) -> dict:
        """Load configuration from .secrets file (supports JSON or key=value)."""
        config = {}
        secrets_path = Path('.secrets')
        
        if not secrets_path.exists():
            return config
        
        try:
            with open(secrets_path, 'r') as f:
                content = f.read().strip()
                
                # Try JSON format first
                if content.startswith('{'):
                    try:
                        data = json.loads(content)
                        if 'DEEPGRAM_API_KEY' in data:
                            config['deepgram_api_key'] = data['DEEPGRAM_API_KEY']
                        if 'DEEPGRAM_MODEL' in data:
                            config['deepgram_model'] = data['DEEPGRAM_MODEL']
                        if 'DEEPGRAM_ENCODING' in data:
                            config['deepgram_encoding'] = data['DEEPGRAM_ENCODING']
                        if 'DEEPGRAM_SAMPLE_RATE' in data:
                            config['deepgram_sample_rate'] = int(data['DEEPGRAM_SAMPLE_RATE'])
                        return config
                    except json.JSONDecodeError:
                        pass
                
                # Fall back to key=value format
                for line in content.split('\n'):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        
                        if key == 'DEEPGRAM_API_KEY':
                            config['deepgram_api_key'] = value
                        elif key == 'DEEPGRAM_MODEL':
                            config['deepgram_model'] = value
                        elif key == 'DEEPGRAM_ENCODING':
                            config['deepgram_encoding'] = value
                        elif key == 'DEEPGRAM_SAMPLE_RATE':
                            try:
                                config['deepgram_sample_rate'] = int(value)
                            except ValueError:
                                pass
        except Exception as e:
            print(f"Warning: Error reading .secrets file: {e}")
        
        return config
    
    def _load_config(self) -> Config:
        """Load configuration with precedence: env vars > .env > .secrets."""
        # Start with defaults
        config_data = {
            'deepgram_model': 'aura-asteria-en',
            'deepgram_encoding': 'mp3',
            'deepgram_sample_rate': 24000
        }
        
        # Load from .secrets (lowest priority)
        secrets_config = self._load_from_secrets()
        config_data.update(secrets_config)
        
        # Load from .env (medium priority)
        env_file_config = self._load_from_dotenv()
        config_data.update(env_file_config)
        
        # Load from environment variables (highest priority)
        env_config = self._load_from_env()
        config_data.update(env_config)
        
        # Validate required fields
        if 'deepgram_api_key' not in config_data:
            raise ValueError(
                "DEEPGRAM_API_KEY not found. Please set it via:\n"
                "  1. Environment variable: export DEEPGRAM_API_KEY=your_key\n"
                "  2. .env file: DEEPGRAM_API_KEY=your_key\n"
                "  3. .secrets file: DEEPGRAM_API_KEY=your_key"
            )
        
        return Config(**config_data)
    
    def get_config(self) -> Config:
        """Get the loaded configuration."""
        return self._config
    
    def reload(self) -> Config:
        """Force reload configuration (useful for testing)."""
        self._config = self._load_config()
        return self._config


# Convenience function for easy imports
def get_config() -> Config:
    """Get the application configuration."""
    loader = ConfigLoader()
    return loader.get_config()


# For testing/debugging
if __name__ == '__main__':
    try:
        config = get_config()
        print("Configuration loaded successfully!")
        print(f"Model: {config.deepgram_model}")
        print(f"Encoding: {config.deepgram_encoding}")
        print(f"Sample Rate: {config.deepgram_sample_rate}")
        print(f"API Key: {'*' * 10}{config.deepgram_api_key[-4:]}")
    except ValueError as e:
        print(f"Configuration Error: {e}")
