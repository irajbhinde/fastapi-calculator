# 🧮 FastAPI Calculator + 🐘 PostgreSQL Integration (Docker Compose) + 🔐 Secure User Model

This repository demonstrates:
- A **FastAPI-based calculator** application.
- Integration with **PostgreSQL and pgAdmin** using **Docker Compose**.
- A **secure SQLAlchemy User model** with hashed passwords and Pydantic schemas.
- Logging, automated testing, and CI/CD with **GitHub Actions** and Docker Hub.

![CI](https://github.com/irajbhinde/fastapi-calculator/actions/workflows/ci.yml/badge.svg)

---

## 🚀 Features

✅ **Calculator API**
- `/add`, `/subtract`, `/multiply`, `/divide`, `/health`  
  (POST for arithmetic operations, GET for `/health`)

✅ **Secure User Model**
- SQLAlchemy `User` model with:
  - Unique `username` and `email`
  - `password_hash` (hashed using Passlib)
  - `created_at` timestamp
- Pydantic schemas:
  - `UserCreate` – validates input (`username`, `email`, `password`)
  - `UserRead` – returns safe user data (no password hash)
- Endpoints:
  - `POST /users` – create a user with a hashed password
  - `GET /users` – list all users

✅ **Docker Integration**
- Fully containerized setup with FastAPI, PostgreSQL, and pgAdmin.

✅ **Database Operations (Assignment 1)**
- SQL queries to create, insert, update, delete, and join data between `users` and `calculations` tables.

✅ **Testing**
- Unit tests:
  - Calculator operations
  - Password hashing helpers
  - Pydantic schemas
- Integration tests:
  - API endpoints
  - User model uniqueness and DB behavior (using Postgres)
- End-to-End tests:
  - Browser tests with **Playwright** for the calculator UI.

✅ **Logging**
- Logs all API and database activity to `logs/app.log`.

✅ **CI/CD**
- GitHub Actions workflow:
  - Spins up a Postgres service
  - Runs Python unit & integration tests
  - Runs Playwright tests
  - Builds and pushes a Docker image to Docker Hub on successful pushes (using repo secrets).

---

## 🧠 Project Structure

```text
fastapi-calculator/
├── app/
│   ├── main.py
│   ├── operations.py
│   ├── logger.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── DockerFile
├── sql/
│   └── steps.sql
├── tests/
│   ├── unit/
│   │   ├── test_operations.py
│   │   ├── test_security.py
│   │   └── test_schemas.py
│   ├── integration/
│   │   ├── test_api.py
│   │   └── test_user_model.py
│   └── e2e/
│       └── tests/
│           └── test_calculator.spec.ts
├── logs/
│   └── app.log
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── .env.example
├── FastAPI_Postgres_Assignment.pdf
├── requirements.txt
└── README.md
```

---

## ⚙️ Run Locally (Without Docker)

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# or Git Bash / macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

- API docs: http://localhost:8000/docs  
- Calculator UI: http://localhost:8000  
- Health endpoint: http://localhost:8000/health  
- DB ping: http://localhost:8000/db-ping

---

## 🔐 Secure User Model

### Endpoints

- **Create user**

  `POST /users`

  Request body example:
  ```json
  {
    "username": "alice",
    "email": "alice@example.com",
    "password": "secret123"
  }
  ```

  Response example:
  ```json
  {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "created_at": "2025-11-16T19:37:32.867729"
  }
  ```

- **List users**

  `GET /users`

  Returns `List[UserRead]` (no password hashes).

### Implementation details

- SQLAlchemy model: `app/models.py`
- Pydantic schemas: `app/schemas.py`
- Password hashing: `app/security.py`
- CRUD helpers: `app/crud.py`
- DB session & engine: `app/database.py`

---

## 🧪 Running Tests Locally

Make sure Postgres is running (either via Docker or locally). For Docker:

```bash
docker-compose up -d db
```

Then, with your virtualenv active:

```bash
# Run all unit + integration tests
pytest -q
```

To run only user/security tests:

```bash
pytest tests/unit/test_security.py tests/unit/test_schemas.py tests/integration/test_user_model.py -q
```

### Playwright E2E tests

1. Ensure the FastAPI app is running locally:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. In another terminal:
   ```bash
   npm install
   npx playwright install --with-deps chromium
   npx playwright test
   ```

---

## 🐳 Run with Docker Compose

```bash
docker-compose up --build
```

Access:

- FastAPI → http://localhost:8000
- pgAdmin → http://localhost:5050

Default credentials (from `.env`):

```text
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin123
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fastapi_db
```

In pgAdmin, connect to:

```text
Host: db
Port: 5432
Database: fastapi_db
Username: postgres
Password: postgres
```

---

## 🧾 SQL Operations (Assignment 1)

All commands are in [`sql/steps.sql`](sql/steps.sql):

1️⃣ **Create Tables**
```sql
CREATE TABLE users (...);
CREATE TABLE calculations (...);
```

2️⃣ **Insert Records**
```sql
INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com');
```

3️⃣ **Query Data**
```sql
SELECT * FROM users;
SELECT u.username, c.operation, c.result
FROM calculations c
JOIN users u ON c.user_id = u.id;
```

4️⃣ **Update / Delete**
```sql
UPDATE calculations SET result = 6 WHERE id = 1;
DELETE FROM calculations WHERE id = 2;
```

---

## 🔁 CI/CD & Docker Hub

The GitHub Actions workflow (`.github/workflows/ci.yml`) does the following:

1. **Test job**
   - Starts a Postgres service
   - Sets `DATABASE_URL` for the app
   - Installs Python dependencies
   - Runs `pytest`
   - Installs Node + Playwright
   - Starts FastAPI server
   - Runs Playwright E2E tests

2. **Build & Push job**
   - Runs after tests succeed on `push`
   - Logs in to Docker Hub using:
     - `DOCKERHUB_USERNAME`
     - `DOCKERHUB_TOKEN` (Docker Hub access token)
   - Builds the Docker image from `app/DockerFile`
   - Pushes tags:
     - `${DOCKERHUB_USERNAME}/fastapi-calculator:latest`
     - `${DOCKERHUB_USERNAME}/fastapi-calculator:${GITHUB_SHA}`

Update the README with your actual Docker Hub repository link where appropriate.

---

## 🖼️ Screenshots

### 🧩 Docker & Database Proof (Assignment 1)
- ![Create Table](M9_Screenshots/pgAdmin_createQuery.png)
- ![Insert Records](M9_Screenshots/insertQuery.png)
- ![Join Query](M9_Screenshots/select_query.png)
- ![Update Query](M9_Screenshots/updateQuery.png)
- ![Delete Query](M9_Screenshots/deleteQuery.png)
- ![FastAPI Health Check](M9_Screenshots/health_dbUp_screenshot.png)

### 🔐 Secure User Model (This assignment)
- ![POST /users](M10_Screenshots/post_request.png)
- ![GET /users](M10_Screenshots/get_users.png)
- ![users_secure in pgAdmin](M10_Screenshots/pg_admin.png)

### 🟢 GitHub Actions Workflow
![CI Success](https://github.com/irajbhinde/fastapi-calculator/blob/main/actions-success.png)

---

## 📄 Documentation

Full screenshots and outputs for the database assignment → [`FastAPI_Postgres_Assignment.pdf`](./FastAPI_Postgres_Assignment.pdf)

---

## 🌐 Repository

- Main repo:  
  🔗 **GitHub:** https://github.com/irajbhinde/fastapi-calculator
- This assignment branch:  
  🔗 **GitHub (secure user + CI/CD):** https://github.com/irajbhinde/fastapi-calculator/tree/secure-user-ci