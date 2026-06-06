# F1 Data Visualization API

A FastAPI backend for Formula 1 data visualization powered by [FastF1](https://docs.fastf1.dev/).

## Features

- RESTful API endpoints for F1 data
- Pydantic validation for all requests and responses
- FastF1 integration for seamless data access
- Comprehensive test coverage with pytest

## Getting Started

### Prerequisites

- Python 3.13+
- uv (Python package manager)

### Installation

```bash
uv sync
```

This installs all dependencies and creates a virtual environment.

## Running the API

```bash
uv run uvicorn src.app:app --reload
```

The API will be available at `http://localhost:8000`. Interactive API documentation is at `http://localhost:8000/docs`.

## Testing

Run all tests:

```bash
uv run pytest
```

Run a specific test file:

```bash
uv run pytest tests/test_endpoints.py
```

Run a specific test:

```bash
uv run pytest tests/test_endpoints.py::test_health_check
```

## API Endpoints

- `GET /health` — Health check endpoint
- `GET /years/{year}/available` — Check if a given year has F1 data available

## Project Structure

```
src/
  app.py           # FastAPI application and endpoints
  models/          # Pydantic models for request/response validation
tests/
  test_endpoints.py  # Endpoint tests
```
