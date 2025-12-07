
# FastAPI Calculator

A small full-stack demo application built with **FastAPI**, **PostgreSQL**, and **Playwright** that supports:

- User registration and login (JWT-based backend, HTML + JS frontend).
- A calculator for basic operations (add, subtract, multiply, divide).
- Full **BREAD** (Browse, Read, Edit, Add, Delete) UI for calculation history.
- End‑to‑end tests using **Playwright**.
- Continuous Integration with **GitHub Actions**.
- Containerized deployment with **Docker**.

---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy 2.x, Pydantic v2
- **Database:** PostgreSQL (via `psycopg2`)
- **Auth:** JWT + password hashing
- **Frontend:** HTML templates + vanilla JS (`auth.js`, `calculations.js`)
- **Testing:** Pytest, Playwright
- **CI/CD:** GitHub Actions
- **Container:** Docker

---

## Getting Started (Local Development)

### Prerequisites

- Python **3.11+**
- Node.js **18+** and `npm`
- PostgreSQL running locally (or a remote instance)
- Optional: `pytest`, `playwright` installed globally

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>.git
cd fastapi-calculator

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
# or install your dependencies as configured in the project
```

### 2. Configure the database

The app uses a `DATABASE_URL` environment variable. For local development, you can use:

```bash
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_db"
# Windows PowerShell:
# $env:DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_db"
```

On application import, `app.database.init_db()` creates the required tables:

- `users_secure`
- `calculations`

No manual migration step is required for this demo.

### 3. Run the application

From the project root:

```bash
uvicorn app.main:app --reload
```

By default the app runs at `http://127.0.0.1:8000`.

Key routes:

- `GET /` – Calculator page
- `GET /register` – Registration form
- `GET /login` – Login form
- `GET /calculations-ui` – Calculations BREAD UI
- `GET /docs` – Interactive Swagger/OpenAPI docs

---

## Running Tests Locally

### 1. Backend tests (pytest)

With your virtual environment active:

```bash
pytest
```

This runs unit and integration tests, including calculator behavior.

### 2. Playwright E2E tests

First, make sure the app is running locally (for example:

```bash
uvicorn app.main:app --reload
```

in one terminal window).

Then, in another terminal:

```bash
npx playwright install  # first time only
npx playwright test
```

The E2E suite currently includes:

- `auth.smoke.spec.ts`
  - Register + login (happy path)
  - Login with wrong password (negative)
- `calculations.smoke.spec.ts`
  - Add → edit → delete calculation (BREAD smoke)
  - Divide‑by‑zero error (negative)
- `test_calculator.spec.ts`
  - Core calculator operations

---

## Docker

### Build the image

From the project root:

```bash
docker build -t <your-dockerhub-username>/fastapi-calculator:latest .
```

### Run the container

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql+psycopg2://postgres:postgres@host.docker.internal:5432/fastapi_db" \
  <your-dockerhub-username>/fastapi-calculator:latest
```

Adjust the `DATABASE_URL` to match your environment (for example, a Docker network or cloud-hosted PostgreSQL instance).

### Docker Hub

Push the image:

```bash
docker push <your-dockerhub-username>/fastapi-calculator:latest
```

Docker Hub repository (replace with your actual namespace):

- https://hub.docker.com/r/<your-dockerhub-username>/fastapi-calculator

---

## GitHub Actions (CI/CD)

The repository includes a GitHub Actions workflow that:

1. Installs Python and Node dependencies.
2. Starts PostgreSQL and configures `DATABASE_URL`.
3. Runs backend tests and Playwright E2E tests.
4. Builds the Docker image.
5. Optionally pushes the image to Docker Hub on successful runs for main branch or tagged releases.

For your report, capture a screenshot of a successful workflow run from the **Actions** tab showing all steps passing.

---

## Frontend BREAD Flow

Once logged in:

1. Navigate to **“Calculations BREAD”** (`/calculations-ui`).
2. Use the **Add Calculation** form to create a new calculation entry.
3. Confirm the entry appears in **All Calculations** and use:
   - **Edit** to populate the edit form and save changes.
   - **Delete** to remove the calculation.
4. Use the details section to inspect a single calculation (as supported by `calculations.js`).

These flows are covered by the Playwright smoke tests to ensure the UI and API stay wired correctly.

---

## Screenshots 

Added under M14 Folder of Screenshots

## Reflection 

This project was mainly about getting the whole stack to work together - database models, FastAPI routes, HTML templates, and Playwright tests. The big breakthrough came when we cleaned up the SQLAlchemy setup, making sure there was just one Base and a reliable init_db() call that always created users_secure and calculations before any request or test. Once the database was predictable, the rest was about making sure the frontend and tests matched up: using real IDs instead of guessed labels, showing realistic success and error messages, and writing smoke tests that check behavior without being too fragile.

For testing, the main takeaway was to keep E2E tests simple and flexible at first. Early versions checked for exact strings and specific DOM states that the real UI didn’t always provide, which caused a lot of unnecessary failures. In the end, we focused on the main flows - registering, logging in, BREAD operations, and important negative cases like invalid credentials and divide-by-zero, while letting details like message text or how delete updates the table change as needed. This balance between reliability and flexibility keeps the test suite manageable for a small app like this.
