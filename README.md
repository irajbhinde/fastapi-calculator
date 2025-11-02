
# FastAPI Calculator (with Tests, Logging, and CI)

A simple FastAPI-based calculator demonstrating unit, integration, and end-to-end testing with Playwright, plus structured logging and a GitHub Actions CI workflow.

## Features
- REST API: `/add`, `/subtract`, `/multiply`, `/divide`, `/health`
- HTML UI served at `/` with fetch calls to the API
- Logging to console and `logs/app.log` (rotating)
- Tests:
  - Unit tests for pure functions in `app/operations.py`
  - Integration tests for FastAPI endpoints in `app/main.py`
  - End-to-end tests (Playwright) that click through the browser UI
- GitHub Actions CI running all tests on push/PR

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/ in your browser.

## Run tests (local)
```bash
# Unit + integration
pytest -q

# End-to-end (requires Node 18+)
npm install -D @playwright/test
npx playwright install
# in one terminal, run the server:
uvicorn app.main:app --port 8000
# in another terminal:
npx playwright test
```

## CI
The workflow at `.github/workflows/ci.yml`:
1. Installs Python deps and runs `pytest`
2. Installs Playwright + browsers
3. Starts the FastAPI server
4. Runs E2E tests
5. Uploads the Playwright HTML report as an artifact

## Screenshots required for submission
- **GitHub Actions successful run**: from your repo's *Actions* tab after a green run.
- **App running in the browser**: a screenshot of the index page with a sample calculation.

## Notes
- Division by zero returns HTTP 400 with a helpful message.
- Numeric inputs are coerced to float; invalid strings raise a 400 from the API.
