
# 🧮 FastAPI Calculator + 🐘 PostgreSQL Integration (Docker Compose)

This repository demonstrates:
- A **FastAPI-based calculator** application.
- Integration with **PostgreSQL and pgAdmin** using **Docker Compose**.
- Logging, automated testing, and CI/CD with GitHub Actions.

![CI](https://github.com/irajbhinde/fastapi-calculator/actions/workflows/ci.yml/badge.svg)

---

## 🚀 Features

✅ **Calculator API**
- `/add`, `/subtract`, `/multiply`, `/divide`, `/health`  
  (POST for arithmetic operations, GET for `/health`)

✅ **Docker Integration**
- Fully containerized setup with FastAPI, PostgreSQL, and pgAdmin.

✅ **Database Operations**
- SQL queries to create, insert, update, delete, and join data between `users` and `calculations` tables.

✅ **Testing**
- Unit, integration, and Playwright end-to-end tests.

✅ **Logging**
- Logs all API and database activity to `logs/app.log`.

---

## 🧠 Project Structure

```
fastapi-calculator/
├── app/
│   ├── main.py
│   ├── operations.py
│   ├── logger.py
│   └── DockerFile
├── sql/
│   └── steps.sql
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── logs/
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
.venv\Scripts\activate   # or source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open [http://localhost:8000](http://localhost:8000)

---

## 🐳 Run with Docker Compose

```bash
docker-compose up --build
```

Access:
- FastAPI → [http://localhost:8000](http://localhost:8000)
- pgAdmin → [http://localhost:5050](http://localhost:5050)

Default credentials (from `.env`):
```
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin123
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fastapi_db
```

In pgAdmin, connect to:
```
Host: db
Port: 5432
Database: fastapi_db
Username: postgres
Password: postgres
```

---

## 🧾 SQL Operations

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
SELECT u.username, c.operation, c.result FROM calculations c JOIN users u ON c.user_id = u.id;
```

4️⃣ **Update / Delete**
```sql
UPDATE calculations SET result = 6 WHERE id = 1;
DELETE FROM calculations WHERE id = 2;
```

---

## 🖼️ Screenshots

### 🧩 Docker & Database Proof
- ![Create Table](M9_Screenshots/pgAdmin_createQuery.png)
- ![Insert Records](M9_Screenshots/insertQuery.png)
- ![Join Query](M9_Screenshots/select_query.png)
- ![Update Query](M9_Screenshots/updateQuery.png)
- ![Delete Query](M9_Screenshots/deleteQuery.png)
- ![FastAPI Health Check](M9_Screenshots/health_dbUp_screenshot.png)

### 🟢 GitHub Actions Workflow  
![CI Success]([https://github.com/irajbhinde/fastapi-calculator/blob/main/actions-success.png](https://github.com/irajbhinde/fastapi-calculator/blob/postgres-pgAdmin-module9/M9_Screenshots/github_actions_screenshot.png))

---

## 📄 Documentation

Full screenshots and outputs → [`FastAPI_Postgres_Assignment.pdf`](./M9_Screenshots/FastAPI_Postgres_Assignment_Screenshots.pdf)

---

## 🌐 Repository

🔗 **GitHub:** [[https://github.com/irajbhinde/fastapi-calculator/tree/docker-postgres-setup](https://github.com/irajbhinde/fastapi-calculator/tree/postgres-pgAdmin-module9)]

---

**Developed by [@irajbhinde](https://github.com/irajbhinde)**  
© 2025 – NJIT Python for Web Development
