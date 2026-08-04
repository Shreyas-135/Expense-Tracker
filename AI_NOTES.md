# AI Usage Notes

## Summary

I used ChatGPT and Claude as development assistants while building this Smart Expense Tracker API. AI helped me generate the initial FastAPI project structure, some API endpoints, and testing boilerplate. Rather than directly using the generated code, I reviewed every file, understood the implementation, modified parts of the code where necessary, and validated the final application by testing it locally.

The final submission reflects both AI-assisted development and my own engineering decisions.

---

# AI-Generated Components

AI assisted me with the following:

- Initial FastAPI project setup
- Pydantic model definitions
- CRUD API endpoint templates
- JSON persistence implementation
- Initial pytest test cases
- README documentation
- Basic API documentation

---

# What I Reviewed and Changed

After generating the initial implementation, I reviewed each module and made several improvements.

### API Design

- Verified all REST endpoints behaved as expected.
- Added proper HTTP status codes for success and failure cases.
- Ensured consistent JSON response formats.

### Route Design

I ensured that:

- `/expenses/total`
- `/expenses/total/by-category`

are declared before

- `/expenses/{expense_id}`

to prevent FastAPI from interpreting `total` as a path parameter.

### Storage Layer

I reviewed the JSON persistence implementation and verified that:

- New expenses are immediately written to disk.
- Data is automatically loaded when the server restarts.
- Invalid JSON files do not crash the application.
- Thread locking protects write operations.

### Validation

I reviewed the Pydantic models to ensure:

- Amount must always be positive.
- Title cannot be empty.
- Category is mandatory.
- Dates follow the ISO (`YYYY-MM-DD`) format.

### Search & Filtering

I verified that:

- Category filtering is case-insensitive.
- Title search works using case-insensitive substring matching.
- Expense totals are calculated correctly for both all expenses and individual categories.

---

# Testing and Validation

Before submitting the assignment, I validated the project by:

- Installing all project dependencies.
- Running the FastAPI server locally.
- Testing every endpoint using Swagger UI.
- Executing the pytest test suite.
- Testing invalid request payloads.
- Verifying deletion of expenses.
- Verifying category filtering.
- Verifying title search.
- Confirming JSON persistence across server restarts.
- Checking overall and category-wise expense totals.

---

# AI Suggestions I Decided Not to Use

## 1. Database Integration

AI suggested using SQLite for persistent storage.

Since the assignment explicitly allowed storing data in memory or a JSON file, I intentionally kept the project lightweight by using JSON persistence instead of introducing an unnecessary database.

---

## 2. Sequential Integer IDs

AI suggested auto-incrementing integer IDs.

I chose UUIDs instead because they:

- Guarantee uniqueness
- Avoid collisions
- Do not reveal the number of stored expenses

---

## 3. Decimal for Monetary Values

AI recommended using Python's `Decimal` type for better financial precision.

For this assignment, I chose `float` because the application stores data in a JSON file and does not perform complex financial calculations. This keeps serialization simpler while still meeting the assignment requirements.

---

## 4. Additional Features

AI suggested implementing authentication, pagination, and database migrations.

Since these features were outside the assignment scope, I decided not to include them and instead focused on delivering a clean, fully functional REST API.

---

# Engineering Decisions

Some design decisions I made during development include:

- Using FastAPI for automatic validation and built-in Swagger documentation.
- Separating API routes, models, and storage logic into different modules.
- Using UUIDs for expense identification.
- Persisting expenses in a local JSON file instead of using a database.
- Implementing case-insensitive filtering and searching.
- Sorting expenses by date before returning results.
- Using thread locking to avoid concurrent write issues while saving data.

---

# What I Learned

AI significantly accelerated the initial development process by generating boilerplate code and suggesting implementation ideas. However, I treated the generated output as a starting point rather than the final solution.

I reviewed every module, understood how the code worked, validated the API behaviour through testing, made implementation improvements where necessary, and ensured the final project met all assignment requirements.

This project helped me improve my understanding of FastAPI, REST API design, request validation using Pydantic, JSON-based persistence, API testing with pytest, and how to effectively use AI as a development assistant while maintaining ownership of the final implementation.
