#!/usr/bin/env python3
"""
Test script to verify LipFuzzer setup and Deepgram TTS integration.

Usage:
    python3 test_setup.py
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("=" * 60)
    print("Testing imports...")
    print("=" * 60)
    
    tests = {
        'inflect': False,
        'enchant': False,
        'nltk': False,
        'config': False,
        'tts.deepgram_tts': False,
        'lip_engine': False,
        'nlp_engine': False
    }
    
    for module in tests.keys():
        try:
            if module == 'enchant':
                import enchant
            elif module == 'inflect':
                import inflect
            elif module == 'nltk':
                import nltk
            elif module == 'config':
                from config import get_config
            elif module == 'tts.deepgram_tts':
                from tts.deepgram_tts import DeepgramTTS
            elif module == 'lip_engine':
                from lip_engine import lipEngine
            elif module == 'nlp_engine':
                from nlp_engine import NLPEngine
            tests[module] = True
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module} - {e}")
    
    return all(tests.values())

def test_config():
    """Test configuration loading."""
    print("\n" + "=" * 60)
    print("Testing configuration...")
    print("=" * 60)
    
    try:
        from config import get_config
        config = get_config()
        
        print(f"✓ Configuration loaded successfully")
        print(f"  Model: {config.deepgram_model}")
        print(f"  Encoding: {config.deepgram_encoding}")
        print(f"  Sample Rate: {config.deepgram_sample_rate}")
        print(f"  API Key: {'*' * 10}{config.deepgram_api_key[-4:]}")
        return True
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print("\nPlease set your Deepgram API key using one of these methods:")
        print("  1. export DEEPGRAM_API_KEY='your_key'")
        print("  2. Create .env file with: DEEPGRAM_API_KEY=your_key")
        print("  3. Create .secrets file with: DEEPGRAM_API_KEY=your_key")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_tts():
    """Test TTS client initialization."""
    print("\n" + "=" * 60)
    print("Testing TTS client...")
    print("=" * 60)
    
    try:
        from tts.deepgram_tts import DeepgramTTS
        
        tts = DeepgramTTS()
        print(f"✓ Deepgram TTS client initialized")
        print(f"  Using model: {tts.model}")
        
        # Optional: Test actual synthesis if user wants
        print("\nTo test actual speech synthesis, run:")
        print("  python3 -c \"from tts.deepgram_tts import DeepgramTTS; tts = DeepgramTTS(); tts.synthesize('Hello world', 'test.mp3')\"")
        
        return True
    except Exception as e:
        print(f"✗ TTS initialization failed: {e}")
        return False

def test_stanford_corenlp():
    """Test Stanford CoreNLP availability."""
    print("\n" + "=" * 60)
    print("Testing Stanford CoreNLP...")
    print("=" * 60)
    
    try:
        from nlp_engine import NLPEngine
        nlp = NLPEngine()
        
        # Check if JAR files exist
        if os.path.exists(nlp.path_to_jar):
            print(f"✓ Stanford CoreNLP JAR found: {nlp.path_to_jar}")
        else:
            print(f"✗ Stanford CoreNLP JAR not found: {nlp.path_to_jar}")
            print("\nPlease download Stanford CoreNLP from:")
            print("  https://stanfordnlp.github.io/CoreNLP/")
            return False
        
        if os.path.exists(nlp.path_to_models_jar):
            print(f"✓ Stanford CoreNLP models found: {nlp.path_to_models_jar}")
        else:
            print(f"✗ Stanford CoreNLP models not found: {nlp.path_to_models_jar}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error checking Stanford CoreNLP: {e}")
        return False

def test_lipengine():
    """Test LipEngine initialization."""
    print("\n" + "=" * 60)
    print("Testing LipEngine...")
    print("=" * 60)
    
    try:
        from lip_engine import lipEngine
        
        engine = lipEngine()
        print(f"✓ LipEngine initialized")
        print(f"  Supported modules: {engine.supportedModule}")
        
        if engine.tts_client:
            print(f"✓ TTS client integrated")
        else:
            print(f"⚠ TTS client not available (install deepgram-sdk)")
        
        return True
    except Exception as e:
        print(f"✗ LipEngine initialization failed: {e}")
        return False

def main():
    """Run all tests."""
    print("\n🔍 LipFuzzer Setup Verification")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("TTS Client", test_tts()))
    results.append(("Stanford CoreNLP", test_stanford_corenlp()))
    results.append(("LipEngine", test_lipengine()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed! LipFuzzer is ready to use.")
        print("\nRun the fuzzer with: python3 first.py")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        print("\nFor help, see README.md or check the error messages above.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
