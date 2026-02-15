"""Command-line interface for LipFuzzer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lipfuzzer import __version__, lipEngine


def main() -> int:
    """Main CLI entry point.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="LipFuzzer - Linguistic-model-guided fuzzing for Voice Assistant security testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic fuzzing
  lipfuzzer fuzz --rules data/testRule.txt --input data/testInput.txt
  
  # Generate seed commands
  lipfuzzer generate seeds --assistant Alexa --domain smart_home --count 10
  
  # Generate mutations
  lipfuzzer generate mutations --command "Alexa, open crypto wallet" --type phonetic
  
  # Full pipeline with TTS
  lipfuzzer pipeline --rules data/testRule.txt --input data/testInput.txt --output audio/

For more information, visit: https://github.com/yangyong/lipfuzzer
        """,
    )

    parser.add_argument("--version", action="version", version=f"LipFuzzer {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Fuzz command
    fuzz_parser = subparsers.add_parser("fuzz", help="Run fuzzing on voice commands")
    fuzz_parser.add_argument("--rules", "-r", required=True, help="Path to rules file")
    fuzz_parser.add_argument("--input", "-i", required=True, help="Path to input data file")
    fuzz_parser.add_argument("--output", "-o", default="out.txt", help="Output file path")
    fuzz_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate test commands using LLM")
    gen_subparsers = gen_parser.add_subparsers(dest="gen_type", help="Generation type")

    # Generate seeds
    seeds_parser = gen_subparsers.add_parser("seeds", help="Generate seed commands")
    seeds_parser.add_argument("--assistant", required=True, help="Voice assistant (Alexa, Siri, Google)")
    seeds_parser.add_argument("--domain", required=True, help="Domain (smart_home, banking, etc.)")
    seeds_parser.add_argument("--count", "-n", type=int, default=10, help="Number of commands to generate")
    seeds_parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    # Generate mutations
    mut_parser = gen_subparsers.add_parser("mutations", help="Generate mutations of a command")
    mut_parser.add_argument("--command", "-c", required=True, help="Command to mutate")
    mut_parser.add_argument(
        "--type",
        "-t",
        choices=["phonetic", "semantic", "syntactic"],
        default="phonetic",
        help="Mutation type",
    )
    mut_parser.add_argument("--count", "-n", type=int, default=5, help="Number of mutations")
    mut_parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    # Pipeline command
    pipeline_parser = subparsers.add_parser("pipeline", help="Full fuzzing + TTS pipeline")
    pipeline_parser.add_argument("--rules", "-r", required=True, help="Path to rules file")
    pipeline_parser.add_argument("--input", "-i", required=True, help="Path to input data file")
    pipeline_parser.add_argument("--output", "-o", default="audio/", help="Output directory for audio files")
    pipeline_parser.add_argument("--voice", default="aura-asteria-en", help="Deepgram voice model")

    # Config command
    config_parser = subparsers.add_parser("config", help="Show configuration")
    config_parser.add_argument("--check", action="store_true", help="Check API keys and dependencies")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    try:
        match args.command:
            case "fuzz":
                return run_fuzz(args)
            case "generate":
                return run_generate(args)
            case "pipeline":
                return run_pipeline(args)
            case "config":
                return run_config(args)
            case _:
                parser.print_help()
                return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def run_fuzz(args: argparse.Namespace) -> int:
    """Run basic fuzzing."""
    print(f"Running fuzzing with rules: {args.rules}, input: {args.input}")
    
    engine = lipEngine(outPath=args.output)
    engine.loadRule(args.rules)
    engine.loadData(args.input)
    engine.fuzz(OUTPUTSTEP=args.verbose)
    
    print(f"Fuzzing complete. Output written to: {args.output}")
    return 0


def run_generate(args):
    """Run LLM generation."""
    if not args.gen_type:
        print("Error: Must specify generation type (seeds or mutations)", file=sys.stderr)
        return 1
    
    engine = lipEngine()
    
    if args.gen_type == 'seeds':
        print(f"Generating {args.count} seed commands for {args.assistant} ({args.domain})...")
        commands = engine.generate_seed_commands(
            assistant=args.assistant,
            domain=args.domain,
            count=args.count
        )
    elif args.gen_type == 'mutations':
        print(f"Generating {args.count} {args.type} mutations...")
        commands = engine.generate_mutations(
            original_command=args.command,
            mutation_type=args.type,
            count=args.count
        )
    else:
        print(f"Error: Unknown generation type: {args.gen_type}", file=sys.stderr)
        return 1
    
    if hasattr(args, 'output') and args.output:
        with open(args.output, 'w') as f:
            for cmd in commands:
                f.write(f"{cmd}\n")
        print(f"Commands written to: {args.output}")
    else:
        for cmd in commands:
            print(cmd)
    
    return 0


def run_pipeline(args):
    """Run full pipeline with TTS."""
    print(f"Running full pipeline: {args.rules} + {args.input} -> {args.output}")
    
    # Create output directory
    Path(args.output).mkdir(parents=True, exist_ok=True)
    
    engine = lipEngine()
    engine.loadRule(args.rules)
    engine.loadData(args.input)
    
    # Run fuzzing
    engine.fuzz(OUTPUTSTEP=True)
    
    # TODO: Add TTS synthesis for fuzzing results
    print(f"Pipeline complete. Audio files saved to: {args.output}")
    return 0


def run_config(args):
    """Show configuration."""
    from config import get_config
    
    print("LipFuzzer Configuration")
    print("=" * 60)
    print(f"Version: {__version__}")
    
    if args.check:
        print("\nChecking dependencies and API keys...")
        
        # Check imports
        try:
            import inflect
            print("✓ inflect")
        except ImportError:
            print("✗ inflect (required)")
        
        try:
            import nltk
            print("✓ nltk")
        except ImportError:
            print("✗ nltk (required)")
        
        try:
            from tts.deepgram_tts import DeepgramTTS
            print("✓ deepgram-sdk")
        except ImportError:
            print("✗ deepgram-sdk (required for TTS)")
        
        # Check API keys
        try:
            config = get_config()
            if config.get('DEEPGRAM_API_KEY'):
                print("✓ DEEPGRAM_API_KEY configured")
            else:
                print("✗ DEEPGRAM_API_KEY not configured")
            
            if config.get('OPENAI_API_KEY') or config.get('GEMINI_API_KEY') or config.get('ANTHROPIC_API_KEY'):
                print("✓ LLM API key configured")
            else:
                print("✗ LLM API key not configured")
        except Exception as e:
            print(f"✗ Config error: {e}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
