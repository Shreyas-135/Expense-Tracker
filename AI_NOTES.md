# AI Usage Notes

## Summary

I used Claude (Anthropic) to generate the full implementation of this
project — `src/models.py`, `src/storage.py`, `src/main.py`, and
`tests/test_api.py` — from a description of the assignment requirements.
This document is an honest account of that process. **If you're using this
as your own submission, you should personalize this file with your own
review notes before submitting** — the assignment specifically grades how
you validated the AI's output, and the paragraph below about the untested
state is important context you'll want to resolve first.

## Important: this version was not run before delivery

I generated the FastAPI implementation in a sandboxed environment with no
network access, so I could not `pip install fastapi` and actually execute
`pytest` or start the server here. I confirmed this by trying `pip install`,
`pip download`, and `apt-get install python3-fastapi`, all of which failed
on network access — I'm noting that explicitly rather than implying this
was verified when it wasn't.

What I *did* do to reduce risk despite that:
- Ran a static syntax check (`ast.parse`) on every file to catch typos and
  syntax errors.
- Kept the routing, validation rules, and storage logic (dict-based store,
  JSON persistence, category/search filtering, total aggregation) identical
  to an earlier stdlib-only version of this same API that I *did* build,
  run, and test end-to-end (20 passing tests, verified live with `curl`,
  verified persistence to disk across restarts). Porting proven logic into
  FastAPI's structure is lower-risk than writing it fresh, but it is not a
  substitute for actually running it.
- Deliberately ordered the `/expenses/total` and `/expenses/total/by-category`
  routes before `/expenses/{expense_id}` in `main.py`, because FastAPI
  matches routes in declaration order and a `{expense_id}` path parameter
  would otherwise swallow the literal `total` path — this is a known
  FastAPI footgun I checked for specifically, and there's a regression
  test for it (`test_total_route_not_shadowed_by_id_route`).

**You must run `pip install -r requirements.txt` and `pytest tests/ -v`
yourself before submitting**, and fix anything that doesn't pass. Likely
candidates for something to double check, in rough order of risk:
- The malformed-JSON test (`test_create_expense_malformed_json`) asserts a
  `422` status. Depending on the exact FastAPI/Starlette version installed,
  this could come back as a different code — verify and adjust if needed.
- Pydantic v2 date parsing accepts ISO format (`YYYY-MM-DD`) by default,
  which is what the tests assume; if you're pinned to Pydantic v1 for some
  reason, field validation syntax (`Field(..., gt=0)` etc.) would need
  adjusting.

## What was AI-generated vs. hand-written

**AI-generated (100% of the code in this version):**
- `src/models.py` — Pydantic `ExpenseCreate`/`Expense` models.
- `src/storage.py` — in-memory store, JSON persistence, filtering, totals.
- `src/main.py` — FastAPI routes.
- `tests/conftest.py`, `tests/test_api.py` — pytest fixtures and test suite.
- `README.md` — docs and example commands.

**Design decisions I made explicitly (not just accepted as AI defaults):**
- `id` is server-generated (UUID4), not client-supplied — the brief lists
  "id" as a field without saying who assigns it; UUID4 avoids collision and
  "count of expenses" leakage that sequential ints would have.
- Category filter and title search are case-insensitive.
- `/expenses/total` and `/expenses/total/by-category` are separate
  endpoints from `/expenses/{id}` and declared first in the file, for the
  routing-collision reason above.
- Picked FastAPI specifically (over the stdlib-only approach I originally
  had verified) because the assignment listed it as one of the expected
  stacks, and because it gets you Swagger docs at `/docs` essentially for
  free — but see the caveat above about not being able to run it here.

## AI suggestions I decided not to use

- **`Decimal` instead of `float` for `amount`.** More correct for money,
  but adds complexity (JSON doesn't have a native Decimal type, so you'd
  need custom serialization) that isn't justified for a personal expense
  tracker at this scope. Documented as a known limitation instead.
- **Auto-incrementing integer IDs.** Simpler-looking in examples, but
  collide across restarts and leak the total count of expenses created.
  UUID4 avoids both at negligible cost.
- **A response_model / explicit return type for `/expenses/total/by-category`.**
  The AI's first draft typed it as `Dict[str, float]` with a `response_model`
  set, which FastAPI would then use to validate/serialize the output. I
  simplified this to a bare dict return with just a type hint (no
  `response_model`) since the shape is dynamic (one key per category) and
  doesn't benefit from a fixed schema the way `Expense` does.

## If you're adapting this project as your own submission

1. Run `pip install -r requirements.txt` and `pytest tests/ -v` yourself —
   this has not been executed in the environment that generated it.
2. Read `src/main.py` and `src/storage.py` end to end (under 150 lines
   combined) and rewrite this document to describe *your* review, in your
   own words.
3. Note here anything you had to fix, and why.
