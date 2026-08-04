"""
Test suite for the Expense Tracker API.

Run with:  pytest tests/ -v
"""


def create_expense(client, title="Coffee", amount=4.5, category="Food", date="2026-07-01"):
    return client.post(
        "/expenses",
        json={"title": title, "amount": amount, "category": category, "date": date},
    )


# ---------- health ----------

def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


# ---------- create ----------

def test_create_expense_success(client):
    resp = create_expense(client)
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data and data["id"]
    assert data["title"] == "Coffee"
    assert data["amount"] == 4.5
    assert data["category"] == "Food"
    assert data["date"] == "2026-07-01"


def test_create_expense_missing_fields(client):
    resp = client.post("/expenses", json={"title": "Incomplete"})
    assert resp.status_code == 422


def test_create_expense_negative_amount(client):
    resp = create_expense(client, amount=-10)
    assert resp.status_code == 422


def test_create_expense_zero_amount(client):
    resp = create_expense(client, amount=0)
    assert resp.status_code == 422


def test_create_expense_blank_title(client):
    resp = create_expense(client, title="")
    assert resp.status_code == 422


def test_create_expense_bad_date_format(client):
    resp = create_expense(client, date="07/01/2026")
    assert resp.status_code == 422


def test_create_expense_malformed_json(client):
    resp = client.post(
        "/expenses",
        content=b"{not valid json",
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 422  # FastAPI/Starlette report JSON parse errors as 422


# ---------- list / filter / search ----------

def test_list_expenses_empty(client):
    resp = client.get("/expenses")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_expenses_returns_created(client):
    create_expense(client, title="Lunch", amount=12, category="Food", date="2026-07-02")
    create_expense(client, title="Bus ticket", amount=3, category="Transport", date="2026-07-03")
    resp = client.get("/expenses")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    assert data[0]["title"] == "Lunch"  # sorted by date ascending


def test_filter_by_category_case_insensitive(client):
    create_expense(client, title="Lunch", amount=12, category="Food", date="2026-07-02")
    create_expense(client, title="Bus ticket", amount=3, category="Transport", date="2026-07-03")
    create_expense(client, title="Dinner", amount=20, category="food", date="2026-07-04")

    resp = client.get("/expenses", params={"category": "Food"})
    assert resp.status_code == 200
    data = resp.json()
    assert {e["title"] for e in data} == {"Lunch", "Dinner"}


def test_filter_by_category_no_match(client):
    create_expense(client, category="Food")
    resp = client.get("/expenses", params={"category": "Nonexistent"})
    assert resp.status_code == 200
    assert resp.json() == []


def test_search_by_title(client):
    create_expense(client, title="Grocery shopping", amount=50, category="Food", date="2026-07-05")
    create_expense(client, title="Movie ticket", amount=15, category="Entertainment", date="2026-07-06")
    resp = client.get("/expenses", params={"q": "grocery"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "Grocery shopping"


# ---------- get single ----------

def test_get_single_expense(client):
    created = create_expense(client).json()
    resp = client.get(f"/expenses/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_get_expense_not_found(client):
    resp = client.get("/expenses/does-not-exist")
    assert resp.status_code == 404


# ---------- totals ----------

def test_total_overall(client):
    create_expense(client, amount=10, category="Food")
    create_expense(client, amount=25.5, category="Transport")
    resp = client.get("/expenses/total")
    assert resp.status_code == 200
    assert resp.json()["total"] == 35.5


def test_total_filtered_by_category(client):
    create_expense(client, amount=10, category="Food")
    create_expense(client, amount=5, category="Food")
    create_expense(client, amount=25.5, category="Transport")
    resp = client.get("/expenses/total", params={"category": "Food"})
    assert resp.status_code == 200
    assert resp.json()["total"] == 15


def test_total_by_category_breakdown(client):
    create_expense(client, amount=10, category="Food")
    create_expense(client, amount=5, category="Food")
    create_expense(client, amount=25.5, category="Transport")
    resp = client.get("/expenses/total/by-category")
    assert resp.status_code == 200
    data = resp.json()
    assert data["Food"] == 15
    assert data["Transport"] == 25.5


def test_total_route_not_shadowed_by_id_route(client):
    """Regression guard: /expenses/total must not be swallowed by the
    /expenses/{expense_id} route."""
    resp = client.get("/expenses/total")
    assert resp.status_code == 200
    assert "total" in resp.json()


# ---------- delete ----------

def test_delete_expense(client):
    created = create_expense(client).json()
    resp = client.delete(f"/expenses/{created['id']}")
    assert resp.status_code == 200

    resp = client.get(f"/expenses/{created['id']}")
    assert resp.status_code == 404


def test_delete_expense_not_found(client):
    resp = client.delete("/expenses/does-not-exist")
    assert resp.status_code == 404


# ---------- persistence ----------

def test_persistence_to_disk(client):
    from src.main import storage
    import json

    created = create_expense(client, title="Persisted item").json()
    on_disk = json.loads(storage.filepath.read_text())
    assert any(e["id"] == created["id"] for e in on_disk)
