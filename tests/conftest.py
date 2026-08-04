import pytest
from fastapi.testclient import TestClient

from src.main import app, storage


@pytest.fixture(autouse=True)
def reset_storage(tmp_path):
    """Point the shared storage instance at a fresh temp file for every test,
    so tests never read/write the real data/expenses.json and never leak
    state into each other."""
    storage.filepath = tmp_path / "expenses.json"
    storage.clear()
    yield
    storage.clear()


@pytest.fixture
def client():
    return TestClient(app)
