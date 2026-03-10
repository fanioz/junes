---
name: junes
description: Use when the user mentions junes, Jules REST API, or needs to perform Jules operations like listing sources, creating sessions, managing activities, sending agent messages, or configuring API credentials. Trigger symptoms: asks about junes commands, Jules API interactions, session management, or authentication issues with junes. Includes error messages like "Authentication failed" or "Resource not found".
compatibility:
  tools:
    - Bash
  requirements:
    - junes must be installed and available in PATH
    - API key configured via junes config init, JULES_API_KEY env var, or --api-key option
---

# Jules CLI Skill

Use this skill to interact with the Jules REST API through the jules-cli command-line tool.

## Overview

This skill enables Claude to perform all jules-cli operations:
- List and manage sources
- Create, list, get, and approve sessions
- List and review activities
- Send messages to the agent
- Configure API credentials

## Quick Start

First, ensure the user has configured their API key:

```bash
jules config init
```

If the API key is not configured, check for the `JULES_API_KEY` environment variable or prompt the user to provide it.

## Core Capabilities

### 1. Sources Management

**List available sources:**

```bash
jules sources list
jules --format json sources list    # For parsing
jules --format table sources list   # For display
jules --format plain sources list   # Default
```

**Note:** Global options like `--format` and `--api-key` must come **before** the subcommand.

### 2. Session Management

**Create a new session:**

```bash
jules sessions create <source-id>
jules sessions create <source-id> --parameter key=value
jules sessions create <source-id> -p key1=value1 -p key2=value2
```

When creating a session, capture the returned session ID for subsequent operations.

**List sessions:**

```bash
jules sessions list
jules sessions list --status active
jules sessions list --status completed
jules --format json sessions list
```

**Get session details:**

```bash
jules sessions get <session-id>
jules --format json sessions get <session-id>
```

**Approve a pending plan:**

```bash
jules sessions approve <session-id>
```

### 3. Activity Management

**List activities for a session:**

```bash
jules activities list <session-id>
jules --format json activities list <session-id>
jules --format table activities list <session-id>
```

### 4. Agent Interaction

**Send a message to the agent:**

```bash
# Direct message
jules agent send <session-id> "Your message here"

# Piped message
echo "Your message" | jules agent send <session-id>

# From file
cat message.txt | jules agent send <session-id>
```

### 5. Configuration

**Initialize configuration:**

```bash
jules config init
```

This prompts for:
- API key (hidden input)
- Default output format (json/table/plain)

## Output Format Selection

Choose the appropriate output format based on the task:

| Format | Use Case |
|--------|----------|
| `json` | When you need to parse, process, or extract data programmatically |
| `table` | When displaying structured data to the user for review |
| `plain` | When presenting human-readable summaries or simple text |

**Important:** The `--format` flag is a **global** flag and must be placed immediately after `jules` and before the subcommand.

**Example workflow:**

```bash
# Get sources as JSON for parsing
jules --format json sources list

# Get session details for display
jules --format table sessions get abc123

# Check activity status programmatically
jules --format json activities list abc123 | jq '.[0].status'
```

## API Key Handling

The API key can be provided in three ways (priority order):

1. **CLI option:** `jules --api-key YOUR_KEY sources list`
2. **Environment variable:** `export JULES_API_KEY=YOUR_KEY`
3. **Config file:** `jules config init` (stored at `~/.jules-cli/config.toml`)

If a command fails with authentication error, prompt the user to:
- Run `jules config init` to set up configuration, OR
- Set the `JULES_API_KEY` environment variable, OR
- Provide the key via `--api-key` option

## Verbose Mode

Enable verbose logging to debug API requests:

```bash
jules --verbose sources list
```

This shows HTTP request details including headers, endpoints, and response status.

## Common Workflows

### Workflow 1: Create Session and Interact

```bash
# 1. List available sources
jules --format json sources list

# 2. Create a session with a specific source
jules --format json sessions create <source-id>

# 3. Check session status and plan
jules sessions get <session-id>

# 4. Approve the plan if needed
jules sessions approve <session-id>

# 5. Monitor activities
jules activities list <session-id>

# 6. Send a message to the agent
jules agent send <session-id> "What's the status?"
```

### Workflow 2: Monitor Session Progress

```bash
# Get session details
jules --format json sessions get <session-id>

# List recent activities
jules --format table activities list <session-id>

# If plan is pending, approve it
jules sessions approve <session-id>
```

### Workflow 3: Batch Operations (Text Parsing Examples)

While JSON is the preferred format for parsing, you can also use standard text processing tools:

```bash
# List all active sessions and extract IDs using JSON + jq
jules --format json sessions list --status active | jq -r '.[].id'

# List all active sessions and extract IDs using text parsing (awk/grep)
# Assuming IDs are in the 3rd column of the default plain/table output
jules sessions list --status active | awk '{print $3}' | grep -E '^[0-9]+$'
```

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `Authentication failed` | Invalid/missing API key | Check API key configuration |
| `Resource not found` | Invalid source/session ID | Verify the ID exists |
| `Rate limit exceeded` | Too many requests | Wait before retrying |
| `Server error` | API is down | Retry later |
| `Error: No such option: --format` | Flag in wrong position | Place `--format` BEFORE the subcommand |

## Best Practices

1. **Place global flags correctly:** Always use `jules --format json <subcommand>` not `jules <subcommand> --format json`.

2. **Capture session IDs:** When creating sessions, save the returned ID for subsequent operations.

3. **Check session status before acting:** Use `jules sessions get` to verify state before approving or sending messages.

4. **Use verbose mode for debugging:** Add `--verbose` when troubleshooting API issues.

5. **Filter sessions by status:** Use `--status` flag to list only active/completed sessions.

6. **Use appropriate output format:** Match the format to your use case (json for parsing, table for review, plain for simple display).
