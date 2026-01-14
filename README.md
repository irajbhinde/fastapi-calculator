# FastAPI Calculator – Extended with Power Operation & Usage Stats

This project is a full‑stack FastAPI application integrating:

- User authentication (JWT)
- Calculator operations (add, subtract, multiply, divide, **power**)
- Full BREAD (Browse, Read, Edit, Add, Delete) interface for calculations
- Usage statistics reporting
- PostgreSQL via SQLAlchemy
- End‑to‑end testing using Playwright
- CI/CD with GitHub Actions
- Dockerized deployment

---

## New Features (Implemented)

### **1. Additional Calculation Type — Power (Exponentiation)**

The app now supports an advanced operation `power` that computes **a^b**.

#### 🔧 Backend
- Implemented in `app/operations.py` as `power(a, b)`.
- Integrated into the calculator factory in `app/calculation_factory.py`.
- New route:  
  **POST `/power`**  
  Returns the computed exponentiation value.

Example (PowerShell):
```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/power -ContentType 'application/json' -Body '{"a":2,"b":3}'
# -> { "result": 8.0 }
```

#### 🎨 Frontend
- Added a **Power** operation button on the main calculator page (`/`).
- Wired via `app/static/script.js`.

#### 🧪 Tests
- **Unit:** `tests/unit/test_operations.py` validates exponentiation logic.
- **Integration:** `tests/integration/test_api.py` includes `POST /power` route tests.
- **E2E:** Playwright tests validate the UI flow involving Power.

---

### **2. Report / History Feature — Usage Statistics**

The application now tracks total and per‑operation usage.

#### 🔧 Backend
A new API endpoint:

**GET `/api/calculations/stats`**

Returns:
- `total_calculations`
- Per‑operation counts: add, subtract, multiply, divide, **power**
- Averages of A, B, and result

#### 🎨 Frontend
The **Calculations BREAD** page (`/calculations-ui`) now includes a **Usage Stats** card.  
Implemented in: `app/static/calculations.js`

#### 🧪 Tests
- **Unit:** verifies aggregation logic in CRUD
- **Integration:** confirms stats route responses
- **E2E:** validates stats updates through BREAD flow

---

## Run Locally

### Start backend
```powershell
uvicorn app.main:app --reload
```

### Test Power endpoint
```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/power -ContentType 'application/json' -Body '{"a":5,"b":2}'
```

### Use Power in UI
Visit:
```
http://127.0.0.1:8000/
```

### Fetch Stats
```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/calculations/stats | ConvertTo-Json
```

### Run Tests
```powershell
pytest
npx playwright install
npx playwright test
```

---

## Reflection

Building the Power feature expanded the calculator from basic operations to advanced computation. This required aligned updates across back‑end logic, schemas, routing, UI behavior, and all test layers. Ensuring the calculation factory and UI events remained consistent was key.

The usage statistics system added real analytical capability to the project, requiring careful DB aggregation and clear UI presentation. Validating these interactions through unit, integration, and E2E tests helped create a more production‑ready feature set overall.

