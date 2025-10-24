# fastapi-opensearch-integration-test
Integration Test Example using FastAPI and OpenSearch

## Prerequisites

- Docker
- docker-compose
- python 3.12
- uv

## Running OpenSearch and FastAPI Locally

1. Run `docker-compose up -d` to run OpenSearch locally
2. Run `source .venv/bin/activate` to activate the virtual environment
3. Run `uv sync --extra test` to install all deps
4. Run `uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000` to run the app locally
5. Run `uv run pytest -q` to run integration tests
