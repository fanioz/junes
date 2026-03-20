<div align="center">

# junes

**A command-line interface for the Jules REST API.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

</div>

## Installation

| Use Case | Recommended Method |
|----------|-------------------|
| **End Users** | [Quick Install (One-Liner)](#quick-install-one-liner) ⭐ |
| **Contributors** | [Manual Clone with uv](#manual-clone-with-uv-recommended-for-development) |
| **Without uv** | [Manual Clone with pip](#manual-clone-with-pip-traditional) |

### Quick Install (One-Liner) ⭐

```bash
curl -sSL https://raw.githubusercontent.com/fanioz/junes/main/install.sh | bash
```

This will:
- Install [uv](https://github.com/astral-sh/uv) if not present
- Clone the repository to `~/.junes/junes`
- Set up a virtual environment
- Install the package
- Create the `junes` command in `~/.local/bin`

> **Note:** Make sure `~/.local/bin` is in your PATH.

---

## Alternative Installation Methods

### Manual Clone with uv (Recommended for Development)

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/fanioz/junes.git
cd junes

# Install in development mode
uv pip install -e .

# Or install with development dependencies
uv pip install -e ".[dev]"

# Create symlink to use globally
ln -sf "$(pwd)/junes-uv" ~/.local/bin/junes
```

### Manual Clone with pip (Traditional)

```bash
# Clone the repository
git clone https://github.com/fanioz/junes.git
cd junes

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### From PyPI

```bash
# Using uv
uv pip install junes

# Using pip
pip install junes
```

**Note:** The PyPI package is named `junes`, but the CLI command is `junes`. This naming avoids conflicts with existing PyPI packages.

## Configuration

### Initialize configuration

```bash
junes config init
```

This will create a configuration file at `~/.junes/config.toml` and prompt for your API key.

### API Key

The API key can be provided in three ways (in order of priority):

1. **CLI option**: `junes --api-key YOUR_KEY sources list`
2. **Environment variable**: Export `JULES_API_KEY=YOUR_KEY`
3. **Config file**: Set via `junes config init`

## Usage

### List sources

```bash
junes sources list
junes sources list --format json
junes sources list --format table
```

### Get source details

```bash
junes sources get <source-id>
```

### Create a session

```bash
junes sessions create <source-id>
junes sessions create <source-id> --format json
```

### List sessions

```bash
junes sessions list
junes sessions list --status active
junes sessions list --source sources/github/org/repo
```

### Get session details

```bash
junes sessions get <session-id>
```

### Approve a plan

```bash
junes sessions approve <session-id>
```

### List activities

```bash
junes activities list <session-id>
```

### Send a message to the agent

```bash
junes agent send <session-id> "Your message here"
echo "Your message" | junes agent send <session-id>
```

## Output Formats

All commands support three output formats:

- `plain` (default): Human-readable text output
- `table`: Tabular output using ASCII tables
- `json`: Machine-readable JSON output

## Verbose Mode

Enable verbose logging to see HTTP request details:

```bash
junes --verbose sources list
```

## Development

### Run tests

**Using uv (recommended):**
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=junes --cov-report=html

# Run specific test file
uv run pytest tests/test_client.py
```

**Using pytest directly:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=junes --cov-report=html

# Run specific test file
pytest tests/test_client.py
```

### Property-based testing

Property tests use Hypothesis and run with minimum 100 iterations by default.

## Requirements

- Python 3.8 or higher

## License

MIT
