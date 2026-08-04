
import json
import threading
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from src.models import Expense, ExpenseCreate


class Storage:
    def __init__(self, filepath: Optional[Path] = None):
        default_path = Path(__file__).resolve().parent.parent / "data" / "expenses.json"
        self.filepath = Path(filepath) if filepath else default_path
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._expenses: Dict[str, Expense] = {}
        self._load()

    def _load(self) -> None:
        self._expenses = {}
        if self.filepath.exists():
            try:
                raw = json.loads(self.filepath.read_text())
                for item in raw:
                    expense = Expense(**item)
                    self._expenses[expense.id] = expense
            except (json.JSONDecodeError, ValueError, TypeError):
                # Corrupt or empty file: start fresh rather than crash the server.
                self._expenses = {}

    def _save(self) -> None:
        data = [json.loads(e.model_dump_json()) for e in self._expenses.values()]
        self.filepath.write_text(json.dumps(data, indent=2))

    def add(self, expense_in: ExpenseCreate) -> Expense:
        with self._lock:
            expense = Expense(id=str(uuid.uuid4()), **expense_in.model_dump())
            self._expenses[expense.id] = expense
            self._save()
            return expense

    def list(self, category: Optional[str] = None, q: Optional[str] = None) -> List[Expense]:
        results = list(self._expenses.values())
        if category:
            results = [e for e in results if e.category.lower() == category.lower()]
        if q:
            results = [e for e in results if q.lower() in e.title.lower()]
        results.sort(key=lambda e: e.date)
        return results

    def get(self, expense_id: str) -> Optional[Expense]:
        return self._expenses.get(expense_id)

    def delete(self, expense_id: str) -> bool:
        with self._lock:
            if expense_id in self._expenses:
                del self._expenses[expense_id]
                self._save()
                return True
            return False

    def total(self, category: Optional[str] = None) -> float:
        exps = self.list(category=category)
        return round(sum(e.amount for e in exps), 2)

    def total_by_category(self) -> Dict[str, float]:
        totals: Dict[str, float] = {}
        for e in self._expenses.values():
            totals[e.category] = round(totals.get(e.category, 0.0) + e.amount, 2)
        return totals

    def clear(self) -> None:
        """Used by tests to reset state between runs."""
        with self._lock:
            self._expenses = {}
