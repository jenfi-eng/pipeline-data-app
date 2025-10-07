# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jenfi Pipeline Data App is a Python library designed for data teams to access Jenfi's data sources within Jupyter notebooks. It provides database query functionality with built-in caching (local + S3), model management, and result handling for data pipeline workflows.

**Key characteristics:**
- Python 3.13 monorepo using Poetry for dependency management
- Primarily used as an imported module in Jupyter notebooks
- Environment-aware configuration (production/staging/development/test)
- Two-tier caching: local filesystem + S3 for query results
- Supports both "Nellie" and "Core" database schemas (auto-detected via `CORE_APP_NAME` env var)

## Development Commands

### Environment Setup
```bash
poetry install              # Install dependencies
poetry shell               # Activate virtual environment
```

### Testing
```bash
pytest                     # Run all tests
pytest tests/pipeline_data_app_test.py  # Run specific test file
pytest -k test_name       # Run specific test by name
```

### Linting & Formatting
```bash
ruff check .              # Run linter
ruff check --fix .        # Auto-fix linting issues
ruff format .             # Format code
pre-commit run --all-files  # Run all pre-commit hooks
```

### Documentation
```bash
pdoc --html --force --output-dir ./docs jenfi_pipeline_data_app
```
Documentation is published at https://jenfi-eng.github.io/pipeline-data-app

## Architecture

### Application Singleton Pattern
The main entry point is `PipelineDataApp`, a singleton instance of `Application` class (jenfi_pipeline_data_app/__init__.py:6-8). It boots on import, initializing database connections and S3 config.

### Core Components

**Query System (app_funcs/_query.py)**
- `df_query()` / `query_df()`: Returns pandas DataFrame
- `query_one()`: Returns single row as dict
- `query_all()`: Returns all rows as array
- All queries route through `DbCache` for caching

**Caching Layer (db_cache/)**
- `DbCache`: Orchestrates caching via `Cacher` class
- `Cacher`: Handles two-tier cache (local + S3)
- Cache key = hash(normalized_query + logical_step_name + state_machine_run_id)
- Query normalization via `sqlparse` (uppercase keywords, strip comments, reindent)
- Pickle serialization for cache storage
- Can be disabled via `disable_cache` parameter

**Result Handling (app_funcs/_result.py)**
- `write_result(dict)`: Writes result to temp file with STATUS_SUCCESS
- `load_result()`: Loads result from temp file
- `write_result_to_db()`: Persists results to pipeline_state_machine_runs table
- Custom `NpEncoder` handles numpy/Decimal/datetime serialization

**S3 Model Management (app_funcs/_models_s3.py)**
- `load_model_from_s3()`: Load pickled models from S3
- `push_model_to_s3()`: Push models to S3
- `load_model_from_s3_to_file()`: Load to local file

**Database Models (db_models.py)**
- `state_machine_run_model()`: Factory function returns appropriate model
- Supports two schemas: Nellie (`pipeline_statemachinerun`) and Core (`pipeline_state_machine_runs`)
- Detection via `CORE_APP_NAME` environment variable

**Configuration (config/db.py)**
- Environment-based configs: ProductionConfig, StagingConfig, DevelopmentConfig, TestConfig
- Uses `PYTHON_ENV` environment variable for selection
- PostgreSQL connection via SQLAlchemy with psycopg driver

### Required Notebook Parameters

Jupyter notebooks using this library must define in a "parameters" tagged cell:
```python
logical_step_name = 'sg_first_payment_default'  # Unique identifier for step+flow
state_machine_run_id = 5                         # Ties caching to specific run
```

Optional:
```python
disable_cache = True  # Default: False. Bypasses cache for fresh data
```

### Environment Variables

Required in `.env` file at `PipelineDataApp.ROOT_DIR`:
- `PYTHON_ENV`: production/staging/development/test
- `PG_USERNAME`, `PG_PASSWORD`, `PG_HOST`, `PG_PORT`, `DB_NAME`
- S3-related vars (bucket names, credentials)
- `CORE_APP_NAME`: Optional, determines Nellie vs Core schema

## Testing

- Test suite uses `pytest` with `pytest-env` plugin
- `PYTHON_ENV=test` set via pytest.ini_options
- Tests use `_jupyter_faker.py` to simulate Jupyter environment
- Notebooks in `tests/notebooks/` for integration testing
- Papermill available for notebook execution testing
