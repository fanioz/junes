# Jules CLI

A command-line interface for the Jules REST API.

## Installation

### From source

```bash
# Clone the repository
git clone https://github.com/yourusername/jules-cli.git
cd jules-cli

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Using pip (when published)

```bash
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
