## 2025-02-26 - Lazy Importing Heavy Modules in CLI
**Learning:** Initializing heavy network libraries like `requests` at the module level severely impacts CLI startup time, even for commands that don't make network requests (like `--help`).
**Action:** Use lazy importing (importing inside the functions that actually need the library) to defer the cost until the library is actually used, dramatically speeding up general CLI responsiveness.

## 2025-02-27 - Lazy Importing Format Modules in CLI
**Learning:** Initializing heavy formatting libraries like `tabulate` at the module level heavily impacts CLI startup time, saving over 100ms when used lazily.
**Action:** Use lazy importing (importing inside the functions that actually need the library) to defer the cost until the library is actually used, further speeding up CLI responsiveness for default formats.

## 2025-02-28 - Lazy Importing TOML Libraries in CLI Config
**Learning:** Initializing TOML libraries (`tomllib`/`tomli`) at the module level in `junes/config.py` impacts CLI startup time by about 0.01-0.02s, which adds up for quick commands like `--help`.
**Action:** Use lazy importing for `tomllib` and `tomli` inside the functions that actually need configuration parsing (`init_config` and `load_config`), saving startup time for default commands.
