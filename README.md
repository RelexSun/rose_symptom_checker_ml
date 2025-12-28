# 🌹 Red Rose Flower Symptom Checker Expert System

An intelligent **FastAPI + Machine Learning** system for diagnosing rose flower diseases based on observable symptoms. The system combines a rule-based expert layer with an ML model and supports secure JWT-based authentication.

---

## ✨ Features

- 🔐 **JWT Authentication** (Register / Login)
- 🤖 **Machine Learning Disease Prediction** (Scikit-learn)
- 📊 **Diagnosis History Tracking** (per user)
- 🔍 **Symptom-based Expert System**
- 🐳 **Dockerized Environment** (API, PostgreSQL, pgAdmin)
- 📝 **RESTful API** with FastAPI & OpenAPI (Swagger)

---

## 🧰 Tech Stack

| Layer           | Technology                  |
| --------------- | --------------------------- |
| Backend         | FastAPI (Python 3.11)       |
| Database        | PostgreSQL 16               |
| ORM             | SQLAlchemy 2.0              |
| Auth            | JWT (python-jose)           |
| ML              | Scikit-learn, Pandas, NumPy |
| Package Manager | uv                          |
| Containers      | Docker & Docker Compose     |

---

## 🚀 Quick Start (Docker – Recommended)

### Prerequisites

- Docker
- Docker Compose

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd rose-symptom-checker
```

### 2️⃣ Environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://postgres:postgres@db:5432/rose_checker
```

### 3️⃣ Run with Docker

```bash
docker compose up --build
```

### 4️⃣ Access services

- **API** → [http://localhost:8000](http://localhost:8000)
- **Swagger Docs** → [http://localhost:8000/docs](http://localhost:8000/docs)
- **pgAdmin** → [http://localhost:5050](http://localhost:5050)

---

## 🧑‍💻 Local Development (Virtual Environment)

### Prerequisites

- Python **3.11+**
- PostgreSQL running locally
- `uv` installed

```bash
pip install uv
```

---

### 1️⃣ Create & activate virtual environment

```bash
python -m venv .venv
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
.venv\\Scripts\\Activate.ps1
```

---

### 2️⃣ Install dependencies (from pyproject.toml)

```bash
uv pip install -e .
```

For development tools:

```bash
uv pip install -e ".[dev]"
```

---

### 3️⃣ Configure environment

```bash
cp .env.example .env
```

Update `DATABASE_URL`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rose_checker
```

---

### 4️⃣ Train ML model (required once)

```bash
python scripts/train_model.py
```

This generates:

- Trained model
- Label encoder

---

### 5️⃣ Run the application

```bash
uvicorn rose_symptom_checker.main:app --reload
```

---

## 🔐 Authentication Flow (JWT)

1. **Register** → `/api/v1/auth/register`
2. **Login** → `/api/v1/auth/login`
3. Receive **Access Token**
4. Authorize requests using:

```
Authorization: Bearer <access_token>
```

Swagger uses **HTTP Bearer auth** (token-only input).

---

## 📡 API Endpoints

### Auth

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`

### Diagnosis

- `POST /api/v1/diagnosis/check`
- `GET /api/v1/diagnosis/history`
- `GET /api/v1/diagnosis/history/{id}`

---

## 🧠 Disease Categories

The system can detect:

1. **Black Spot** – Dark leaf spots
2. **Powdery Mildew** – White powder coating
3. **Rust** – Orange / rust-colored spots
4. **Botrytis Blight** – Gray mold
5. **Rose Mosaic** – Yellow mosaic patterns
6. **Crown Gall** – Tumor-like growths
7. **Healthy** – No disease detected

---

## 🧪 Symptoms Input Example

```json
{
  "symptoms": ["dark_spots_on_leaves", "yellowing_leaves", "leaf_drop"]
}
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📁 Project Structure

```
src/
├── rose_symptom_checker/
│   ├── api/          # API routes
│   ├── core/         # Config, security, settings
│   ├── db/           # Models & session
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   └── ml/           # ML model utilities
scripts/          # Training & DB scripts
tests/
```

---

## ✅ Notes

- Tables are auto-created on startup via SQLAlchemy
- ML model **must be trained before first run**
- Docker users do NOT need local Python or Po
