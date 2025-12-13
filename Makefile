.PHONY: run test lint

run:
	uv run main.py

test:
	uv run pytest

lint:
	uv run ruff check .
