# LLM Integration - Implementation Summary

## Overview

LipFuzzer now includes comprehensive LLM integration for intelligent voice command generation. This enables researchers to use large language models (OpenAI GPT, Google Gemini, Claude, local models) to generate realistic, mutated, and adversarial voice commands for security testing.

## What Was Implemented

### 1. LLM Module Structure (`llm/`)

**Created Files:**
- `llm/base.py` - Abstract base class for LLM providers
- `llm/litellm_provider.py` - LiteLLM unified interface (100+ models)
- `llm/openai_llm.py` - Direct OpenAI integration
- `llm/gemini_llm.py` - Google Gemini integration
- `llm/prompts.py` - Flexible prompt template system
- `llm/__init__.py` - Module exports and factory function

**Architecture:**
```
LLMProvider (Abstract Base)
    ├── LiteLLMProvider (100+ models)
    ├── OpenAIProvider (GPT-3.5, GPT-4)
    └── GeminiProvider (Gemini Pro)
```

### 2. Prompt Template System

**Features:**
- YAML-based templates with variable substitution
- Pre-built templates for common use cases
- Support for custom templates
- Template categories: seed generation, mutations, adversarial, domain-specific

**Default Templates:**
- `seed_generation.yaml` - Generate initial commands
- `mutation_generation.yaml` - Create variations
- `adversarial_generation.yaml` - Security testing commands
- `smart_home_commands.yaml` - Smart home domain
- `banking_commands.yaml` - Banking/finance domain

### 3. LipEngine Integration

**New Methods:**
```python
# Generate seed commands
generate_seed_commands(assistant, domain, count, template)

# Generate mutations
generate_mutations(original_command, mutation_type, count, template)

# Generate adversarial commands
generate_adversarial_commands(assistant, target_domain, count, template)

# Generate and synthesize to audio
generate_and_synthesize(prompt_template, context, output_dir, voice, prefix)

# Custom prompt generation
generate_with_custom_prompt(prompt, count)
```

### 4. Configuration System

**Extended `config.py`:**
- `llm_provider` - Provider selection (litellm, openai, gemini)
- `llm_model` - Model name
- `llm_temperature` - Generation temperature (0.0-1.0)
- `llm_max_tokens` - Maximum tokens to generate
- `openai_api_key` - OpenAI API key
- `gemini_api_key` - Google Gemini API key
- `anthropic_api_key` - Anthropic API key

**Configuration Precedence:**
1. Environment variables (highest priority)
2. `.env` file
3. `.secrets` file (lowest priority)

### 5. Dependencies

**Added to `requirements.txt`:**
- `litellm>=1.0.0` - Unified LLM interface
- `openai>=1.0.0` - OpenAI SDK
- `google-generativeai>=0.3.0` - Gemini SDK
- `pyyaml>=6.0` - YAML parsing
- `jinja2>=3.1.0` - Template rendering

### 6. Documentation & Examples

**Updated `README.md`:**
- LLM configuration instructions
- Usage examples for all features
- Available models and providers
- Troubleshooting section

**Created `examples/llm_generation_demo.py`:**
- Comprehensive demo of all LLM features
- 6 different usage scenarios
- Error handling examples
- Integration with TTS

## Installation

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Configure API Keys

Create `.env` file:
```bash
# TTS (existing)
DEEPGRAM_API_KEY=your_deepgram_key

# LLM (new - at least one required)
OPENAI_API_KEY=your_openai_key
# OR
GEMINI_API_KEY=your_gemini_key

# LLM Configuration
LLM_PROVIDER=litellm
LLM_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000
```

## Usage Examples

### Basic Command Generation

```python
from lip_engine import lipEngine

engine = lipEngine()

# Generate smart home commands
commands = engine.generate_seed_commands(
    assistant="Alexa",
    domain="smart_home",
    count=10
)

for cmd in commands:
    print(cmd)
```

### Generate Mutations

```python
# Create phonetic variations
mutations = engine.generate_mutations(
    original_command="Alexa, open crypto wallet",
    mutation_type="phonetic",
    count=5
)
```

### Generate and Synthesize

```python
# Generate commands and create audio files
results = engine.generate_and_synthesize(
    prompt_template='adversarial_generation',
    context={
        'assistant': 'Alexa',
        'domain': 'banking',
        'count': 5
    },
    output_dir='adversarial_audio/'
)

for command, audio_path in results:
    print(f"{command} -> {audio_path}")
```

### Custom Prompts

```python
commands = engine.generate_with_custom_prompt(
    prompt="""Generate voice commands that exploit homophones 
    in banking applications. Focus on commands that sound like 
    legitimate operations but could be misinterpreted.""",
    count=5
)
```

## Running the Demo

```bash
python3 examples/llm_generation_demo.py
```

This demonstrates:
1. Seed command generation
2. Mutation generation
3. Adversarial command creation
4. Custom prompt usage
5. End-to-end generation + synthesis
6. Domain-specific templates

## Key Features

### Multi-Provider Support

Switch between providers easily:

```bash
# OpenAI
LLM_PROVIDER=openai
LLM_MODEL=gpt-4

# Google Gemini
LLM_PROVIDER=gemini
LLM_MODEL=gemini-pro

# Anthropic Claude via LiteLLM
LLM_PROVIDER=litellm
LLM_MODEL=claude-3-sonnet

# Local Ollama models
LLM_PROVIDER=litellm
LLM_MODEL=ollama/llama2
```

### Flexible Prompting

- Pre-built templates for common scenarios
- YAML-based templates for easy customization
- Support for custom inline prompts
- Variable substitution with context dictionaries
- Template categories by use case

### Seamless TTS Integration

- Generate commands with LLM
- Automatically synthesize to audio with Deepgram TTS
- Batch processing support
- Configurable voice models

### Cost Optimization

- Use cheaper models (gpt-3.5-turbo) for simple tasks
- Use powerful models (gpt-4) for complex adversarial generation
- Support for free local models via Ollama

## Architecture Benefits

1. **Modular Design** - Clean separation of concerns
2. **Provider Agnostic** - Easy to add new LLM providers
3. **Template-Based** - Customize prompts without code changes
4. **Non-Breaking** - Existing workflows continue to work
5. **Extensible** - Simple to add new features
6. **Well-Documented** - Comprehensive docs and examples

## Future Enhancements

Potential areas for extension:
- Async/batch API calls for better performance
- Few-shot learning with example commands
- Fine-tuning support for domain-specific models
- Integration with existing fuzzing rules
- Auto-generation of mutation rules from LLM analysis
- Multi-turn conversations for iterative refinement

## Testing

The implementation includes:
- Graceful fallbacks when dependencies unavailable
- Clear error messages with installation instructions
- Demo script for validation
- Example prompts and templates
- Comprehensive documentation

## Files Created

```
llm/
├── __init__.py (90 lines)
├── base.py (80 lines)
├── litellm_provider.py (180 lines)
├── openai_llm.py (200 lines)
├── gemini_llm.py (180 lines)
└── prompts.py (350 lines)

examples/
└── llm_generation_demo.py (300 lines)

Modified:
├── config.py (+150 lines)
├── lip_engine.py (+150 lines)
├── requirements.txt (+6 dependencies)
├── .env.example (+20 lines)
└── README.md (+200 lines)
```

Total: ~1,900 lines of new code + documentation

## Getting Started

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Configure API keys:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the demo:**
   ```bash
   python3 examples/llm_generation_demo.py
   ```

4. **Read the documentation:**
   - See README.md for detailed usage
   - Check examples/ for code samples
   - Review llm/templates/ for prompt examples

## Support

For issues or questions:
- Check README.md troubleshooting section
- Review llm_generation_demo.py for working examples
- Consult provider documentation (OpenAI, Gemini, LiteLLM)

---

**Implementation Status:** ✅ Complete

All planned features have been implemented and documented. The system is ready for use with proper API key configuration and dependency installation.
