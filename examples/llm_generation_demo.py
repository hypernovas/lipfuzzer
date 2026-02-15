"""
LLM Voice Command Generation Demo

This script demonstrates how to use LipFuzzer's LLM integration to:
1. Generate seed voice commands
2. Create mutations of existing commands
3. Generate adversarial commands for security testing
4. Synthesize commands to audio files
"""

import sys
import os

# Add parent directory to path to import lip_engine
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lipfuzzer import lipEngine


def demo_seed_generation(engine):
    """Demonstrate seed command generation."""
    print("\n" + "="*70)
    print("DEMO 1: Seed Command Generation")
    print("="*70)
    print("\nGenerating voice commands for smart home domain...")
    
    commands = engine.generate_seed_commands(
        assistant="Alexa",
        domain="smart_home",
        count=5
    )
    
    if commands:
        print("\nGenerated Commands:")
        for i, cmd in enumerate(commands, 1):
            print(f"  {i}. {cmd}")
    else:
        print("Failed to generate commands. Check your LLM configuration.")
    
    return commands


def demo_mutation_generation(engine):
    """Demonstrate command mutation generation."""
    print("\n" + "="*70)
    print("DEMO 2: Mutation Generation")
    print("="*70)
    
    original_command = "Alexa, open crypto wallet"
    print(f"\nOriginal command: {original_command}")
    print("\nGenerating phonetic mutations...")
    
    mutations = engine.generate_mutations(
        original_command=original_command,
        mutation_type="phonetic",
        count=3
    )
    
    if mutations:
        print("\nGenerated Mutations:")
        for i, cmd in enumerate(mutations, 1):
            print(f"  {i}. {cmd}")
    else:
        print("Failed to generate mutations.")
    
    return mutations


def demo_adversarial_generation(engine):
    """Demonstrate adversarial command generation."""
    print("\n" + "="*70)
    print("DEMO 3: Adversarial Command Generation")
    print("="*70)
    print("\nGenerating adversarial commands for banking domain...")
    
    commands = engine.generate_adversarial_commands(
        assistant="Alexa",
        target_domain="banking",
        count=3
    )
    
    if commands:
        print("\nGenerated Adversarial Commands:")
        for i, cmd in enumerate(commands, 1):
            print(f"  {i}. {cmd}")
    else:
        print("Failed to generate adversarial commands.")
    
    return commands


def demo_custom_prompt(engine):
    """Demonstrate custom prompt generation."""
    print("\n" + "="*70)
    print("DEMO 4: Custom Prompt Generation")
    print("="*70)
    
    custom_prompt = """Generate voice commands for a smart home assistant that could 
be misinterpreted due to similar-sounding words. Focus on commands involving:
- Security systems (locks, cameras)
- Financial transactions
- Privacy settings

Generate {count} commands."""
    
    print(f"\nCustom prompt: {custom_prompt[:100]}...")
    
    commands = engine.generate_with_custom_prompt(
        prompt=custom_prompt,
        count=3
    )
    
    if commands:
        print("\nGenerated Commands:")
        for i, cmd in enumerate(commands, 1):
            print(f"  {i}. {cmd}")
    else:
        print("Failed to generate commands.")
    
    return commands


def demo_generate_and_synthesize(engine):
    """Demonstrate end-to-end generation and synthesis."""
    print("\n" + "="*70)
    print("DEMO 5: Generate and Synthesize to Audio")
    print("="*70)
    print("\nGenerating commands and synthesizing to audio files...")
    
    context = {
        'assistant': 'Alexa',
        'domain': 'smart_home',
        'count': 3
    }
    
    results = engine.generate_and_synthesize(
        prompt_template='smart_home_commands',
        context=context,
        output_dir='demo_audio',
        prefix='smart_home'
    )
    
    if results:
        print(f"\nSuccessfully generated {len(results)} audio files:")
        for command, audio_path in results:
            print(f"  - {command}")
            print(f"    Audio: {audio_path}")
    else:
        print("Failed to generate and synthesize.")
    
    return results


def demo_domain_specific(engine):
    """Demonstrate domain-specific generation."""
    print("\n" + "="*70)
    print("DEMO 6: Domain-Specific Generation")
    print("="*70)
    
    # Banking domain
    print("\nGenerating banking commands...")
    banking_context = {
        'assistant': 'Alexa',
        'count': 3
    }
    
    banking_commands = engine.llm_client.generate_commands(
        banking_context,
        'banking_commands',
        3
    )
    
    if banking_commands:
        print("\nBanking Commands:")
        for i, cmd in enumerate(banking_commands, 1):
            print(f"  {i}. {cmd}")
    
    return banking_commands


def main():
    """Run all demos."""
    print("\n" + "="*70)
    print("LipFuzzer LLM Integration Demo")
    print("="*70)
    print("\nThis demo showcases LLM-powered voice command generation.")
    print("Make sure you have configured your LLM API keys in .env file.")
    
    # Initialize engine
    print("\nInitializing LipFuzzer engine...")
    try:
        engine = lipEngine()
    except Exception as e:
        print(f"\nError: Failed to initialize LipEngine: {e}")
        print("\nMake sure you have:")
        print("  1. Set DEEPGRAM_API_KEY in your .env file")
        print("  2. Set at least one LLM API key (OPENAI_API_KEY, GEMINI_API_KEY, etc.)")
        print("  3. Installed all dependencies: pip install -r requirements.txt")
        return
    
    if not engine.llm_client:
        print("\nWarning: LLM client not available.")
        print("Please install LLM dependencies and configure API keys.")
        print("\nInstall dependencies:")
        print("  pip install litellm openai google-generativeai pyyaml")
        print("\nConfigure API keys in .env file:")
        print("  OPENAI_API_KEY=your_key_here")
        return
    
    # Run all demos
    try:
        # Demo 1: Seed generation
        demo_seed_generation(engine)
        
        # Demo 2: Mutations
        demo_mutation_generation(engine)
        
        # Demo 3: Adversarial generation
        demo_adversarial_generation(engine)
        
        # Demo 4: Custom prompts
        demo_custom_prompt(engine)
        
        # Demo 5: Generate and synthesize (only if TTS is available)
        if engine.tts_client:
            demo_generate_and_synthesize(engine)
        else:
            print("\n" + "="*70)
            print("DEMO 5: Skipped (TTS client not available)")
            print("="*70)
        
        # Demo 6: Domain-specific
        demo_domain_specific(engine)
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("\n" + "="*70)
    print("Demo Complete!")
    print("="*70)
    print("\nKey Features Demonstrated:")
    print("  1. Seed command generation for different domains")
    print("  2. Intelligent mutations of existing commands")
    print("  3. Adversarial command generation for security testing")
    print("  4. Custom prompt-based generation")
    print("  5. End-to-end generation and synthesis to audio")
    print("  6. Domain-specific templates (banking, smart home, etc.)")
    print("\nFor more information, see README.md")
    print("="*70)


if __name__ == '__main__':
    main()
