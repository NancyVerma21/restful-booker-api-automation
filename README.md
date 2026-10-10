# RESTful Booker API Automation

This repository contains automated tests for the RESTful Booker practice API using Python, Pytest, Requests, JSON Schema, Allure, and GitHub Actions.

## Features

- API health and authentication checks
- Booking list, retrieval, creation, full update, and deletion tests
- Negative test for a nonexistent booking
- JSON Schema validation of booking creation responses
- Reusable Pytest fixtures and request timeouts
- Test-created bookings are cleaned up after use
- Allure-compatible test results
- GitHub Actions CI workflow

## Tech stack

- Python 3.11
- Pytest
- Requests
- jsonschema
- allure-pytest
- python-dotenv
- GitHub Actions

## Setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` if you want to customize the API configuration. The public practice API's demo credentials are used by default.

## Run tests

Run all tests:

```powershell
python -m pytest
```

Run smoke tests:

```powershell
python -m pytest -m smoke
```

Run regression tests:

```powershell
python -m pytest -m regression
```

Create Allure result files:

```powershell
python -m pytest --alluredir=allure-results
```

Allure result files are generated locally in `allure-results/`. They are not automatically a public report URL. To view an HTML report, install the Allure command-line tool and run:

```powershell
allure serve allure-results
```

## Project structure

```text
restful-booker-api-automation/
├── .github/
│   └── workflows/
│       └── api-tests.yml
├── schemas/
│   ├── booking.json
│   └── booking_response_schema.json
├── tests/
│   ├── test_health_auth.py
│   ├── test_bookings.py
│   └── test_booking_crud.py
├── .env.example
├── .gitignore
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## CI

GitHub Actions runs the API tests on pushes and pull requests and uploads the Allure result files as a workflow artifact.

## Notes

This project targets a shared public practice API. Its availability and data may change, so transient external service failures can occur. Tests create their own bookings and only delete bookings created during their own test runs.

