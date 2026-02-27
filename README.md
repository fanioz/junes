<div align="center">

# Jules CLI

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
curl -sSL https://raw.githubusercontent.com/yourusername/jules-cli/main/install.sh | bash
```

This will:
- Install [uv](https://github.com/astral-sh/uv) if not present
- Clone the repository to `~/.jules-cli/jules-cli`
- Set up a virtual environment
- Install the package
- Create the `jules` command in `~/.local/bin`

> **Note:** Make sure `~/.local/bin` is in your PATH.

---

## Alternative Installation Methods

### Manual Clone with uv (Recommended for Development)

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/yourusername/jules-cli.git
cd jules-cli

# Install in development mode
uv pip install -e .

# Or install with development dependencies
uv pip install -e ".[dev]"

# Create symlink to use globally
ln -sf "$(pwd)/jules-uv" ~/.local/bin/jules
```

### Manual Clone with pip (Traditional)

```bash
# Clone the repository
git clone https://github.com/yourusername/jules-cli.git
cd jules-cli

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### From PyPI (When Published)

```bash
# Using uv
uv pip install jules-cli

# Using pip
pip install jules-cli
```

## Configuration

### Initialize configuration

```bash
jules config init
```

This will create a configuration file at `~/.jules-cli/config.toml` and prompt for your API key.

### API Key

The API key can be provided in three ways (in order of priority):

1. **CLI option**: `jules --api-key YOUR_KEY sources list`
2. **Environment variable**: Export `JULES_API_KEY=YOUR_KEY`
3. **Config file**: Set via `jules config init`

## Usage

### List sources

```bash
jules sources list
jules sources list --format json
jules sources list --format table
```

### Create a session

```bash
jules sessions create <source-id>
jules sessions create <source-id> --format json
```

### List sessions

```bash
jules sessions list
jules sessions list --status active
```

### Get session details

```bash
jules sessions get <session-id>
```

### Approve a plan

```bash
jules sessions approve <session-id>
```

### List activities

```bash
jules activities list <session-id>
```

### Send a message to the agent

```bash
jules agent send <session-id> "Your message here"
echo "Your message" | jules agent send <session-id>
```

## Output Formats

All commands support three output formats:

- `plain` (default): Human-readable text output
- `table`: Tabular output using ASCII tables
- `json`: Machine-readable JSON output

## Verbose Mode

Enable verbose logging to see HTTP request details:

```bash
jules --verbose sources list
```

## Development

### Run tests

**Using uv (recommended):**
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=jules_cli --cov-report=html

# Run specific test file
uv run pytest tests/test_client.py
```

**Using pytest directly:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=jules_cli --cov-report=html

# Run specific test file
pytest tests/test_client.py
```

### Property-based testing

Property tests use Hypothesis and run with minimum 100 iterations by default.

## Requirements

- Python 3.8 or higher

## License

MIT
