# Simple Makefile to run common tasks

.PHONY: help venv install test lint typecheck run uvicorn

VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

help:
	@echo "Available targets: venv, install, test, lint, typecheck, run, uvicorn"

venv:
	@echo "Creating virtual environment in $(VENV)..."
	python3 -m venv $(VENV)
	@echo "Upgrading pip in $(VENV)..."
	$(PY) -m pip install --upgrade pip

install: venv
	@echo "Installing dependencies from requirements.txt..."
	@$(PIP) install -r requirements.txt || (echo "\nInstallation failed. If you see errors building 'pycairo' or 'reportlab', please install system packages first (Debian/Ubuntu):"; echo "  sudo apt update && sudo apt install -y pkg-config libcairo2-dev libgirepository1.0-dev python3-dev build-essential"; echo "After that, re-run: make install"; exit 1)

system-deps:
	@echo "Install OS packages required to build native extensions on Debian/Ubuntu:";
	@echo "  sudo apt update && sudo apt install -y pkg-config libcairo2-dev libgirepository1.0-dev python3-dev build-essential"

test:
	@echo "Running tests..."
	$(PY) -m pytest -q

lint:
	@echo "Running flake8..."
	$(PY) -m flake8 src tests || true

typecheck:
	@echo "Running mypy..."
	$(PY) -m mypy src || true

run: install
	@echo "Starting application (development)..."
	$(PY) main.py

uvicorn:
	@echo "Starting uvicorn server"
	$(PY) -m uvicorn main:app --host 0.0.0.0 --port 8080

simulate:
	@echo "Running simulation via scripts/run_simulation.py"
	$(PY) scripts/run_simulation.py -n $(N) --seed $(SEED)
