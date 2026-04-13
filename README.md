# OSS Backend Render Starter v3

Added in v3:
- attribute delete validation: cannot delete if used in attribute involvement
- attribute involvement supports:
  - allowed_values subset for this involvement
  - default_values constrained by allowed_values
- decomposition endpoints
- attribute propagation endpoints

Build command:
`pip install -r requirements.txt && alembic upgrade head`

Start command:
`uvicorn app.main:app --host 0.0.0.0 --port $PORT`
