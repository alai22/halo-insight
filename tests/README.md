# Testing Guide

This directory contains comprehensive tests for the Gladly Conversation Analyzer application.

## Test Structure

```
tests/
├── conftest.py              # Shared pytest fixtures
├── fixtures/                # Test data files
│   └── test_conversations.jsonl
├── unit/                    # Unit tests
│   ├── test_claude_service.py
│   ├── test_storage_service.py
│   └── test_conversation_service.py
└── integration/             # Integration tests
    └── test_api_routes.py
```

## Running Tests

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=backend --cov-report=html
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_claude_service.py

# Specific test function
pytest tests/unit/test_claude_service.py::TestClaudeService::test_send_message_success
```

### Run with Markers

```bash
# Run only fast tests (exclude slow/external)
pytest -m "not slow and not external"

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

## Test Fixtures

The `conftest.py` file provides several useful fixtures:

- `app`: Flask application instance
- `client`: Flask test client
- `mock_storage_service`: Mock storage service with sample data
- `mock_claude_service`: Mock Claude API service
- `service_container`: Service container with mocked services
- `sample_conversations`: Sample conversation data

## Writing New Tests

### Unit Test Example

```python
import pytest
from unittest.mock import Mock
from backend.services.claude_service import ClaudeService

class TestClaudeService:
    def test_send_message(self, mock_claude_service):
        response = mock_claude_service.send_message("Hello")
        assert response.content is not None
```

### Integration Test Example

```python
import pytest
from flask import json

class TestAPI:
    def test_endpoint(self, client):
        response = client.get('/api/health')
        assert response.status_code == 200
```

## Test Coverage

The project aims for 80%+ test coverage. Current coverage can be viewed by running:

```bash
pytest --cov=backend --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

## Mocking External Services

Tests use mocks to avoid calling external APIs:

- **Claude API**: Mocked to return predictable responses
- **S3/Azure Storage**: Mocked to return test data
- **File System**: Uses test fixtures in `tests/fixtures/`

## Continuous Integration

Tests should be run automatically in CI/CD pipelines. The `pytest.ini` configuration ensures consistent test execution across environments.

## Best Practices

1. **Isolation**: Each test should be independent
2. **Mocking**: Mock external dependencies
3. **Fixtures**: Use pytest fixtures for common setup
4. **Naming**: Use descriptive test names
5. **Assertions**: Use specific assertions with helpful messages

## Troubleshooting

### Tests Fail with Import Errors

Make sure you're running tests from the project root:
```bash
cd /path/to/halo-insight
pytest
```

### Environment Variables Not Set

Tests use `conftest.py` to set test environment variables. If you need custom values, override them in your test:

```python
@pytest.fixture
def custom_env(monkeypatch):
    monkeypatch.setenv('CUSTOM_VAR', 'value')
```

### Service Container Not Available

Integration tests patch the service container. Make sure you're using the `mock_storage_service` and `mock_claude_service` fixtures.




