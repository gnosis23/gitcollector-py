# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**gitcollector** is a Python tool for analyzing Git repository commit statistics. It provides total commit counts and weekday distribution analysis for the current Git repository.

## Development Commands

### Setup and Installation
```bash
# Install dependencies using UV (modern Python package manager)
uv sync

# Create virtual environment (optional, UV handles this)
uv venv
```

### Running the Application
```bash
# Run the main application
make run

# Or directly with UV
uv run main.py
```

### Testing
```bash
# Run all tests
make test

# Or directly with pytest
uv run pytest

# Run a specific test file
uv run pytest collector/commit_test.py

# Run with verbose output
uv run pytest -v
```

## Architecture

### Module Structure
- **`main.py`**: CLI entry point - handles output formatting and display
- **`collector/`**: Core business logic package
  - `commit.py`: Git command execution and commit parsing
  - `types.py`: Data structures (dataclasses) for type safety
  - `util.py`: Helper functions for date/weekday calculations
  - `commit_test.py`: Unit tests for commit parsing

### Key Components
1. **Git Integration**: Uses `subprocess` to run `git` commands (`rev-list`, `log`)
2. **Data Processing**: Parses git log output into structured `DailyCommitCount` objects
3. **Analysis**: Calculates weekday distributions and percentages
4. **CLI Presentation**: Formats and displays results with ASCII art header

### Data Flow
1. `main.py` calls `count_commits()` and `get_daily_commit_counts()` from `collector.commit`
2. `count_commits()` executes `git rev-list --count HEAD` for total commits
3. `get_daily_commit_counts()` executes `git log --format=%an <%ae>|%cd|%ai` and parses output
4. `parse_daily_commit_counts()` aggregates commits by date
5. `get_weekday()` from `collector.util` converts dates to weekday indices (0=Sunday)
6. Results are aggregated by weekday and percentages calculated

### Data Types
- `DailyCommitCount`: Dataclass with `date` (YYYY-MM-DD string) and `count` (int)
- Functions use Python type hints for clarity

## Development Guidelines

### Code Style
- Follow `.editorconfig` settings: 4-space indentation for Python, LF line endings
- Use type hints for all function signatures
- Write docstrings in Chinese (current convention)
- Keep functions focused and modular

### Error Handling
- Use try-catch blocks for `subprocess` calls
- Print error messages to stderr when git commands fail
- Validate date formats in `get_weekday()`

### Testing
- Test files use `_test.py` suffix (e.g., `commit_test.py`)
- Tests are located in the `collector/` module alongside source code
- Use `pytest` framework for unit testing

### Dependencies
- Managed with **UV** (not pip)
- Development dependencies in `pyproject.toml` under `[dependency-groups.dev]`
- Python 3.13+ required

## Project Context

### Recent Development
The project has evolved through these features:
1. Initial setup and basic structure
2. Total commit counting (`git rev-list`)
3. Date-based commit analysis (`git log` parsing)
4. Weekday grouping and percentage calculations

### Current Limitations
- Only analyzes current Git repository (no path arguments)
- Basic CLI with no command-line options
- Limited test coverage
- Minimal documentation

### Extension Points
Potential areas for enhancement:
- Add command-line arguments for repository path
- Support for additional git statistics (author analysis, time-based patterns)
- Export options (JSON, CSV)
- Configuration file support
- CI/CD pipeline integration