# Installing LipFuzzer with uv

This guide covers installing and using LipFuzzer with [uv](https://github.com/astral-sh/uv), a fast Python package installer and resolver.

## Why uv?

- **Fast**: 10-100x faster than pip
- **Reliable**: True dependency resolution with universal lockfiles
- **Compatible**: Drop-in replacement for pip, pip-tools, and virtualenv
- **Modern**: Built in Rust for performance

## Installation

### 1. Install uv

#### macOS and Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Using pip

```bash
pip install uv
```

### 2. Install LipFuzzer

#### From PyPI (when published)

```bash
uv pip install lipfuzzer
```

#### From Source

```bash
# Clone the repository
git clone https://github.com/yangyong/lipfuzzer.git
cd lipfuzzer

# Sync dependencies (creates .venv automatically)
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

## Using LipFuzzer with uv

### Running Commands

```bash
# Run lipfuzzer CLI directly with uv
uv run lipfuzzer --help

# Run Python scripts
uv run python first.py

# Run examples
uv run python examples/llm_generation_demo.py

# Run tests
uv run pytest
```

### Development Workflow

```bash
# Sync dependencies
uv sync

# Add a new dependency
uv add requests

# Add a development dependency
uv add --dev pytest-asyncio

# Update dependencies
uv lock --upgrade

# Show installed packages
uv pip list

# Run linting
uv run ruff check src/
uv run black src/
uv run mypy src/
```

## Virtual Environment Management

### Create and Activate

```bash
# uv sync creates .venv automatically
uv sync

# Activate manually if needed
source .venv/bin/activate  # Unix/macOS
.venv\Scripts\activate     # Windows

# Or run commands without activating
uv run lipfuzzer --help
```

### Python Version Management

```bash
# Install specific Python version
uv python install 3.11

# Use specific Python version
uv python pin 3.11

# List available Python versions
uv python list
```

## Configuration

### Environment Variables

Create `.env` file:

```bash
DEEPGRAM_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
LLM_PROVIDER=litellm
LLM_MODEL=gpt-3.5-turbo
```

uv will automatically use these when running commands.

### pyproject.toml

Dependencies are managed in `pyproject.toml`:

```toml
[project]
dependencies = [
    "deepgram-sdk>=3.0.0",
    "python-dotenv>=1.0.0",
    # ... other dependencies
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]
```

## Common Tasks

### Installing Optional Dependencies

```bash
# Install with dev dependencies
uv sync --extra dev

# Install with docs dependencies
uv sync --extra docs

# Install with async dependencies
uv sync --extra async

# Install all optional dependencies
uv sync --all-extras
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_setup.py
```

### Code Quality

```bash
# Format code
uv run black src/

# Check formatting
uv run black --check src/

# Lint code
uv run ruff check src/

# Type checking
uv run mypy src/
```

### Building and Publishing

```bash
# Build package
uv build

# Publish to PyPI (requires token)
uv publish --token <your-token>

# Publish to TestPyPI
uv publish --index-url https://test.pypi.org/legacy/ --token <your-token>
```

## Troubleshooting

### Resolver Issues

If you encounter dependency conflicts:

```bash
# Update the lockfile
uv lock --upgrade

# Reinstall from scratch
rm -rf .venv uv.lock
uv sync
```

### Package Not Found

```bash
# Clear cache
uv cache clean

# Reinstall
uv sync --reinstall
```

### Import Errors

Make sure to activate the virtual environment or use `uv run`:

```bash
# Option 1: Activate venv
source .venv/bin/activate
python -c "import lipfuzzer"

# Option 2: Use uv run
uv run python -c "import lipfuzzer"
```

## Migration from pip

### From requirements.txt

If you have an existing `requirements.txt`:

```bash
# uv can use requirements.txt directly
uv pip install -r requirements.txt

# Or convert to pyproject.toml (recommended)
# Dependencies are already in pyproject.toml
uv sync
```

### From pip to uv

```bash
# Instead of: pip install package
uv pip install package

# Instead of: pip install -r requirements.txt
uv pip install -r requirements.txt

# Instead of: pip install -e .
uv pip install -e .

# Or better: use uv sync for project dependencies
uv sync
```

## Best Practices

### 1. Use uv.lock for Reproducible Builds

The `uv.lock` file ensures everyone gets the same versions:

```bash
# Generate/update lockfile
uv lock

# Install from lockfile
uv sync
```

### 2. Separate Development Dependencies

Use optional dependencies in `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = ["pytest", "black", "ruff"]
```

Install with:
```bash
uv sync --extra dev
```

### 3. Pin Python Version

In `pyproject.toml`:

```toml
[project]
requires-python = ">=3.9"
```

### 4. Use uv run for Scripts

Avoid manual venv activation:

```bash
# Instead of:
source .venv/bin/activate
python script.py

# Use:
uv run python script.py
```

## Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [uv GitHub Repository](https://github.com/astral-sh/uv)
- [Python Packaging Guide](https://packaging.python.org/)

## Support

For issues:
- LipFuzzer: Open issue on GitHub
- uv: Check [uv documentation](https://docs.astral.sh/uv/) or GitHub issues
