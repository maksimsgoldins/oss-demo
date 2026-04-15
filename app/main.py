from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings
from app.api.routes.task_specs import router as task_specs_router
from app.api.routes.gateway_specs import router as gateway_specs_router
from app.api.routes.event_specs import router as event_specs_router
from app.api.routes.process_specs import router as process_specs_router
from app.api.routes.process_elements import router as process_elements_router
from app.api.routes.process_flows import router as process_flows_router
from app.api.routes.inter_process_dependencies import router as inter_process_dependencies_router

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://oss-frontend-brep.onrender.com"],
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
        "attribute_propagation": "/api/attribute-propagation",
        "diagram_layout": "/api/diagram-layout",
    }

app.include_router(api_router)
