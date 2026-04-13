from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://oss-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "OSS Catalog API is running",
        "health": "/health",
        "services": "/api/services",
        "order_aims": "/api/order-aims",
        "attributes": "/api/attributes",
        "service_aim_mappings": "/api/service-aim-mappings",
        "relations": "/api/relations",
        "attribute_involvement": "/api/attribute-involvement",
        "diagram_layout": "/api/diagram-layout",
    }

app.include_router(api_router)
