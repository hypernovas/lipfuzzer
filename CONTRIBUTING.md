# Contributing to LipFuzzer

Thank you for your interest in contributing to LipFuzzer! This document provides guidelines and instructions for contributing to this research project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Research Contributions](#research-contributions)

## Code of Conduct

This project is a research tool focused on improving voice assistant security. We expect all contributors to:

- Use the tool responsibly and ethically
- Follow responsible disclosure practices
- Respect privacy and security considerations
- Collaborate professionally and respectfully

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/lipfuzzer.git
   cd lipfuzzer
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original/lipfuzzer.git
   ```

## Development Setup

1. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Download Stanford CoreNLP** (see README.md for instructions)

3. **Configure API keys** (see README.md):
   - Copy `.env.example` to `.env`
   - Add your API keys

4. **Run tests** to verify setup:
   ```bash
   python3 tests/test_setup.py
   ```

## How to Contribute

### Reporting Issues

Before creating an issue:
- Check if the issue already exists
- Collect relevant information (OS, Python version, error messages)
- Provide a minimal reproducible example

When creating an issue, include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages/logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
- Use issue templates if available
- Clearly describe the enhancement
- Explain the use case and benefits
- Consider backward compatibility

### Code Contributions

Areas where contributions are particularly welcome:
- **New mutation modules** (see `modules/` directory)
- **LLM provider integrations** (see `llm/` directory)
- **TTS provider integrations** (see `tts/` directory)
- **Prompt templates** (see `llm/templates/` directory)
- **Documentation improvements**
- **Test coverage**
- **Bug fixes**

## Coding Standards

### Python Style Guide

We follow **Google Python Style Guide** and **PEP 8**:

- **Module names**: lowercase_with_underscores (e.g., `lip_engine.py`)
- **Class names**: PascalCase or camelCase (e.g., `lipEngine`, `NLPEngine`)
- **Function names**: camelCase or lowercase_with_underscores
- **Constants**: UPPER_CASE_WITH_UNDERSCORES
- **Indentation**: Tabs (as per existing codebase)
- **Line length**: 120 characters maximum

### Documentation

- Add docstrings to all public classes and methods
- Include type hints where appropriate
- Update README.md for user-facing changes
- Document new modules in relevant documentation

### Example Module Structure

```python
"""
Module description here.
"""

class ExampleClass(object):
	"""Class description."""
	
	def __init__(self):
		"""Initialize the class."""
		pass
	
	def example_method(self, param):
		"""
		Method description.
		
		Args:
			param: Description of parameter
			
		Returns:
			Description of return value
		"""
		pass
```

## Testing

### Running Tests

```bash
# Run basic setup test
python3 tests/test_setup.py

# Run basic fuzzing test
python3 first.py

# Run LLM demo
python3 examples/llm_generation_demo.py
```

### Adding Tests

- Add test files to `tests/` directory
- Name test files `test_*.py`
- Include both positive and negative test cases
- Test edge cases and error handling

## Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow coding standards
   - Add tests if applicable
   - Update documentation

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```
   
   Commit message format:
   - Use present tense ("Add feature" not "Added feature")
   - First line: brief summary (50 chars max)
   - Blank line, then detailed description if needed

4. **Sync with upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**:
   - Provide clear title and description
   - Reference related issues (e.g., "Fixes #123")
   - Include testing details
   - Add screenshots/examples if applicable

### PR Review Process

- Maintainers will review your PR
- Address feedback and make requested changes
- Once approved, your PR will be merged
- Your contribution will be acknowledged

## Research Contributions

### Publishing Research Using LipFuzzer

If you use LipFuzzer in your research:

1. **Cite the original paper**:
   ```bibtex
   @inproceedings{zhang2019lipfuzzer,
     title={Life after Speech Recognition: Fuzzing Semantic Misinterpretation for Voice Assistant Applications},
     author={Zhang, Yangyong and Xu, Lei and Mendoza, Abner and Yang, Guangliang and Chinprutthiwong, Phakpoom and Gu, Guofei},
     booktitle={NDSS},
     year={2019}
   }
   ```

2. **Consider contributing back**:
   - Share new mutation strategies
   - Contribute domain-specific prompt templates
   - Share findings (following responsible disclosure)

### Responsible Disclosure

If you discover security vulnerabilities:

1. **Do NOT** create public issues
2. Email maintainers directly with details
3. Allow reasonable time for response/fix
4. Follow coordinated disclosure practices

## Project Structure

```
lipfuzzer/
├── src/                   # Source code
│   ├── lip_engine.py      # Main fuzzing engine
│   ├── nlp_engine.py      # NLP preprocessing
│   └── io/                # I/O modules
│       ├── rule_io.py     # Rule file I/O
│       ├── utterance_io.py  # Utterance data I/O
│       └── table_io.py    # Table data I/O
├── config.py              # Configuration management
├── first.py               # Basic usage example
├── modules/               # Mutation modules
├── llm/                   # LLM integration
├── tts/                   # TTS integration
├── examples/              # Usage examples
├── tests/                 # Test files
├── test/                  # Legacy test utilities
├── input_generation/      # Input generators
├── rule_generation/       # Rule generators
├── data/                  # Test data files
├── docs/                  # Additional documentation
└── scripts/               # Utility scripts
```

## Getting Help

- **Documentation**: Check README.md and docs/
- **Issues**: Search existing issues on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Research Paper**: Read the original NDSS paper

## Recognition

Contributors will be:
- Listed in project contributors
- Acknowledged in relevant documentation
- Credited in academic contexts when appropriate

Thank you for contributing to LipFuzzer! Your contributions help advance voice assistant security research.
