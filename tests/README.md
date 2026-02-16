# Tests

Unit, Integration & End-to-End Tests für SBS GTM Automation.

## Test-Struktur:

```
tests/
├── unit/                    # Unit Tests
│   ├── test_lead_generation.py
│   ├── test_content_automation.py
│   └── test_analytics.py
├── integration/            # Integration Tests
│   ├── test_linkedin_api.py
│   └── test_bigquery_sync.py
├── e2e/                    # End-to-End Tests
│   └── test_full_workflow.py
└── conftest.py             # Pytest Configuration
```

## Test-Ausführung:

```bash
# Alle Tests
pytest

# Mit Coverage
pytest --cov=src --cov-report=html

# Nur Unit Tests
pytest tests/unit/

# Mit Verbose Output
pytest -v
```

## Enterprise Standards:
- 90%+ Code Coverage Target
- Type Checking via mypy
- Mocking für externe APIs
- DSGVO-konforme Test-Daten
