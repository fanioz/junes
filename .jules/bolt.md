## 2025-02-26 - Lazy Importing Heavy Modules in CLI
**Learning:** Initializing heavy network libraries like `requests` at the module level severely impacts CLI startup time, even for commands that don't make network requests (like `--help`).
**Action:** Use lazy importing (importing inside the functions that actually need the library) to defer the cost until the library is actually used, dramatically speeding up general CLI responsiveness.
