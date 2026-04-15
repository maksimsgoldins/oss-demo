TASK_TYPES = {
    "serviceTask", "userTask", "manualTask", "scriptTask",
    "callActivity", "sendTask", "receiveTask", "businessRuleTask",
}
GATEWAY_TYPES = {"exclusiveGateway", "parallelGateway", "inclusiveGateway", "eventBasedGateway"}
EVENT_TYPES = {"startEvent", "endEvent", "intermediateCatchEvent", "intermediateThrowEvent"}
ELEMENT_TYPES = {"task", "gateway", "event"}
FLOW_TYPES = {"sequenceFlow"}
DEPENDENCY_TYPES = {"finish_to_start", "start_to_start", "finish_to_finish", "start_to_finish"}
PROCESS_STATUS = {"draft", "active", "retired"}
