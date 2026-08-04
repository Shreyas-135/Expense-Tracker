# Personal Expense Tracker API

A REST API for managing personal expenses: add, list, filter by category,
delete, and total up spending (overall and per category), plus search by
title (bonus feature).

## Features

- Add, view and delete expenses
- Filter expenses by category
- Search expenses by title (bonus)
- Calculate overall expenses
- Calculate category-wise expense totals
- JSON-based persistent storage
- Automatic API documentation using Swagger
- Unit tests using pytest

  
## Stack

- **Python 3.10+** with **FastAPI** + **Pydantic v2** for the API and
  request validation.
- **Uvicorn** as the ASGI server.
- **Pytest** + **httpx**-backed `TestClient` for tests.
- Storage: an in-memory dict, flushed to a local JSON file
  (`data/expenses.json`) after every write, so data survives a server
  restart. No database.

## Design Decisions

- Built using FastAPI for automatic request validation and Swagger documentation.
- Used UUIDs as expense identifiers to ensure uniqueness.
- Stored data in a local JSON file instead of a database, as allowed by the assignment.
- Separated API routes, models, and storage logic for better maintainability.
  
## Install

```bash
git clone https://github.com/Shreyas-135/Expense-Tracker.git
cd Expense-Tracker
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run the server

```bash
uvicorn src.main:app --reload
```

Server runs at `http://127.0.0.1:8000`.

Interactive API docs (Swagger UI) are auto-generated at
`http://127.0.0.1:8000/docs`, and the raw OpenAPI schema at
`http://127.0.0.1:8000/openapi.json`.

## Run the tests

```bash
pytest tests/ -v
```

Each test gets an isolated storage instance pointed at a pytest `tmp_path`
(see `tests/conftest.py`), so tests never touch your real
`data/expenses.json` and never leak state between each other.

## API Reference

| Method | Path                             | Description                     |
|--------|-----------------------------------|----------------------------------|
| POST   | `/expenses`                       | Add an expense                   |
| GET    | `/expenses`                       | View all expenses                |
| GET    | `/expenses?category=Food`         | Filter expenses by category      |
| GET    | `/expenses?q=coffee`              | Search expenses by title (bonus) |
| GET    | `/expenses/{id}`                  | Get a single expense             |
| DELETE | `/expenses/{id}`                  | Delete an expense                |
| GET    | `/expenses/total`                 | Overall total                    |
| GET    | `/expenses/total?category=Food`   | Total for one category           |
| GET    | `/expenses/total/by-category`     | Totals grouped by every category |
| GET    | `/health`                         | Liveness check                   |

### Example requests

```bash
# Add an expense
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"title":"Groceries","amount":45.20,"category":"Food","date":"2026-07-15"}'

# View all expenses
curl http://127.0.0.1:8000/expenses

# Filter by category
curl "http://127.0.0.1:8000/expenses?category=Food"

# Search by title
curl "http://127.0.0.1:8000/expenses?q=grocer"

# Overall total
curl http://127.0.0.1:8000/expenses/total

# Total for one category
curl "http://127.0.0.1:8000/expenses/total?category=Food"

# Totals broken down by category
curl http://127.0.0.1:8000/expenses/total/by-category

# Delete an expense
curl -X DELETE http://127.0.0.1:8000/expenses/<id>
```

### Expense object

```json
{
  "id": "84a62a0b-6895-47f1-8efc-786fbdbe1b5e",
  "title": "Groceries",
  "amount": 45.2,
  "category": "Food",
  "date": "2026-07-15"
}
```

`id` is server-generated (UUID4) — don't send it on create. `date` must be
`YYYY-MM-DD`. `amount` must be a positive number. Validation is handled by
Pydantic; invalid input returns `422` with a field-level error body.

## Project structure

```
expense-tracker/
  README.md
  AI_NOTES.md
  requirements.txt
  src/
    __init__.py
    main.py        # FastAPI app + routes
    models.py       # Pydantic request/response models
    storage.py       # in-memory store + JSON persistence
  tests/
    __init__.py
    conftest.py      # pytest fixtures (isolated storage per test)
    test_api.py
  data/
    .gitkeep         # expenses.json is created here at runtime
```

## Known limitations

- Single-process, single JSON file — not meant for concurrent multi-instance
  deployment (no database, as specced).
- No auth — this is a personal single-user tool, not a multi-tenant service.
- Amount is stored as a `float` rounded to 2 decimals; for real currency
  handling you'd want `Decimal` end-to-end, which felt like overkill for the
  scope of this exercise.

## AI Usage

AI tools (ChatGPT and Claude) were used during development to accelerate implementation and generate boilerplate code. All generated code was reviewed, tested, and modified where necessary before submission. Additional details are available in `AI_NOTES.md`.
