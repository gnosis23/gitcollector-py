# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**gitcollector** is a Python CLI tool for analyzing Git repository commit statistics. It provides:
- Total commit count
- Commit distribution by weekday (with percentages)
- Commit distribution by hour of day (with percentages)
- Bilingual support (English/Chinese via `--locale` flag)

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

# With Chinese locale
uv run main.py --locale zh
```

### Quality Assurance
```bash
# Run all tests
make test

# Lint code with Ruff
make lint

# Format code with Ruff
make format

# Type check with MyPy (strict mode)
make type
```

### Building
```bash
# Build standalone executable with PyInstaller
make build

# Output will be in dist/pygitcollector
```

### Testing (Detailed)
```bash
# Run all tests
uv run pytest

# Run a specific test file
uv run pytest collector/commit_test.py

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=collector
```

## Architecture

### Module Structure
- **`main.py`**: CLI entry point using Typer - handles output formatting with Rich tables
- **`collector/`**: Core business logic package
  - `commit.py`: Git command execution using `sh` library and commit parsing
  - `mytypes.py`: Data structures (dataclasses) for type safety
  - `util.py`: Helper functions for date/weekday calculations
  - `commit_test.py`: Unit tests for commit parsing

### Key Components
1. **Git Integration**: Uses `sh` library to run `git` commands (`rev-list`, `log`)
2. **Data Processing**: Parses git log output into structured `DailyCommitCount` and `DailyCommitHours` objects
3. **Analysis**: Calculates weekday and hour distributions with percentages
4. **CLI Presentation**: Formats and displays results with Rich tables and colored output

### Data Flow
1. `main.py` calls `count_commits()`, `get_daily_commit_counts()`, and `get_daily_commit_hours()` from `collector.commit`
2. `count_commits()` executes `git rev-list --count HEAD` for total commits
3. `get_daily_commit_counts()` executes `git log --format=%an <%ae>|%cd|%ai` and parses output with `parse_daily_commit_counts()`
4. `get_daily_commit_hours()` extracts hour information from commit timestamps
5. `get_weekday()` from `collector.util` converts dates to weekday indices (0=Sunday)
6. Results are aggregated by weekday/hour and percentages calculated
7. Rich tables display formatted results with proper alignment

### Data Types
- `DailyCommitCount`: Dataclass with `date` (YYYY-MM-DD string) and `count` (int)
- `DailyCommitHours`: Dataclass with `date` and `hours` (set[int])
- `ParsedTimestamp`: Dataclass for parsed timestamps with timezone awareness
- Functions use Python type hints with MyPy strict mode

## Development Guidelines

### Code Style
- Follow `.editorconfig` settings: 4-space indentation for Python, LF line endings
- Use type hints for all function signatures (MyPy strict mode enabled)
- Write docstrings in Chinese (current convention)
- Keep functions focused and modular
- Use pre-commit hooks with Ruff for linting and formatting

### Error Handling
- Use try-catch blocks for `sh.ErrorReturnCode` exceptions
- Print error messages to stderr when git commands fail
- Validate date formats in `get_weekday()`
- Check for `.git` directory existence before running

### Testing
- Test files use `_test.py` suffix (e.g., `commit_test.py`)
- Tests are located in the `collector/` module alongside source code
- Use `pytest` framework for unit testing
- Test both success and error cases for git command execution

### Dependencies
- Managed with **UV** (not pip)
- Main dependencies: `rich`, `sh`, `termcolor`, `typer`
- Development dependencies in `pyproject.toml` under `[dependency-groups.dev]`: `mypy`, `pyinstaller`, `pytest`, `ruff`
- Python 3.13+ required

### CI/CD Pipeline
- GitHub Actions workflow in `.github/workflows/release.yml`
- Triggers on version tags (vX.Y.Z)
- Builds executables for Linux, macOS (ARM64/Intel)
- Creates GitHub releases with platform-specific binaries
- Uses UV for dependency management

## Project Context

### Recent Development
The project has evolved through these features:
1. Initial setup and basic structure
2. Total commit counting (`git rev-list`)
3. Date-based commit analysis (`git log` parsing)
4. Weekday grouping and percentage calculations
5. Hour-of-day analysis
6. Bilingual support (English/Chinese)
7. CI/CD pipeline with multi-platform builds

### Current Features
- Analyzes current Git repository
- Provides total commit count
- Shows commit distribution by weekday with percentages
- Shows commit distribution by hour of day with percentages
- Bilingual output (English/Chinese)
- Standalone executable builds for multiple platforms
- Type-safe code with MyPy strict mode

### Extension Points
Potential areas for enhancement:
- Add command-line arguments for repository path
- Support for additional git statistics (author analysis, time-based patterns)
- Export options (JSON, CSV)
- Configuration file support
- Interactive mode with more detailed views
- Historical trend analysis