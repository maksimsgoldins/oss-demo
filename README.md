# OSS Backend Render Starter

## What is included
- FastAPI
- PostgreSQL via SQLAlchemy
- Alembic migrations
- Health endpoint
- Basic CRUD endpoints for:
  - services
  - order aims
  - attributes

## Local run
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

## Render deploy
1. Create a GitHub repository
2. Upload this backend starter to the repository
3. In Render, create a **New Web Service**
4. Connect the GitHub repository
5. In Environment Variables set:
   - `DATABASE_URL`
6. Use:
   - Build Command: `pip install -r requirements.txt && alembic upgrade head`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Important about Render database URL
For SQLAlchemy + psycopg use this format:
```text
postgresql+psycopg://USER:PASSWORD@HOST:5432/DBNAME
```

If Render gives you:
```text
postgresql://...
```
change only the prefix to:
```text
postgresql+psycopg://...
```

## First useful endpoints
- `GET /health`
- `GET /api/services`
- `POST /api/services`
- `GET /api/order-aims`
- `POST /api/order-aims`
- `GET /api/attributes`
- `POST /api/attributes`
