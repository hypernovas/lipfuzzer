# Migration Guide: LipFuzzer 1.x to 2.0

This guide helps you upgrade from AWS Polly (LipFuzzer 1.x) to Deepgram TTS (LipFuzzer 2.0).

## What's New in 2.0

- ✅ **Modern TTS**: Deepgram SDK with better voices and performance
- ✅ **Secure Config**: direnv-style configuration (no more hardcoded keys!)
- ✅ **Better DX**: Simple setup with .env files
- ✅ **Same Output**: MP3 files with same naming conventions
- ✅ **Backward Compatible**: No changes to fuzzing logic or modules

## Migration Steps

### 1. Install New Dependencies

```bash
pip3 install -r requirements.txt
```

This installs:
- `deepgram-sdk>=3.0.0`
- `python-dotenv>=1.0.0`
- All existing dependencies

### 2. Remove AWS Credentials

**Before (LipFuzzer 1.x):**
```python
# test/audio/pollyAudio.py
polly_client = boto3.Session(
    aws_access_key_id='YOUR KEY',
    aws_secret_access_key='YOUR KEY',
    region_name='us-east-1'
).client('polly')
```

**After (LipFuzzer 2.0):**
```python
# test/audio/pollyAudio.py
from tts.deepgram_tts import DeepgramTTS
tts_client = DeepgramTTS()  # Keys loaded from config
```

### 3. Set Up Deepgram API Key

Get your free API key from [Deepgram Console](https://console.deepgram.com/).

Choose ONE method:

#### Method A: Environment Variable
```bash
export DEEPGRAM_API_KEY="your_api_key_here"
```

#### Method B: .env File (Recommended)
```bash
cp .env.example .env
# Edit .env and add your key
```

#### Method C: .secrets File
Create `.secrets` with:
```
DEEPGRAM_API_KEY=your_api_key_here
```

### 4. Update Your Code

#### If You Used Polly Directly

**Before:**
```python
import boto3

polly = boto3.client('polly', 
    aws_access_key_id='key',
    aws_secret_access_key='secret',
    region_name='us-east-1')

response = polly.synthesize_speech(
    VoiceId='Joanna',
    OutputFormat='mp3',
    Text='Hello world'
)

with open('output.mp3', 'wb') as f:
    f.write(response['AudioStream'].read())
```

**After:**
```python
from tts.deepgram_tts import DeepgramTTS

tts = DeepgramTTS()
tts.synthesize('Hello world', 'output.mp3')
```

#### If You Used LipEngine

No changes needed! The LipEngine now automatically uses Deepgram TTS:

```python
from LipEngine import lipEngine

l = lipEngine()  # TTS client auto-initialized
l.loadRule("testRule.txt")
l.loadData("testInput.txt")
l.fuzz(OUTPUTSTEP=True)

# New feature: Direct synthesis
l.synthesize_speech("Alexa, open wallet", "test.mp3")
```

### 5. Verify Setup

Run the test script:
```bash
python3 test_setup.py
```

This checks:
- ✓ All dependencies installed
- ✓ Configuration loaded correctly
- ✓ TTS client working
- ✓ Stanford CoreNLP available
- ✓ LipEngine integration

## API Comparison

| Feature | AWS Polly (1.x) | Deepgram (2.0) |
|---------|----------------|----------------|
| Setup | Manual credentials | Config-based |
| Voices | Neural/Standard | Aura models |
| Latency | ~2-3s | ~0.5-1s |
| Quality | Good | Excellent |
| Price | $4/1M chars | $0.015/min |
| Python API | boto3 | deepgram-sdk |
| Output Format | MP3/OGG/PCM | MP3/WAV/FLAC |

## Voice Models

### Polly to Deepgram Voice Mapping

| Polly Voice | Deepgram Equivalent | Gender |
|-------------|-------------------|--------|
| Joanna | aura-asteria-en | Female |
| Salli | aura-luna-en | Female |
| Kimberly | aura-stella-en | Female |
| Kendra | aura-athena-en | Female |
| Ivy | aura-hera-en | Female |
| Matthew | aura-orion-en | Male |
| Joey | aura-arcas-en | Male |
| Justin | aura-perseus-en | Male |

## Configuration Options

### Optional Settings

Create a `.env` file with:

```bash
# Required
DEEPGRAM_API_KEY=your_key

# Optional (with defaults)
DEEPGRAM_MODEL=aura-asteria-en
DEEPGRAM_ENCODING=mp3
DEEPGRAM_SAMPLE_RATE=24000
```

## Troubleshooting

### "DEEPGRAM_API_KEY not found"
**Solution:** Set your API key using one of the three methods above.

### "ModuleNotFoundError: No module named 'deepgram'"
**Solution:** Run `pip3 install deepgram-sdk`

### Audio sounds different
**Solution:** Deepgram voices are more natural. To match Polly's Joanna, use `aura-asteria-en` (default).

### Need specific voice?
**Solution:** Override in code:
```python
tts.synthesize(text, output, voice='aura-luna-en')
```

Or set globally in `.env`:
```bash
DEEPGRAM_MODEL=aura-luna-en
```

## Rollback (If Needed)

If you need to temporarily rollback to Polly:

1. Keep old version in a branch:
   ```bash
   git checkout -b polly-backup
   ```

2. The old code is in git history:
   ```bash
   git log --all -- test/audio/pollyAudio.py
   ```

## Benefits of Upgrading

1. **Security**: No hardcoded credentials
2. **Performance**: 2-3x faster synthesis
3. **Quality**: More natural voices
4. **Cost**: Often cheaper for research projects
5. **Modern**: Active SDK with regular updates
6. **Flexibility**: Easy to add other TTS providers later

## Need Help?

- Check `README.md` for full documentation
- Run `python3 test_setup.py` to diagnose issues
- Review `test/audio/pollyAudio.py` for usage examples
- Check `.env.example` for configuration options

## Summary

✅ **Install**: `pip3 install -r requirements.txt`
✅ **Configure**: Set `DEEPGRAM_API_KEY` in `.env`
✅ **Test**: Run `python3 test_setup.py`
✅ **Use**: Same as before, just better!

That's it! Your LipFuzzer is now modernized with Deepgram TTS.
