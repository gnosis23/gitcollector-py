.PHONY: run test lint format

run:
	uv run main.py

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format
