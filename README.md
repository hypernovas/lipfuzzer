# LipFuzzer 2.0
Modern linguistic-model-guided fuzzing tool for Voice Assistant security testing.

## Overview

LipFuzzer is a research tool designed to systematically discover speech misinterpretations (LAPSUS) in Voice Assistant applications. It uses linguistic models to generate mutations that can cause semantic inconsistency in voice command interpretation.

**Key Features:**
- 🎯 Linguistic-model-guided fuzzing
- 🤖 LLM-powered command generation (OpenAI, Gemini, Claude, local models)
- 🗣️ Modern Deepgram TTS integration
- 🔒 Secure configuration management
- 📊 8 mutation modules (phoneme, word, grammar levels)
- 🧪 Automated verification pipeline
- 🎨 Flexible prompt templates for domain-specific testing

## Prerequisites

- Python 3.6 or higher
- Deepgram API key ([Get one here](https://console.deepgram.com/))
- LLM API key (at least one):
  - OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
  - Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
  - Anthropic API key ([Get one here](https://console.anthropic.com/))

## Quick Start

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Download Stanford CoreNLP

Download [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/) (English models) and extract to the **root folder**.

```bash
# Example for version 4.5.0
wget https://nlp.stanford.edu/software/stanford-corenlp-4.5.0.zip
unzip stanford-corenlp-4.5.0.zip
```

Update the path in `NLPEngine.py` if needed:
```python
self.path_to_jar = './stanford-corenlp-full-YYYY-MM-DD/stanford-corenlp-X.X.X.jar'
```

### 3. Configure API Keys

Choose **one** of the following methods (checked in order of priority):

#### Option A: Environment Variable (Recommended for CI/CD)
```bash
export DEEPGRAM_API_KEY="your_deepgram_key"
export OPENAI_API_KEY="your_openai_key"
# Or for Gemini:
export GEMINI_API_KEY="your_gemini_key"
```

#### Option B: .env File (Recommended for Development)
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Example `.env` file:
```bash
# TTS (required)
DEEPGRAM_API_KEY=your_deepgram_key

# LLM (at least one required)
OPENAI_API_KEY=your_openai_key
# OR
GEMINI_API_KEY=your_gemini_key
# OR
ANTHROPIC_API_KEY=your_anthropic_key

# LLM Configuration
LLM_PROVIDER=litellm
LLM_MODEL=gpt-3.5-turbo
```

#### Option C: .secrets File
```bash
# Create .secrets file with:
DEEPGRAM_API_KEY=your_deepgram_key
OPENAI_API_KEY=your_openai_key
```

Or use JSON format:
```json
{
  "DEEPGRAM_API_KEY": "your_deepgram_key",
  "OPENAI_API_KEY": "your_openai_key"
}
```

### 4. Run LipFuzzer

```bash
python3 first.py
```

## Configuration

### Environment Variables

#### TTS Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `DEEPGRAM_API_KEY` | Deepgram API key (required) | - |
| `DEEPGRAM_MODEL` | TTS voice model | `aura-asteria-en` |
| `DEEPGRAM_ENCODING` | Audio encoding format | `mp3` |
| `DEEPGRAM_SAMPLE_RATE` | Sample rate in Hz | `24000` |

#### LLM Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider (`litellm`, `openai`, `gemini`) | `litellm` |
| `LLM_MODEL` | Model name | `gpt-3.5-turbo` |
| `LLM_TEMPERATURE` | Generation temperature (0.0-1.0) | `0.7` |
| `LLM_MAX_TOKENS` | Maximum tokens to generate | `1000` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `GEMINI_API_KEY` | Google Gemini API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |

### Available Voice Models (Deepgram TTS)

- `aura-asteria-en` - Default female voice
- `aura-luna-en` - Warm female voice
- `aura-stella-en` - Energetic female voice
- `aura-athena-en` - Professional female voice
- `aura-hera-en` - Clear female voice
- `aura-orion-en` - Deep male voice
- `aura-arcas-en` - Confident male voice
- `aura-perseus-en` - Strong male voice
- `aura-angus-en` - Friendly male voice
- `aura-orpheus-en` - Smooth male voice
- `aura-helios-en` - Authoritative male voice
- `aura-zeus-en` - Commanding male voice

### Available LLM Models

**With LiteLLM (Unified Interface):**
- OpenAI: `gpt-4`, `gpt-3.5-turbo`, `gpt-4-turbo`
- Anthropic: `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`
- Google: `gemini-pro`, `gemini-1.5-pro`
- Local: `ollama/llama2`, `ollama/mistral`, `ollama/codellama`
- 100+ more models via LiteLLM

**Direct Providers:**
- OpenAI: `gpt-4`, `gpt-3.5-turbo`
- Gemini: `gemini-pro`, `gemini-pro-vision`

## Usage Examples

### Basic Fuzzing
```python
from lip_engine import lipEngine

l = lipEngine()
l.loadRule("testRule.txt")
l.loadData("testInput.txt")
l.fuzz(OUTPUTSTEP=True)
```

### LLM Command Generation

#### Generate Seed Commands
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

#### Generate Mutations
```python
# Create variations of existing commands
mutations = engine.generate_mutations(
    original_command="Alexa, open crypto wallet",
    mutation_type="phonetic",  # or "semantic", "syntactic"
    count=5
)

for mutation in mutations:
    print(mutation)
```

#### Generate Adversarial Commands
```python
# Generate security-focused test commands
adversarial = engine.generate_adversarial_commands(
    assistant="Alexa",
    target_domain="banking",
    count=10
)

for cmd in adversarial:
    print(cmd)
```

#### Custom Prompts
```python
# Use your own custom prompt
commands = engine.generate_with_custom_prompt(
    prompt="Generate voice commands that exploit homophones in banking apps",
    count=5
)
```

### LLM + TTS Integration

#### Generate and Synthesize to Audio
```python
# Generate commands with LLM and synthesize to audio files
results = engine.generate_and_synthesize(
    prompt_template='adversarial_generation',
    context={
        'assistant': 'Alexa',
        'domain': 'banking',
        'count': 5
    },
    output_dir='adversarial_audio/',
    voice='aura-orion-en'
)

# Results contain (command_text, audio_path) tuples
for command, audio_path in results:
    print(f"{command} -> {audio_path}")
```

### Traditional Speech Synthesis
```python
# Synthesize a single command
engine.synthesize_speech(
    "Alexa, open crypto wallet", 
    "output.mp3"
)
```

## Module System

LipFuzzer supports 8 mutation modules:

| Module | Type | Description |
|--------|------|-------------|
| 0 | Word | Word swapping/replacement |
| 1 | Word | Word addition based on dependency |
| 2 | Grammar | Word removal by Part-of-Speech |
| 3 | Grammar | Determiner addition |
| 4 | Phoneme | Phoneme mutation |
| 5 | Grammar | Prefix removal |
| 6 | Grammar | Lemmatization |
| 7 | Grammar | Prefix addition |

### Adding Custom Modules

1. Create `modules/module_<name>.py`
2. Add module ID to `LipEngine.py`:
   ```python
   self.supportedModule = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Add 8
   ```
3. Update `modules/__init__.py`:
   ```python
   __all__ = ["module_zero", ..., "module_eight"]
   ```

## Migration from AWS Polly

If you're upgrading from LipFuzzer 1.x with AWS Polly:

1. Remove AWS credentials from code
2. Install new dependencies: `pip3 install -r requirements.txt`
3. Configure Deepgram API key (see Configuration above)
4. Run as normal - audio output format remains the same (MP3)

## Project Structure

```
lipfuzzer/
├── config.py              # Configuration loader
├── lip_engine.py          # Main fuzzing engine
├── nlp_engine.py          # NLP preprocessing
├── llm/                  # LLM module (NEW)
│   ├── base.py          # LLM interface
│   ├── litellm_provider.py  # LiteLLM (unified)
│   ├── openai_llm.py    # OpenAI provider
│   ├── gemini_llm.py    # Gemini provider
│   ├── prompts.py       # Prompt management
│   └── templates/       # Prompt templates
│       ├── seed_generation.yaml
│       ├── mutation_generation.yaml
│       ├── adversarial_generation.yaml
│       ├── smart_home_commands.yaml
│       └── banking_commands.yaml
├── tts/                  # TTS module
│   ├── base.py          # TTS interface
│   └── deepgram_tts.py  # Deepgram implementation
├── modules/             # Mutation modules
│   ├── module_zero.py   # Word swapping
│   ├── module_one.py    # Word addition
│   └── ...
├── examples/            # Example scripts (NEW)
│   └── llm_generation_demo.py
├── test/                # Test utilities
│   └── audio/           # Audio generation
└── input_generation/    # Input generators

```

## Research Paper

This tool is based on the research paper:

**"LipFuzzer: Linguistic-Model-Guided Fuzzing for Voice Assistant Applications"**

Published in USENIX Security Symposium

[Read the paper](https://par.nsf.gov/servlets/purl/10104003)

## Citation

```bibtex
@inproceedings{zhang2019lipfuzzer,
  title={Life after Speech Recognition: Fuzzing Semantic Misinterpretation for Voice Assistant Applications},
  author={Zhang, Yangyong and Xu, Lei and Mendoza, Abner and Yang, Guangliang and Chinprutthiwong, Phakpoom and Gu, Guofei},
  booktitle={NDSS},
  year={2019}
}
```

## License

Research and educational use only. See LICENSE file for details.

## Advanced Usage

### Custom Prompt Templates

Create your own prompt templates in `llm/templates/`:

```yaml
name: custom_template
description: My custom prompt template
variables:
  - count
  - assistant
  - custom_param
template: |
  Generate {count} voice commands for {assistant} that {custom_param}.
  
  Return only the commands, one per line.
```

Use it in code:
```python
commands = engine.llm_client.generate_commands(
    context={
        'count': 5,
        'assistant': 'Alexa',
        'custom_param': 'test privacy features'
    },
    template='custom_template',
    count=5
)
```

### Switching LLM Providers

```bash
# Use OpenAI directly
LLM_PROVIDER=openai
LLM_MODEL=gpt-4

# Use Gemini
LLM_PROVIDER=gemini
LLM_MODEL=gemini-pro

# Use LiteLLM with Claude
LLM_PROVIDER=litellm
LLM_MODEL=claude-3-sonnet

# Use local Ollama model
LLM_PROVIDER=litellm
LLM_MODEL=ollama/llama2
```

### Running the Demo

```bash
python3 examples/llm_generation_demo.py
```

This demonstrates:
- Seed command generation
- Mutation generation
- Adversarial command creation
- Custom prompts
- End-to-end generation + synthesis
- Domain-specific templates

## Troubleshooting

### "DEEPGRAM_API_KEY not found"
Make sure you've set your API key via environment variable, .env file, or .secrets file.

### "LLM client not available"
Install LLM dependencies: `pip3 install litellm openai google-generativeai pyyaml`
Set at least one LLM API key in your .env file.

### "deepgram-sdk not installed"
Run: `pip3 install deepgram-sdk`

### Stanford CoreNLP errors
Ensure the CoreNLP path in `NLPEngine.py` matches your downloaded version.

### Import errors
Make sure all dependencies are installed: `pip3 install -r requirements.txt`

### LiteLLM model not found
Check available models at [LiteLLM docs](https://docs.litellm.ai/docs/providers)
Make sure you have the correct API key set for your chosen provider.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the research paper for methodology details
- Review test files for usage examples

