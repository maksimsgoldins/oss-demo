from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

@app.get("/")
def root():
    return {
        "message": "OSS Catalog API is running",
        "health": "/health",
        "services": "/api/services",
        "order_aims": "/api/order-aims",
        "attributes": "/api/attributes",
    }

app.include_router(api_router)
