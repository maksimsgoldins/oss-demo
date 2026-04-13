from fastapi import APIRouter
from app.api.routes.health import router as health_router
from app.api.routes.services import router as services_router
from app.api.routes.order_aims import router as order_aims_router
from app.api.routes.attributes import router as attributes_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(services_router)
api_router.include_router(order_aims_router)
api_router.include_router(attributes_router)
