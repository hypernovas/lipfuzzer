# Publishing to PyPI

This guide explains how to build and publish LipFuzzer to PyPI.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) installed
- PyPI account and API token
- Permissions to publish to PyPI

## Local Development

### Install in Development Mode

```bash
# Clone the repository
git clone https://github.com/yangyong/lipfuzzer.git
cd lipfuzzer

# Sync dependencies with uv
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# The package is installed in editable mode automatically
```

### Run Tests

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# Run linting
uv run ruff check src/
uv run black --check src/
uv run mypy src/
```

### Using the CLI

```bash
# Run lipfuzzer CLI
uv run lipfuzzer --help

# Or after activating venv
lipfuzzer --help
```

## Building for Distribution

### Build the Package

```bash
# Build wheel and source distribution
uv build

# This creates:
# - dist/lipfuzzer-2.0.0-py3-none-any.whl
# - dist/lipfuzzer-2.0.0.tar.gz
```

### Test the Built Package

```bash
# Install from wheel in a fresh environment
uv pip install dist/lipfuzzer-2.0.0-py3-none-any.whl

# Or install from source distribution
uv pip install dist/lipfuzzer-2.0.0.tar.gz

# Test the installation
python -c "import lipfuzzer; print(lipfuzzer.__version__)"
lipfuzzer --version
```

## Publishing to PyPI

### Test on TestPyPI First

```bash
# Upload to TestPyPI
uv publish --index-url https://test.pypi.org/legacy/ --token <your-test-pypi-token>

# Or use twine
pip install twine
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
uv pip install --index-url https://test.pypi.org/simple/ lipfuzzer
```

### Publish to Production PyPI

```bash
# Upload to PyPI
uv publish --token <your-pypi-token>

# Or use twine
twine upload dist/*
```

### Using PyPI API Tokens

Create a `.pypirc` file in your home directory:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-<your-pypi-token>

[testpypi]
username = __token__
password = pypi-<your-testpypi-token>
```

Then publish with:

```bash
twine upload --repository pypi dist/*
```

## CI/CD with GitHub Actions

### Automated Publishing

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
      
      - name: Set up Python
        run: uv python install 3.12
      
      - name: Build package
        run: uv build
      
      - name: Publish to PyPI
        run: uv publish
        env:
          UV_PUBLISH_TOKEN: ${{ secrets.PYPI_TOKEN }}
```

Add your PyPI token to GitHub Secrets as `PYPI_TOKEN`.

## Version Management

### Updating Version

Update version in `pyproject.toml`:

```toml
[project]
version = "2.1.0"
```

Also update in `src/lipfuzzer/__init__.py`:

```python
__version__ = '2.1.0'
```

### Creating a Release

```bash
# Tag the release
git tag -a v2.1.0 -m "Release version 2.1.0"
git push origin v2.1.0

# Build and publish
uv build
uv publish --token <your-token>
```

## Package Verification

After publishing, verify the package:

```bash
# Install from PyPI
pip install lipfuzzer

# Test import
python -c "import lipfuzzer; print(lipfuzzer.__version__)"

# Test CLI
lipfuzzer --version
lipfuzzer --help

# Test basic functionality
lipfuzzer config --check
```

## Checklist Before Publishing

- [ ] All tests pass (`uv run pytest`)
- [ ] Linting passes (`uv run ruff check`)
- [ ] Type checking passes (`uv run mypy`)
- [ ] Version updated in `pyproject.toml` and `__init__.py`
- [ ] CHANGELOG.md updated
- [ ] README.md is up to date
- [ ] Build succeeds (`uv build`)
- [ ] Package installs locally (`uv pip install dist/*.whl`)
- [ ] CLI works (`lipfuzzer --version`)
- [ ] Tested on TestPyPI first
- [ ] Git tag created
- [ ] Release notes written

## Troubleshooting

### Build Errors

```bash
# Clean build artifacts
rm -rf dist/ build/ *.egg-info
uv clean

# Rebuild
uv build
```

### Import Errors

Ensure package structure is correct:
```
src/
└── lipfuzzer/
    ├── __init__.py
    ├── lip_engine.py
    ├── nlp_engine.py
    ├── cli.py
    └── io/
        ├── __init__.py
        ├── rule_io.py
        ├── utterance_io.py
        └── table_io.py
```

### Publishing Errors

- Check token permissions
- Verify package name is available on PyPI
- Ensure version number hasn't been used before
- Check network connectivity

## Resources

- [uv documentation](https://docs.astral.sh/uv/)
- [PyPI packaging guide](https://packaging.python.org/)
- [Python packaging tutorial](https://packaging.python.org/tutorials/packaging-projects/)
- [twine documentation](https://twine.readthedocs.io/)

## Support

For issues or questions:
- Open an issue on GitHub
- Check the documentation
- Review existing issues and discussions
