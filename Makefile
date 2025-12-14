.PHONY: run test lint format type

run:
	uv run main.py

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format

type:
	uv run mypy .
