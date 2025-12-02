# 📘 FastAPI Calculator --- Full Stack App (Modules 9--13)

A complete calculator web application built using **FastAPI, PostgreSQL,
SQLAlchemy, Jinja2, JWT Authentication, and Playwright E2E tests**.

This project includes:

-   Calculator API (add/subtract/multiply/divide)
-   Database-backed calculation storage
-   User registration (REST + JWT)
-   HTML frontend for Register/Login
-   Static assets (CSS, JS)
-   JWT authentication from frontend (`auth.js`)
-   Full Playwright E2E test suite

------------------------------------------------------------------------

## 🚀 Features

### 🔢 Calculator

-   Add, subtract, multiply, divide
-   Store and view past calculations
-   Full CRUD operations for saved calculations

### 👤 Users

Login options: - **`/users/login`** → Module 12 legacy login
(identifier + password) - **`/login`** → Module 13 JWT login (email +
password)

JWT Auth: - **POST `/register`** → Register & return JWT - **POST
`/login`** → Login & return JWT

------------------------------------------------------------------------

## 🎨 Frontend Auth Pages

### `/register` DOM IDs

-   `#reg-username`
-   `#reg-email`
-   `#reg-password`
-   `#reg-confirm`
-   `#register-success`
-   `#register-error`

### `/login` DOM IDs

-   `#login-identifier`
-   `#login-password`
-   `#login-success`
-   `#login-error`

**Auth JS (`static/auth.js`)** - Handles form submission - Performs
login/register requests - Saves JWT to `localStorage.access_token` -
Updates DOM for Playwright selectors

------------------------------------------------------------------------

# 📂 Project Structure

    app/
     ├── main.py
     ├── models.py
     ├── schemas.py
     ├── crud.py
     ├── security.py
     ├── database.py
     ├── operations.py
     ├── calculation_factory.py
     ├── templates/
     │    ├── index.html
     │    ├── login.html
     │    └── register.html
     └── static/
          ├── styles.css
          └── auth.js
    tests/
     ├── integration/
     ├── unit/
     └── e2e/

------------------------------------------------------------------------

# 🛠️ Installation

### 1. Create virtual environment

``` bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 2. Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# 🗄️ Database Setup (PostgreSQL)

Default connection:

    postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_db

Create database:

``` sql
CREATE DATABASE fastapi_db;
```

------------------------------------------------------------------------

# 🐳 Docker Setup

``` bash
docker build -t fastapi-calculator .
docker run -p 8000:8000 fastapi-calculator
```

------------------------------------------------------------------------

# ▶️ Run the App

``` bash
uvicorn app.main:app --reload
```

Open in browser:

-   **App UI:** http://127.0.0.1:8000\
-   **Docs:** http://127.0.0.1:8000/docs\
-   **Register:** http://127.0.0.1:8000/register\
-   **Login:** http://127.0.0.1:8000/login

------------------------------------------------------------------------

# 🔐 JWT Authentication Guide

### Register

``` json
POST /register
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "secret123"
}
```

### Login

``` json
POST /login
{
  "email": "alice@example.com",
  "password": "secret123"
}
```

Token is stored in:

    localStorage.access_token

------------------------------------------------------------------------

# 🧪 Testing

### Unit + Integration Tests

``` bash
pytest -q
```

### Playwright Tests

``` bash
npm install
npx playwright install
npx playwright test
```

------------------------------------------------------------------------

# 🖼️ GitHub Actions Screenshot

Add screenshot in:

    Screenshots/M13_Screenshots

------------------------------------------------------------------------

# 🧮 Module 9--12 Summary

-   Calculator API\
-   PostgreSQL integration\
-   Secure user system\
-   Calculation model\
-   CRUD API\
-   JWT authentication\
-   CI/CD with GitHub Actions\
-   Playwright E2E testing

------------------------------------------------------------------------

# 🌐 Repository Links

**Main Repo:**\
https://github.com/irajbhinde/fastapi-calculator

**Module 12 Branch:**\
https://github.com/irajbhinde/fastapi-calculator/tree/module12-user-calculation-routes

**Docker Hub:**\
https://hub.docker.com/r/rajbhinde/fastapi-calculator
