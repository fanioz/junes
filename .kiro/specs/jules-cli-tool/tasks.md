# Implementation Plan: Jules CLI Tool

## Overview

This implementation plan breaks down the Jules CLI Tool into incremental coding tasks. The tool is a Python command-line interface for the Jules REST API, featuring authentication, multiple output formats, comprehensive error handling, and configuration management. Tasks are ordered to build core infrastructure first, then layer on commands and features, with testing integrated throughout.

## Tasks

- [ ] 1. Set up project structure and dependencies
  - Create directory structure: `jules_cli/` with `__init__.py`, `__main__.py`, `cli.py`, `client.py`, `config.py`, `formatter.py`, `exceptions.py`, `constants.py`
  - Create `tests/` directory with test files
  - Create `pyproject.toml` with dependencies: Click, requests, tomli/tomllib, tabulate, pytest, hypothesis, responses
  - Create `setup.py` for package installation
  - Create basic `README.md` with installation and usage instructions
  - _Requirements: 12.1, 13.1_

- [ ] 2. Implement exception hierarchy and constants
  - [ ] 2.1 Create custom exception classes in `exceptions.py`
    - Implement `JulesAPIError` base exception
    - Implement `AuthenticationError`, `ResourceNotFoundError`, `RateLimitError`, `ServerError`, `NetworkError`, `ConfigurationError`
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 11.6_
  
  - [ ] 2.2 Write unit tests for exception classes
    - Test exception inheritance and message formatting
    - _Requirements: 9.1-9.5_
  
  - [ ] 2.3 Define API constants in `constants.py`
    - Define base URL: `https://jules.googleapis.com/v1alpha`
    - Define API endpoints for all operations
    - Define header constants
    - _Requirements: 1.6, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1_

- [ ] 3. Implement configuration management
  - [ ] 3.1 Create `ConfigManager` class in `config.py`
    - Implement `init_config()` to create configuration file in `~/.jules-cli/config.toml`
    - Implement `load_config()` to read TOML configuration
    - Implement `get_api_key()` with priority: CLI > ENV > Config
    - Implement `validate_config()` for format validation
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_
  
  - [ ] 3.2 Write unit tests for configuration management
    - Test config file creation, reading, and validation
    - Test API key priority order with specific examples
    - Test invalid configuration handling
    - _Requirements: 1.1-1.4, 11.1-11.6_
  
  - [ ] 3.3 Write property test for API key priority
    - **Property 1: API Key Priority Order**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4**
  
  - [ ] 3.4 Write property test for configuration persistence
    - **Property 12: Configuration Persistence**
    - **Validates: Requirements 11.3, 11.4**
  
  - [ ] 3.5 Write property test for configuration validation
    - **Property 13: Configuration Validation**
    - **Validates: Requirements 11.5, 11.6**

- [ ] 4. Implement API client
  - [ ] 4.1 Create `JulesAPIClient` class in `client.py`
    - Implement `__init__()` with API key, base URL, and verbose flag
    - Implement `_make_request()` for HTTP requests with error handling
    - Map HTTP status codes to custom exceptions (401, 404, 429, 5xx)
    - Implement verbose logging with API key redaction
    - _Requirements: 1.5, 1.6, 9.1, 9.2, 9.3, 9.4, 9.5, 14.2, 14.3, 14.4_
  
  - [ ] 4.2 Implement API methods in `JulesAPIClient`
    - Implement `list_sources()` - GET /sources
    - Implement `create_session()` - POST /sessions
    - Implement `list_sessions()` - GET /sessions with optional status filter
    - Implement `get_session()` - GET /sessions/{session_id}
    - Implement `approve_plan()` - POST /sessions/{session_id}/approve
    - Implement `list_activities()` - GET /sessions/{session_id}/activities
    - Implement `send_message()` - POST /sessions/{session_id}/messages
    - _Requirements: 2.1, 3.1, 4.1, 4.6, 5.1, 6.1, 7.1, 8.1_
  
  - [ ] 4.3 Write unit tests for API client
    - Test each API method with mocked responses using `responses` library
    - Test error handling for 401, 404, 429, 5xx, network errors
    - Test API key header inclusion
    - Test verbose logging and API key redaction
    - _Requirements: 1.6, 2.1-2.3, 3.1-3.3, 4.1-4.3, 5.1-5.4, 6.1-6.3, 7.1-7.3, 8.1-8.3, 9.1-9.5, 14.2-14.4_
  
  - [ ] 4.4 Write property test for API key header inclusion
    - **Property 4: API Key Header Inclusion**
    - **Validates: Requirements 1.6**
  
  - [ ] 4.5 Write property test for API error display
    - **Property 2: API Error Display**
    - **Validates: Requirements 2.3, 3.3, 4.3, 5.3, 6.3, 7.3, 8.3**
  
  - [ ] 4.6 Write property test for server error handling
    - **Property 9: Server Error Handling**
    - **Validates: Requirements 9.4**
  
  - [ ] 4.7 Write property test for verbose HTTP logging
    - **Property 16: Verbose HTTP Logging**
    - **Validates: Requirements 14.2, 14.3**
  
  - [ ] 4.8 Write property test for API key redaction
    - **Property 17: API Key Redaction**
    - **Validates: Requirements 14.4**

- [ ] 5. Implement output formatting
  - [ ] 5.1 Create `OutputFormatter` class in `formatter.py`
    - Implement `__init__()` with format type (json, table, plain)
    - Implement `format_sources()` for sources list
    - Implement `format_sessions()` for sessions list
    - Implement `format_session_details()` for single session
    - Implement `format_activities()` for activities list with chronological ordering
    - Implement `format_message_response()` for agent responses
    - Implement `format_error()` for error messages
    - Support JSON, table (using tabulate), and plain text formats
    - _Requirements: 2.2, 2.4, 2.5, 4.2, 4.4, 4.5, 5.2, 5.5, 7.2, 7.4, 7.5, 7.6, 8.2, 8.6, 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [ ] 5.2 Write unit tests for output formatting
    - Test JSON, table, and plain text formats with sample data
    - Test chronological ordering of activities
    - Test JSON validity
    - _Requirements: 2.4, 2.5, 4.4, 4.5, 5.5, 7.4, 7.5, 7.6, 8.6, 10.1-10.5_
  
  - [ ] 5.3 Write property test for complete field display
    - **Property 7: Complete Field Display**
    - **Validates: Requirements 4.2, 5.2, 7.2, 8.2**
  
  - [ ] 5.4 Write property test for chronological activity ordering
    - **Property 8: Chronological Activity Ordering**
    - **Validates: Requirements 7.6**
  
  - [ ] 5.5 Write property test for JSON output validity
    - **Property 10: JSON Output Validity**
    - **Validates: Requirements 10.5**
  
  - [ ] 5.6 Write property test for JSON round-trip
    - **Property 11: JSON Round-Trip Property**
    - **Validates: Requirements 10.6**

- [ ] 6. Implement CLI interface foundation
  - [ ] 6.1 Create main CLI group in `cli.py`
    - Implement main `@click.group()` with global options: `--api-key`, `--format`, `--verbose`, `--version`
    - Implement context object to pass configuration to commands
    - Implement version flag handler
    - Implement help flag handler
    - Set up API key resolution using `ConfigManager.get_api_key()`
    - Handle missing API key error
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 10.1, 10.2, 10.3, 10.4, 12.1, 12.3, 13.1, 13.2, 14.1_
  
  - [ ] 6.2 Create entry point in `__main__.py`
    - Import and invoke CLI group
    - Handle top-level exceptions
    - _Requirements: 1.5, 9.6_
  
  - [ ] 6.3 Write unit tests for CLI foundation
    - Test version flag output
    - Test help flag output
    - Test missing API key error
    - Test global options parsing
    - _Requirements: 1.5, 12.1, 12.3, 13.1, 13.2_
  
  - [ ] 6.4 Write property test for exit code correctness
    - **Property 3: Exit Code Correctness**
    - **Validates: Requirements 1.5, 3.5, 5.4, 6.5, 9.6**

- [ ] 7. Implement sources commands
  - [ ] 7.1 Implement `sources list` command
    - Create `@click.command()` for listing sources
    - Call `JulesAPIClient.list_sources()`
    - Format output using `OutputFormatter.format_sources()`
    - Handle errors and display error messages
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  
  - [ ] 7.2 Write unit tests for sources commands
    - Test successful list with JSON and table formats
    - Test error handling
    - _Requirements: 2.1-2.5_

- [ ] 8. Implement sessions commands
  - [ ] 8.1 Implement `sessions create` command
    - Create `@click.command()` for creating sessions with source ID argument
    - Support optional parameters via `**kwargs`
    - Call `JulesAPIClient.create_session()`
    - Display session ID on success
    - Handle errors and display error messages
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_
  
  - [ ] 8.2 Implement `sessions list` command
    - Create `@click.command()` for listing sessions
    - Support optional `--status` filter
    - Call `JulesAPIClient.list_sessions()`
    - Format output using `OutputFormatter.format_sessions()`
    - Handle errors and display error messages
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_
  
  - [ ] 8.3 Implement `sessions get` command
    - Create `@click.command()` for getting session details with session ID argument
    - Call `JulesAPIClient.get_session()`
    - Format output using `OutputFormatter.format_session_details()`
    - Handle errors including 404 for non-existent sessions
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [ ] 8.4 Implement `sessions approve` command
    - Create `@click.command()` for approving plans with session ID argument
    - Call `JulesAPIClient.approve_plan()`
    - Display confirmation message on success
    - Handle errors including no pending plan scenario
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [ ] 8.5 Write unit tests for sessions commands
    - Test create, list, get, approve with various scenarios
    - Test optional parameters and filters
    - Test error handling for each command
    - _Requirements: 3.1-3.5, 4.1-4.6, 5.1-5.5, 6.1-6.5_
  
  - [ ] 8.6 Write property test for optional parameter pass-through
    - **Property 5: Optional Parameter Pass-Through**
    - **Validates: Requirements 3.4**
  
  - [ ] 8.7 Write property test for session filter pass-through
    - **Property 6: Session Filter Pass-Through**
    - **Validates: Requirements 4.6**

- [ ] 9. Implement activities commands
  - [ ] 9.1 Implement `activities list` command
    - Create `@click.command()` for listing activities with session ID argument
    - Call `JulesAPIClient.list_activities()`
    - Format output using `OutputFormatter.format_activities()` with chronological ordering
    - Handle errors and display error messages
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_
  
  - [ ] 9.2 Write unit tests for activities commands
    - Test successful list with JSON and table formats
    - Test chronological ordering
    - Test error handling
    - _Requirements: 7.1-7.6_

- [ ] 10. Implement agent interaction commands
  - [ ] 10.1 Implement `agent send` command
    - Create `@click.command()` for sending messages with session ID and message arguments
    - Support reading message from stdin when no argument provided
    - Call `JulesAPIClient.send_message()`
    - Format output using `OutputFormatter.format_message_response()`
    - Handle errors and display error messages
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_
  
  - [ ] 10.2 Write unit tests for agent commands
    - Test sending message with argument
    - Test reading message from stdin
    - Test JSON output format
    - Test error handling
    - _Requirements: 8.1-8.6_

- [ ] 11. Implement config command
  - [ ] 11.1 Implement `config init` command
    - Create `@click.command()` for initializing configuration
    - Prompt for API key and output format
    - Call `ConfigManager.init_config()`
    - Display success message with config file location
    - Handle errors and display error messages
    - _Requirements: 11.1, 11.2, 11.3, 11.4_
  
  - [ ] 11.2 Write unit tests for config command
    - Test config initialization
    - Test config file creation in home directory
    - Test error handling
    - _Requirements: 11.1-11.4_

- [ ] 12. Implement help and documentation
  - [ ] 12.1 Add help text and examples to all commands
    - Add docstrings to all command functions
    - Add help text to all command arguments and options
    - Add usage examples in command help
    - Ensure help displays command syntax with required/optional parameters
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_
  
  - [ ] 12.2 Write unit tests for help system
    - Test help flag for each command
    - Test help content includes syntax and examples
    - Test no arguments shows available commands
    - _Requirements: 12.1-12.5_
  
  - [ ] 12.3 Write property test for command help availability
    - **Property 14: Command Help Availability**
    - **Validates: Requirements 12.2**
  
  - [ ] 12.4 Write property test for help content completeness
    - **Property 15: Help Content Completeness**
    - **Validates: Requirements 12.4, 12.5**

- [ ] 13. Implement verbose mode
  - [ ] 13.1 Add verbose logging throughout the application
    - Ensure verbose flag is passed to `JulesAPIClient`
    - Implement logging in `_make_request()` for HTTP details
    - Ensure API key redaction in all log output
    - Ensure non-verbose mode only shows results and errors
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_
  
  - [ ] 13.2 Write unit tests for verbose mode
    - Test verbose logging enabled/disabled
    - Test API key redaction
    - Test log output suppression when disabled
    - _Requirements: 14.1-14.5_
  
  - [ ] 13.3 Write property test for verbose mode suppression
    - **Property 18: Verbose Mode Suppression**
    - **Validates: Requirements 14.5**

- [ ] 14. Checkpoint - Ensure all tests pass
  - Run all unit tests and property tests
  - Verify test coverage meets goals (90% line coverage, 85% branch coverage)
  - Ensure all tests pass, ask the user if questions arise

- [ ] 15. Integration and final wiring
  - [ ] 15.1 Wire all components together
    - Ensure all commands are registered with CLI group
    - Ensure error handling flows correctly through all layers
    - Ensure configuration loading works end-to-end
    - Ensure output formatting works for all commands
    - _Requirements: All requirements_
  
  - [ ] 15.2 Create package installation configuration
    - Finalize `pyproject.toml` with all metadata
    - Finalize `setup.py` with entry points
    - Test package installation with `pip install -e .`
    - _Requirements: 12.1, 13.1_
  
  - [ ] 15.3 Write integration tests
    - Test end-to-end command execution flows
    - Test error propagation through all layers
    - Test configuration → API client → formatter pipeline
    - _Requirements: All requirements_

- [ ] 16. Final checkpoint - Ensure all tests pass
  - Run complete test suite including all unit and property tests
  - Verify all acceptance criteria are covered
  - Ensure all tests pass, ask the user if questions arise

## Notes

- Each task references specific requirements for traceability
- Property tests validate universal correctness properties across randomized inputs
- Unit tests validate specific examples, edge cases, and command existence
- The implementation uses Python 3.8+ with Click, requests, tabulate, pytest, and hypothesis
- All property tests should run with minimum 100 iterations
- Checkpoints ensure incremental validation at key milestones
