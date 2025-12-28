# 🌹 Red Rose Flower Symptom Checker Expert System

An intelligent ML-powered system for diagnosing rose flower diseases based on symptoms.

## Features

- 🔐 User authentication (register/login with JWT)
- 🤖 Machine Learning disease prediction
- 📊 Diagnosis history tracking
- 🔍 Symptom-based expert system
- 🐳 Docker containerization
- 📝 RESTful API with FastAPI

## Tech Stack

- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL 16
- **ML**: Scikit-learn, Pandas
- **Package Manager**: uv
- **Authentication**: JWT (python-jose)
- **ORM**: SQLAlchemy 2.0

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- uv package manager

### Installation

1. **Clone the repository**

   ```bash
   git clone
   cd rose-symptom-checker
   ```

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

3. **Run with Docker**

   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - PgAdmin: http://localhost:5050

### Local Development (without Docker)

1. **Install dependencies**

   ```bash
   uv pip install -e ".[dev]"
   ```

2. **Set up database**

   ```bash
   # Make sure PostgreSQL is running
   # Update DATABASE_URL in .env
   ```

3. **Train the ML model**

   ```bash
   python scripts/train_model.py
   ```

4. **Run the application**
   ```bash
   uvicorn src.main:app --reload
   ```

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

### Diagnosis

- `POST /api/v1/diagnosis/check` - Check rose disease symptoms
- `GET /api/v1/diagnosis/history` - Get user diagnosis history
- `GET /api/v1/diagnosis/history/{id}` - Get specific diagnosis

## Project Structure

```
src/
├── api/          # API routes and endpoints
├── core/         # Core configurations
├── db/           # Database models
├── schemas/      # Pydantic schemas
├── services/     # Business logic
└── ml/           # ML models and utilities
```

## Disease Categories

The system can diagnose the following rose diseases:

1. **Black Spot** - Dark spots on leaves
2. **Powdery Mildew** - White powdery coating
3. **Rust** - Orange/rust colored spots
4. **Botrytis Blight** - Gray mold on flowers
5. **Rose Mosaic** - Yellow mosaic patterns
6. **Crown Gall** - Tumor-like growths
7. **Healthy** - No disease detected

## Symptoms Input Example

```json
{
  "symptoms": ["dark_spots_on_leaves", "yellowing_leaves", "leaf_drop"]
}
```

## Testing

```bash
pytest tests/
```
