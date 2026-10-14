.PHONY: help install test-creds run lint format test

PYTHON := .venv/bin/python
PIP := .venv/bin/pip

help:
	@echo "Available make commands:"
	@echo "  make install      - Create venv and install dependencies"
	@echo "  make test-creds   - Run credentials and API pre-flight check"
	@echo "  make run          - Launch the Discord bot locally"
	@echo "  make test         - Run automated test suite"
	@echo "  make lint         - Run ruff linter check"
	@echo "  make format       - Format code using ruff"

install:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-asyncio ruff

test-creds:
	$(PYTHON) test_credentials.py

run:
	$(PYTHON) bot.py

test:
	$(PYTHON) -m pytest tests/

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format .

