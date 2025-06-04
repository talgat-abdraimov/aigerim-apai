# Aigerim Apai 👋

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

</div>

> 🎯 Your AI-powered writing assistant and audio transcription tool

Aigerim Apai is an intelligent assistant that helps you perfect your writing and convert speech to text. It combines advanced AI capabilities to:

- ✍️ **Fix Grammar Mistakes**: Automatically detect and correct grammatical errors in your text
- 🎙️ **Transcribe Audio**: Convert spoken words into accurate written text
- 🤖 **AI-Powered**: Leverages OpenAI's advanced language models and LanguageTool for high accuracy
- 🚀 **Easy to Use**: Simple setup with both API and Docker deployment options

Perfect for:
- Any dumb people who can't write (like me)
- Anyone who doesn't want to pay for Grammarly or Telegram Premium
- Anyone who wants to improve their writing quality

## 🚀 Features

- **Grammar Correction**: Automatically identifies and corrects grammar mistakes in text
- **Audio Transcription**: Converts audio files to text with high accuracy
- **OpenAI Integration**: Leverages OpenAI's powerful language models
- **LanguageTool Integration**: Provides offline rule-based grammar correction
- **Docker Support**: Easy deployment with containerization
- **Comprehensive Testing**: Ensures reliability and accuracy
- **Developer-Friendly**: Complete development tools and linting setup

## 📋 Prerequisites

- Python 3.x
- Docker (optional, for containerized deployment)
- UV (Python package installer)
- Just command runner (for development tasks)

## 🛠️ Installation

### Local Development Setup

1. Create and activate a virtual environment:
   ```bash
   just venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   just dev-deps
   ```

3. Install production dependencies:
   ```bash
   just deps
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Docker Setup

1. Build the Docker image:
   ```bash
   just build
   ```

2. Start the server:
   ```bash
   just up
   ```

3. Stop the server:
   ```bash
   just stop
   ```

4. Stop and remove containers:
   ```bash
   just down
   ```

## ⚙️ Configuration

1. Configure your environment variables according to `config.py`
2. Adjust settings in `.ruff.toml` for linting preferences
3. Modify `pytest.ini` for test configurations

## 🧪 Testing

Run tests using the just command:
```bash
just test
```

## 🛠️ Development Commands

The project uses `just` as a command runner. Here are the available commands:

```bash
just venv          # Create virtual environment
just dev-deps      # Install development dependencies
just deps          # Install production dependencies
just build         # Build the server
just up [args]     # Start the server (optional arguments)
just stop          # Stop the server
just down          # Stop and remove the server
just logs [args]   # Show logs (optional arguments)
just lint          # Run ruff checks and formatting
just test          # Run tests
```

## 🐳 Docker

The project includes Docker support for containerized deployment:

- `Dockerfile`: Contains the build instructions
- `docker-compose.yml`: Defines the service configuration
- `.dockerignore`: Specifies files to exclude from the build

## 📁 Project Structure

```
├── src/
│   ├── bot.py           # Main bot implementation
│   ├── open_ai.py       # OpenAI integration
│   ├── utils.py         # Utility functions
│   ├── decorators.py    # Custom decorators
│   ├── constants.py     # Project constants
│   └── config.py        # Configuration management
├── tests/               # Test files
├── requirements.txt     # Production dependencies
├── dev-requirements.txt # Development dependencies
├── docker-compose.yml   # Docker compose configuration
└── Dockerfile          # Docker build instructions
```

## ✨ Acknowledgments

- OpenAI for their API and language models
- LanguageTool project for grammar corrections
- UV package installer for dependency management
- Just command runner for task automation
