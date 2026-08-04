"""Pydantic models for the Expense Tracker API."""
from datetime import date

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    """Payload for creating an expense. `id` is assigned by the server."""

    title: str = Field(..., min_length=1, description="Short description, e.g. 'Groceries'")
    amount: float = Field(..., gt=0, description="Must be a positive number")
    category: str = Field(..., min_length=1, description="e.g. 'Food', 'Transport'")
    date: date = Field(..., description="Date the expense occurred, YYYY-MM-DD")


class Expense(ExpenseCreate):
    """A stored expense, including its server-generated id."""

    id: str
