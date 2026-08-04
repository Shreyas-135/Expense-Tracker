"""
Personal Expense Tracker API (FastAPI).

Run with:  uvicorn src.main:app --reload
Docs at:   http://127.0.0.1:8000/docs  (Swagger UI, auto-generated bonus)
"""
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query, status

from src.models import Expense, ExpenseCreate
from src.storage import Storage

app = FastAPI(
    title="Personal Expense Tracker API",
    description="A REST API for adding, listing, filtering, totaling, and deleting personal expenses.",
    version="1.0.0",
)

storage = Storage()


@app.get("/health", tags=["meta"], summary="Liveness check")
def health() -> dict:
    return {"status": "ok"}


@app.post(
    "/expenses",
    response_model=Expense,
    status_code=status.HTTP_201_CREATED,
    tags=["expenses"],
    summary="Add an expense",
)
def create_expense(expense: ExpenseCreate) -> Expense:
    return storage.add(expense)


@app.get(
    "/expenses",
    response_model=List[Expense],
    tags=["expenses"],
    summary="List all expenses (optionally filtered)",
)
def list_expenses(
    category: Optional[str] = Query(None, description="Filter by category (case-insensitive)"),
    q: Optional[str] = Query(None, description="Search by title, case-insensitive substring match"),
) -> List[Expense]:
    return storage.list(category=category, q=q)


# NOTE: /expenses/total and /expenses/total/by-category must be declared
# BEFORE /expenses/{expense_id}, otherwise FastAPI would match "total" as
# an expense_id path parameter.

@app.get(
    "/expenses/total",
    tags=["expenses"],
    summary="Overall total, or total for a single category",
)
def get_total(category: Optional[str] = Query(None, description="Optional category filter")) -> dict:
    return {"total": storage.total(category=category), "category": category}


@app.get(
    "/expenses/total/by-category",
    tags=["expenses"],
    summary="Totals grouped by every category",
)
def get_total_by_category() -> Dict[str, float]:
    return storage.total_by_category()


@app.get(
    "/expenses/{expense_id}",
    response_model=Expense,
    tags=["expenses"],
    summary="Get a single expense by id",
)
def get_expense(expense_id: str) -> Expense:
    expense = storage.get(expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.delete(
    "/expenses/{expense_id}",
    tags=["expenses"],
    summary="Delete an expense by id",
)
def delete_expense(expense_id: str) -> dict:
    deleted = storage.delete(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"deleted": expense_id}
