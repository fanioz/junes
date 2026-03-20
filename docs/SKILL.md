---
name: junes
description: Use when the user mentions junes, Jules REST API, or needs to perform Jules operations like listing sources, creating sessions, managing activities, sending agent messages, or configuring API credentials. Trigger symptoms: asks about junes commands, Jules API interactions, session management, or authentication issues. Error patterns: "Authentication failed", "Resource not found", "API key not found".
compatibility:
  tools:
    - Bash
  requirements:
    - junes must be installed and available in PATH (pip install junes)
    - API key configured via junes config init, JULES_API_KEY env var, or --api-key option
---

# junes CLI

Command-line interface for the Jules REST API - manage coding sessions, sources, activities, and agent communication.

## Overview

junes wraps the Jules REST API for programmatic session management and agent interaction.

**Core pattern:** `junes [global-options] <category> <command> [args]`

`★ Insight ─────────────────────────────────────`
**Naming clarification:** The CLI tool is "junes" but the service is "Jules API". Environment variable `JULES_API_KEY` references the service name, not the CLI tool name.
`─────────────────────────────────────────────────`

## Quick Reference - Commands

| Category | Command | Purpose |
|----------|---------|---------|
| **sessions** | `list` | List all sessions with optional filters |
| **sessions** | `create` | Create new coding session |
| **sessions** | `get` | Get session details |
| **sessions** | `delete` | Delete a session |
| **sessions** | `approve` | Approve pending plan |
| **agent** | `send` | Send message to session |
| **activities** | `list` | List session activities |
| **sources** | `list` | List available sources |
| **sources** | `get` | Get source details |
| **config** | `init` | Set up configuration file |

## Quick Start

**Initialize configuration:**
```bash
junes config init
```

This prompts for:
- API key (hidden input)
- Default output format (json/table/plain)

## Debugging Rules

**When troubleshooting configuration or authentication issues:**

1. **NEVER claim a bug exists without reading the actual code** - Use the Read tool to verify before claiming bugs
2. **Always verify user's command examples** - They may be outdated or reference old command names ("jules" vs "junes")
3. **Check actual file paths** - Use `ls` or `cat` commands to verify what exists
4. **Environment variable JULES_API_KEY is correct** - It references the SERVICE name "Jules", not the CLI tool "junes"
5. **Common non-bugs:**
   - User's command uses "jules" instead of "junes" (rebranding confusion)
   - User references old config path `~/.jules-cli/` (should be `~/.junes/`)
   - Environment variable name seems "wrong" but is correct (JULES_API_KEY, not JUNES_API_KEY)

`★ Insight ─────────────────────────────────────`
**Fabrication prevention:** When debugging, agents feel compelled to "find the bug." If you think there's a bug, READ THE ACTUAL FILE first. Never claim a bug exists without verification.
`─────────────────────────────────────────────────`

## Authentication

**API key priority order:**

1. **CLI option** (highest): `junes --api-key "YOUR_KEY" sessions list`
2. **Environment variable:** `export JULES_API_KEY="YOUR_KEY"`
3. **Config file:** `junes config init` (stored at `~/.junes/config.toml`)

**Config file location:** `~/.junes/config.toml`

**View config:**
```bash
cat ~/.junes/config.toml
```

`★ Insight ─────────────────────────────────────`
**Global option placement:** `--format` and `--api-key` are global options that go BEFORE the subcommand. Use `junes --format json sessions list` not `junes sessions list --format json`.
`─────────────────────────────────────────────────`

## Output Formats

| Format | Use Case |
|--------|----------|
| `json` | Parsing/processing data programmatically |
| `table` | Displaying structured data for review |
| `plain` | Human-readable summaries (default) |

**Example:**
```bash
junes --format json sources list    # Parse with jq
junes --format table sessions list  # Review with eyes
junes --format plain sessions get   # Simple display
```

## Session Management

### List sessions
```bash
junes sessions list                                    # All sessions
junes sessions list --status active                    # Filter by status
junes sessions list --source sources/github/org/repo   # Filter by repository
junes sessions list --page-size 50                     # Pagination
```

### Create session
```bash
# Basic session
junes sessions create <source-id>

# With parameters
junes sessions create <source-id> --parameter key=value
junes sessions create <source-id> -p key1=value1 -p key2=value2
```

**Capture the returned session ID** for subsequent operations.

### Get session details
```bash
junes sessions get <session-id>
junes --format json sessions get <session-id>    # For parsing
```

### Approve session plan
```bash
junes sessions approve <session-id>
```

### Delete session
```bash
junes sessions delete <session-id>       # With confirmation
```

## Sources Management

**List available sources:**
```bash
junes sources list
junes --format json sources list
junes --format table sources list
```

**Get source details:**
```bash
junes sources get <source-id>
junes --format json sources get <source-id>
```

## Agent Interaction

**Send message to session:**
```bash
# Direct message
junes agent send <session-id> "Your message here"

# Piped message
echo "Your message" | junes agent send <session-id>

# From file
cat message.txt | junes agent send <session-id>
```

## Activity Management

**List activities for a session:**
```bash
junes activities list <session-id>
junes --format json activities list <session-id>
junes --format table activities list <session-id>
```

## Common Workflows

### Workflow 1: Create Session and Interact
```bash
# 1. List available sources
junes --format json sources list

# 2. Create a session
junes --format json sessions create <source-id>
# Save the returned session ID

# 3. Check session status and plan
junes sessions get <session-id>

# 4. Approve the plan if needed
junes sessions approve <session-id>

# 5. Monitor activities
junes activities list <session-id>

# 6. Send message to agent
junes agent send <session-id> "What's the status?"
```

### Workflow 2: Monitor Session Progress
```bash
# Get session details as JSON
junes --format json sessions get <session-id>

# List activities as table
junes --format table activities list <session-id>

# Approve if pending
junes sessions approve <session-id>
```

### Workflow 3: Batch Operations with JSON Parsing
```bash
# Extract active session IDs using jq
junes --format json sessions list --status active | jq -r '.[].id'

# Extract IDs using text parsing (if jq unavailable)
junes sessions list --status active | awk '{print $3}' | grep -E '^[0-9]+$'
```

`★ Insight ─────────────────────────────────────`
**Rate limiting:** Sending messages to many sessions quickly triggers 429 errors. Add delays (5s+) between sends when batching.
`─────────────────────────────────────────────────`

## Pagination Pattern

```bash
# Get first page
junes sessions list --page-size 30 --format json > page1.json

# Extract nextPageToken and get next page
TOKEN=$(jq -r '.nextPageToken' page1.json)
junes sessions list --page-size 30 --page-token "$TOKEN" --format json
```

## Verbose Mode

Enable verbose logging to debug API requests:
```bash
junes --verbose sources list
```

Shows HTTP request details including headers, endpoints, and response status.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Authentication failed` | Invalid/missing API key | Run `junes config init` or set `JULES_API_KEY` |
| `Resource not found` | Invalid source/session ID | Verify the ID exists |
| `Rate limit exceeded` | Too many requests | Wait before retrying |
| `Server error` | API is down | Retry later |
| `API key not found` | No key configured | Provide via `--api-key`, env var, or config |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Wrong `--format` placement | Global options go before subcommand: `junes --format json sessions list` |
| Forgetting `--status` filter | Use filters to narrow results: `--status active` |
| No delays when batch messaging | Add 5s+ delays to avoid 429 rate limit errors |
| Not using JSON for parsing | Use `--format json` with `jq` for programmatic access |
| Missing session ID after create | Capture and save the returned ID from `sessions create` |
| **Trusting user's command examples** | **Verify before using - user may reference old "jules" command** |
| **Claiming bugs without reading code** | **ALWAYS Read tool to verify before claiming bugs exist** |
| **Confusing CLI vs service names** | **CLI is "junes", service is "Jules API", env var is JULES_API_KEY** |

## Red Flags - STOP and Verify

You are about to make a mistake if:

- **About to claim "there's a bug in the code"** → Read the file first
- **User's command example uses "jules"** → Correct to "junes" (rebranding)
- **About to suggest changing env var from JULES_API_KEY** → This is CORRECT (service name)
- **User says config is at ~/.jules-cli/** → Correct to ~/.junes/ (rebranded path)
- **About to modify code without reading it** → Use Read tool to verify actual contents

**All of these mean: Stop. Read actual files. Verify. Then respond.**

## Best Practices

1. **Place global flags correctly:** `junes --format json <subcommand>` not `junes <subcommand> --format json`

2. **Capture session IDs:** Save the returned ID when creating sessions

3. **Check session status before acting:** Use `junes sessions get` to verify state

4. **Use verbose mode for debugging:** Add `--verbose` when troubleshooting

5. **Use appropriate output format:** JSON for parsing, table for review, plain for simple display

6. **Add delays when batching:** Prevent rate limiting with `sleep 5` between operations
