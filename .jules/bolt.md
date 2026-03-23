## 2025-02-26 - Lazy Importing Heavy Modules in CLI
**Learning:** Initializing heavy network libraries like `requests` at the module level severely impacts CLI startup time, even for commands that don't make network requests (like `--help`).
**Action:** Use lazy importing (importing inside the functions that actually need the library) to defer the cost until the library is actually used, dramatically speeding up general CLI responsiveness.

## 2025-02-27 - Lazy Importing Format Modules in CLI
**Learning:** Initializing heavy formatting libraries like `tabulate` at the module level heavily impacts CLI startup time, saving over 100ms when used lazily.
**Action:** Use lazy importing (importing inside the functions that actually need the library) to defer the cost until the library is actually used, further speeding up CLI responsiveness for default formats.

## 2026-03-11 - Lazy Loading Configuration Modules
**Learning:** Loading `tomllib` via `ConfigManager` globally at the module level in `cli.py` adds unnecessary latency (~15ms) to simple commands like `junes --help` that do not require an API key or configuration loading.
**Action:** Defer the instantiation and import of configuration managers to blocks that actually require them (e.g., after checking `ctx.invoked_subcommand is None`), optimizing the CLI startup time.
