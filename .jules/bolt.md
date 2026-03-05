## 2024-05-28 - [Lazy Imports Speed Up Python CLI]
**Learning:** Eager imports of heavy modules like `requests` and `tabulate` at the module level can significantly slow down the startup time of CLI applications (e.g. from ~70ms to ~280ms purely for imports), which is very noticeable to users on quick commands like `--help`.
**Action:** Use lazy imports within the specific command functions that need them rather than module-level imports for heavy dependencies in CLI tools.
