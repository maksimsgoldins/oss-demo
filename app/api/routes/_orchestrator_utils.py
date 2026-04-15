from fastapi import HTTPException
from app.core.orchestrator_enums import (
    DEPENDENCY_TYPES, ELEMENT_TYPES, EVENT_TYPES, FLOW_TYPES,
    GATEWAY_TYPES, PROCESS_STATUS, TASK_TYPES,
)
from app.models.order_aim import OrderSubAim
from app.models.process_element import ProcessElement

def validate_in_set(value: str, allowed: set[str], label: str):
    if value not in allowed:
        raise HTTPException(status_code=400, detail=f"Invalid {label}: {value}")

def validate_task_type(value: str): validate_in_set(value, TASK_TYPES, "task_type")
def validate_gateway_type(value: str): validate_in_set(value, GATEWAY_TYPES, "gateway_type")
def validate_event_type(value: str): validate_in_set(value, EVENT_TYPES, "event_type")
def validate_process_status(value: str): validate_in_set(value, PROCESS_STATUS, "process status")
def validate_element_type(value: str): validate_in_set(value, ELEMENT_TYPES, "element_type")
def validate_flow_type(value: str): validate_in_set(value, FLOW_TYPES, "flow_type")
def validate_dependency_type(value: str): validate_in_set(value, DEPENDENCY_TYPES, "dependency_type")

def validate_sub_aim_belongs_to_aim(db, order_sub_aim_id, order_aim_id):
    sub = db.get(OrderSubAim, order_sub_aim_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Order sub-aim not found")
    if sub.order_aim_id != order_aim_id:
        raise HTTPException(status_code=400, detail="Order sub-aim does not belong to order aim")

def validate_process_element_binding(element_type, task_spec_id, gateway_spec_id, event_spec_id):
    refs = [task_spec_id is not None, gateway_spec_id is not None, event_spec_id is not None]
    if sum(refs) != 1:
        raise HTTPException(status_code=400, detail="Exactly one referenced spec must be set")
    if element_type == "task" and task_spec_id is None:
        raise HTTPException(status_code=400, detail="task_spec_id is required for task element")
    if element_type == "gateway" and gateway_spec_id is None:
        raise HTTPException(status_code=400, detail="gateway_spec_id is required for gateway element")
    if element_type == "event" and event_spec_id is None:
        raise HTTPException(status_code=400, detail="event_spec_id is required for event element")

def validate_element_belongs_to_process(element: ProcessElement, process_spec_id):
    if element.process_spec_id != process_spec_id:
        raise HTTPException(status_code=400, detail="Element does not belong to the specified process")

def validate_dependency_task_elements(source_element: ProcessElement, target_element: ProcessElement):
    if source_element.element_type != "task":
        raise HTTPException(status_code=400, detail="Source element must be task")
    if target_element.element_type != "task":
        raise HTTPException(status_code=400, detail="Target element must be task")
