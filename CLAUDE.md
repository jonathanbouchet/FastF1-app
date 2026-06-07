# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference

### Setup
```bash
uv sync                                 # Install dependencies
```

### Run
```bash
uv run uvicorn src.app:app --reload    # Start development server (http://localhost:8000)
```

### Testing
```bash
uv run pytest                           # Run all tests
uv run pytest tests/test_endpoints.py   # Run specific test file
uv run pytest tests/test_endpoints.py::test_health_check  # Run specific test
```

## Project Overview

FastAPI backend for F1 data visualization using FastF1 as the data source. The project follows PEP-8 style and uses Pydantic for validation.

**Stack:** FastAPI, Pydantic, FastF1, pytest

### Project Structure
```
src/
  app.py               # FastAPI application with all endpoints
  models/              # Pydantic models for validation
    __init__.py
    health.py          # HealthResponse model
    year.py            # YearAvailabilityResponse model
tests/
  test_endpoints.py    # Endpoint tests (one test per endpoint minimum)
```

### Key Dependencies
- `fastapi` — Web framework
- `pydantic` — Request/response validation
- `fastf1` — F1 data provider
- `pytest`, `httpx` — Testing (dev dependencies)

## Development

### Adding New Endpoints
Use the `/add-endpoint` skill for guided workflow. Steps:
1. Create or update the Pydantic model in `src/models/`
2. Add endpoint to `src/app.py` (use `fastapi.status` constants for HTTP codes)
3. Add tests to `tests/test_endpoints.py` (minimum: one test per endpoint)
4. Update README.md API Endpoints section

### API Response Format
All endpoints return Pydantic models. FastAPI automatically converts these to JSON responses.

### Adding Dependencies
Edit `pyproject.toml`, add to `dependencies` or `dev` sections, then run `uv sync`.
