.PHONY: run test

run:
	uv run main.py

test:
	uv run pytest
