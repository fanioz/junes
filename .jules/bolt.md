## 2025-02-26 - Lazy Importing Heavy Modules in CLI
**Learning:** Initializing heavy network libraries like `requests` at the module level severely impacts CLI startup time, even for commands that don't make network requests (like `--help`).
**Action:** Use lazy importing (importing inside the functions that actually need the library) to defer the cost until the library is actually used, dramatically speeding up general CLI responsiveness.

## 2025-02-27 - Lazy Importing Format Modules in CLI
**Learning:** Initializing heavy formatting libraries like `tabulate` at the module level heavily impacts CLI startup time, saving over 100ms when used lazily.
**Action:** Use lazy importing (importing inside the functions that actually need the library) to defer the cost until the library is actually used, further speeding up CLI responsiveness for default formats.

## 2025-02-28 - Lazy Importing Configuration Modules in CLI
**Learning:** Initializing configuration modules that rely on `tomllib` / `tomli` at the module level in CLI commands causes a measurable slowdown during startup. When `junes.config.ConfigManager` imported `tomllib` globally, this contributed around 10ms to the startup time of all commands, including commands that do not load configs like `--help`.
**Action:** Move library imports for file parsing (like `tomllib` and `tomli_w`) into the specific methods that require them (`init_config`, `load_config`), deferring the performance cost until configuration is actively used.
