# LipFuzzer 2.0
Modern linguistic-model-guided fuzzing tool for Voice Assistant security testing.

## Overview

LipFuzzer is a research tool designed to systematically discover speech misinterpretations (LAPSUS) in Voice Assistant applications. It uses linguistic models to generate mutations that can cause semantic inconsistency in voice command interpretation.

**Key Features:**
- 🎯 Linguistic-model-guided fuzzing
- 🗣️ Modern Deepgram TTS integration
- 🔒 Secure configuration management
- 📊 8 mutation modules (phoneme, word, grammar levels)
- 🧪 Automated verification pipeline

## Prerequisites

- Python 3.6 or higher
- Deepgram API key ([Get one here](https://console.deepgram.com/))

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

### 3. Configure Deepgram API Key

Choose **one** of the following methods (checked in order of priority):

#### Option A: Environment Variable (Recommended for CI/CD)
```bash
export DEEPGRAM_API_KEY="your_api_key_here"
```

#### Option B: .env File (Recommended for Development)
```bash
cp .env.example .env
# Edit .env and add your API key
```

#### Option C: .secrets File
```bash
# Create .secrets file with:
DEEPGRAM_API_KEY=your_api_key_here
```

Or use JSON format:
```json
{
  "DEEPGRAM_API_KEY": "your_api_key_here"
}
```

### 4. Run LipFuzzer

```bash
python3 first.py
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEEPGRAM_API_KEY` | Deepgram API key (required) | - |
| `DEEPGRAM_MODEL` | TTS voice model | `aura-asteria-en` |
| `DEEPGRAM_ENCODING` | Audio encoding format | `mp3` |
| `DEEPGRAM_SAMPLE_RATE` | Sample rate in Hz | `24000` |

### Available Voice Models

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

## Usage Examples

### Basic Fuzzing
```python
from LipEngine import lipEngine

l = lipEngine()
l.loadRule("testRule.txt")
l.loadData("testInput.txt")
l.fuzz(OUTPUTSTEP=True)
```

### With Speech Synthesis
```python
from LipEngine import lipEngine

l = lipEngine()
l.loadRule("testRule.txt")
l.loadData("testInput.txt")

# Synthesize a verification audio
l.synthesize_speech(
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
├── LipEngine.py          # Main fuzzing engine
├── NLPEngine.py          # NLP preprocessing
├── tts/                  # TTS module
│   ├── base.py          # TTS interface
│   └── deepgram_tts.py  # Deepgram implementation
├── modules/             # Mutation modules
│   ├── module_zero.py   # Word swapping
│   ├── module_one.py    # Word addition
│   └── ...
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

## Troubleshooting

### "DEEPGRAM_API_KEY not found"
Make sure you've set your API key via environment variable, .env file, or .secrets file.

### "deepgram-sdk not installed"
Run: `pip3 install deepgram-sdk`

### Stanford CoreNLP errors
Ensure the CoreNLP path in `NLPEngine.py` matches your downloaded version.

### Import errors
Make sure all dependencies are installed: `pip3 install -r requirements.txt`

## Support

For issues and questions:
- Open an issue on GitHub
- Check the research paper for methodology details
- Review test files for usage examples

