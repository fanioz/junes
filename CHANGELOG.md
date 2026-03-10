# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-03-10

### Changed
- **PyPI package renamed to `junes`** (previously `jules-cli`)
- Package name conflict on PyPI required renaming
- Installation command: `pip install junes` (command remains `jules`)
- Updated package description to "junes: the Jules CLI"
- Added "junes" and "anthropic" keywords for better discoverability

### Note
- The `jules` command, GitHub repository, and all functionality remain unchanged
- This is a packaging-only change to enable PyPI distribution
- v1.0.0 release remains available on GitHub Releases

## [1.0.0] - 2026-03-10

### Added
- Initial stable release of jules-cli
- Full implementation of Jules REST API interface
- Commands: sources, sessions, activities, agent interaction
- Multiple output formats: json, table, plain
- Configuration management with API key handling
- Verbose mode for debugging
- One-line installer for easy setup
- Comprehensive test suite with 20 test files
- Property-based testing with Hypothesis
- 85%+ code coverage threshold

### Performance
- ⚡ Lazy loading of tabulate library (~100-120ms startup improvement)
- ⚡ Lazy loading of requests module
- ⚡ Lazy loading of API client and formatter
- Optimized CLI startup time for commands that don't use table formatting

### Changed
- Upgraded development status from Alpha to Production/Stable
- Improved code organization and cleanup

### Removed
- Temporary test report files (development artifacts)
- Unused imports across test files

### Fixed
- Removed unused variable in cli.py sessions_approve command
- Stabilized tests and output formatting

### Infrastructure
- Added uv.lock for reproducible dependency resolution
- Updated .gitignore for development tool directories
- Enhanced GitHub workflows

## [0.1.1] - Initial Development
- Initial project setup and core functionality
