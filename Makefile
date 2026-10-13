.PHONY: help install test-creds run docker-build docker-up docker-down lint format test

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
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Run container via docker-compose"
	@echo "  make docker-down  - Stop running docker-compose container"

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

docker-build:
	docker build -t discord-groq-bot:latest .

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down
