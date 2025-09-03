# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<critical>
 - **YOU MUST** see @.claude/rules/code-standards.md
  - **YOU MUST** see @.claude/rules/review.md
  - **YOU MUST** use Serena MCP to discovers and edits code for instead of the READ, WRITE, UPDATE tool
</critical>

## Project Overview

This is a Monopoly board game simulator (Banco Imobiliário) implemented in Python using clean architecture principles with domain-driven design. The project simulates games between 4 different player strategies and provides both JSON and HTML outputs.

## Architecture

The codebase follows a layered architecture:

- **Domain Layer** (`src/domain/`): Core business entities (`Player`, `Property`)
- **Use Cases** (`src/usecases/`): Game simulation logic and orchestration
- **Adapters** (`src/adapters/`): Player strategy implementations
- **Interface** (`src/interfaces/`): FastAPI HTTP endpoints
- **Scripts** (`scripts/`): CLI utilities for simulation

## Development Commands

### Environment Setup
```bash
make install    # Create venv and install dependencies
make system-deps # Install OS packages (Ubuntu/Debian) if needed
```

### Running the Application
```bash
make run        # Start development server on port 8080
make uvicorn    # Alternative server startup
make down       # Stop all application processes
```

### Testing and Quality
```bash
make test       # Run pytest
make lint       # Run flake8
make typecheck  # Run mypy
```

### Simulations
```bash
make simulate N=10 SEED=42  # Run CLI simulation
```

## API Endpoints

- `POST /jogo/simular` - JSON simulation endpoint
- `GET /` - HTML form interface

The API supports content negotiation via Accept headers (JSON/HTML).

## Player Strategies

Four strategies are implemented in `src/adapters/strategies.py`:
- **impulsivo**: Always buys properties
- **exigente**: Buys only if rent > 50
- **cauteloso**: Buys only if keeps 80+ balance
- **aleatorio**: Random 50% purchase probability

## Configuration

- Python 3.8+ required
- Virtual environment managed automatically via Makefile
- Code style: flake8 with 88-char line limit
- Type checking: mypy
- Testing: pytest

## Key Files

- `main.py` - Application entry point
- `src/usecases/game.py:70` - Main simulation function `simulate_games()`
- `src/interfaces/api.py:96` - Primary API endpoint
- `Makefile` - All development commands


- **YOU MUST** see @.claude/rules/code-standards.md
- **YOU MUST** see .claude/rules/review.md