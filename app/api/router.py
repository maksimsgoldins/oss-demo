from fastapi import APIRouter
from app.api.routes.health import router as health_router
from app.api.routes.services import router as services_router
from app.api.routes.order_aims import router as order_aims_router
from app.api.routes.attributes import router as attributes_router
from app.api.routes.service_aim_mappings import router as service_aim_mappings_router
from app.api.routes.relations import router as relations_router
from app.api.routes.attribute_involvement import router as attribute_involvement_router
from app.api.routes.diagram_layout import router as diagram_layout_router
from app.api.routes.attribute_propagation import router as attribute_propagation_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(services_router)
api_router.include_router(order_aims_router)
api_router.include_router(attributes_router)
api_router.include_router(service_aim_mappings_router)
api_router.include_router(relations_router)
api_router.include_router(attribute_involvement_router)
api_router.include_router(diagram_layout_router)
api_router.include_router(attribute_propagation_router)
