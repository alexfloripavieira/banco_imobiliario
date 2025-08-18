# Simple Makefile to run common tasks

.PHONY: help install test lint typecheck run uvicorn

help:
	@echo "Available targets: install, test, lint, typecheck, run, uvicorn"

install:
	@echo "Installing dependencies from requirements.txt..."
	pip3 install -r requirements.txt

test:
	@echo "Running tests..."
	pytest -q

lint:
	@echo "Running flake8..."
	flake8 src tests || true

typecheck:
	@echo "Running mypy..."
	mypy src || true

run:
	@echo "Starting application (development)..."
	python3 main.py

uvicorn:
	@echo "Starting uvicorn server"
	uvicorn main:app --host 0.0.0.0 --port 8080
