.PHONY: run test lint format type build

run:
	uv run main.py

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format

type:
	uv run ty check

build:
	uv run PyInstaller --onefile --name pygitcollector main.py
