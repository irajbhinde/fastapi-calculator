
# 🧮 FastAPI Calculator

A simple **FastAPI-based calculator** demonstrating:
- Unit, integration, and end-to-end testing with **Playwright**
- Structured logging
- Continuous Integration with **GitHub Actions**

![CI](https://github.com/irajbhinde/fastapi-calculator/actions/workflows/ci.yml/badge.svg)

---

## 🚀 Features

✅ REST API Endpoints  
`/add`, `/subtract`, `/multiply`, `/divide`, `/health` where /add, /subtract, /multiply and /divide are POST requests and /health is a GET request

✅ HTML UI  
Served at `/` — lets you perform arithmetic operations interactively.

✅ Logging  
All operations and errors are logged to `logs/app.log` (rotating handler).

✅ Tests
- **Unit tests** → pure functions in `app/operations.py`
- **Integration tests** → FastAPI endpoints in `app/main.py`
- **End-to-End tests** → browser automation via Playwright (`tests/e2e/`)

✅ Continuous Integration  
GitHub Actions workflow runs **pytest** + **Playwright** on every push.

---

## 🧠 Project Structure
```
fastapi-calculator/
├── app/
│   ├── main.py
│   ├── operations.py
│   ├── logger.py
│   ├── templates/
│   └── static/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── logs/
├── .github/workflows/ci.yml
├── playwright.config.ts
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## ⚙️ Run Locally

### 1️⃣ Create venv and install dependencies
```bash
python -m venv .venv
# PowerShell:
.venv\Scripts\Activate.ps1
# Bash:
source .venv/Scripts/activate

pip install -r requirements.txt
```

### 2️⃣ Start the app
```bash
uvicorn app.main:app --reload
```
Then open [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Run Tests

### ✅ Unit + Integration Tests
```bash
pytest -q
```

### ✅ End-to-End Tests (Playwright)
Start the FastAPI server in one terminal:
```bash
uvicorn app.main:app --port 8000
```
In another terminal:
```bash
npm install -D @playwright/test
npx playwright install
npx playwright test
```

---

## 🖼️ Screenshots

### 🟢 GitHub Actions – Successful Workflow Run  
![GitHub Actions Success](https://github.com/irajbhinde/fastapi-calculator/blob/main/actions-success.png)

### 🖥️ App Running in Browser  
![App Running](https://github.com/irajbhinde/fastapi-calculator/blob/main/app-running.png)

---

## 📄 Notes

- Division by zero returns HTTP 400 with a helpful message.
- Numeric inputs are coerced to float; invalid inputs raise a 400.
- Logs saved to `logs/app.log`.

---

## 🌐 Repository

🔗 **GitHub:** [https://github.com/irajbhinde/fastapi-calculator](https://github.com/irajbhinde/fastapi-calculator)

---

**Developed by [@irajbhinde](https://github.com/irajbhinde)**
