# Aigerim Apai 👋

An intelligent text and audio processing assistant that helps you improve your writing and transcribe audio content. Aigerim Apai combines advanced language processing with audio transcription capabilities to provide a comprehensive text enhancement solution.

## 🚀 Features

- **Grammar Correction**: Automatically identifies and corrects grammar mistakes in text
- **Audio Transcription**: Converts audio files to text with high accuracy
- **OpenAI Integration**: Leverages OpenAI's powerful language models
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
- UV package installer for dependency management
- Just command runner for task automation
