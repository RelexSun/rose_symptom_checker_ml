FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./

RUN pip install --no-cache-dir \
    fastapi>=0.109.0 \
    uvicorn[standard]>=0.27.0 \
    sqlalchemy>=2.0.25 \
    psycopg2-binary>=2.9.9 \
    python-jose[cryptography]>=3.3.0 \
    passlib[bcrypt]>=1.7.4 \
    argon2-cffi>=23.1.0 \
    python-multipart>=0.0.6 \
    pydantic[email]>=2.5.3 \
    pydantic-settings>=2.1.0 \
    scikit-learn>=1.4.0 \
    pandas>=2.2.0 \
    numpy>=1.26.3 \
    joblib>=1.3.2 \
    python-dotenv>=1.0.0

COPY . .

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "rose_symptom_checker.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
