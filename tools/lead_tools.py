"""Tool wrappers for lead-related operations.

Each function returns a strict JSON structure:
{
    "success": bool,
    "data": ...,
    "error": null|string
}
"""
from typing import Dict, Any, Optional, List
from services import lead_service
from packages.schema.lead_models import LeadOut

# Provide a local no-op `function_tool` so editors and tests don't error
from typing import Callable, TypeVar, ParamSpec
P = ParamSpec("P")
R = TypeVar("R")
def function_tool(func: Callable[P, R]) -> Callable[P, R]:
    return func

# If the real OpenAI `function_tool` is available at runtime, use it instead
try:
    from openai import function_tool as _real_function_tool  # type: ignore
except Exception:
    _real_function_tool = None

if _real_function_tool is not None:
    function_tool = _real_function_tool


@function_tool
def get_leads_tool(params: Dict[str, Any] | None = None, **kwargs) -> Dict[str, Any]:
    # Accept either a single params dict or keyword args for backwards compatibility
    params = dict(params or {})
    params.update(kwargs)
    email_cap = params.get("email_cap", 5)
    if not isinstance(email_cap, int) or email_cap <= 0:
        return {"success": False, "data": None, "error": "email_cap must be a positive integer"}
    res = lead_service.get_leads(email_cap=email_cap)
    if not res.get("success"):
        return res
    raw = res.get("data") or []
    validated: List[LeadOut] = []
    errors = []
    for idx, item in enumerate(raw):
        try:
            validated.append(LeadOut(**item))
        except Exception as e:
            errors.append(f"item_{idx}: {str(e)}")
    if errors:
        return {"success": False, "data": None, "error": "; ".join(errors)}
    return {"success": True, "data": [l.dict() for l in validated], "error": None}


@function_tool
def update_lead_touch_tool(params: Dict[str, Any] | None = None, **kwargs) -> Dict[str, Any]:
    params = dict(params or {})
    params.update(kwargs)
    lead_id = params.get("lead_id")
    campaign_id = params.get("campaign_id")
    if not isinstance(lead_id, int) or not isinstance(campaign_id, int):
        return {"success": False, "data": None, "error": "lead_id and campaign_id must be integers"}
    return lead_service.update_lead_touch(lead_id=lead_id, campaign_id=campaign_id)


@function_tool
def get_thread_tool(params: Dict[str, Any] | None = None, **kwargs) -> Dict[str, Any]:
    params = dict(params or {})
    params.update(kwargs)
    lead_id = params.get("lead_id")
    if not isinstance(lead_id, int):
        return {"success": False, "data": None, "error": "lead_id must be an integer"}
    return lead_service.get_thread(lead_id=lead_id)


@function_tool
def update_lead_status_tool(params: Dict[str, Any] | None = None, **kwargs) -> Dict[str, Any]:
    params = dict(params or {})
    params.update(kwargs)
    lead_id = params.get("lead_id")
    status = params.get("status")
    if not isinstance(lead_id, int) or not isinstance(status, str):
        return {"success": False, "data": None, "error": "lead_id must be int and status must be string"}
    return lead_service.update_lead_status(lead_id=lead_id, status=status)


@function_tool
def log_event_tool(params: Dict[str, Any] | None = None, **kwargs) -> Dict[str, Any]:
    params = dict(params or {})
    params.update(kwargs)
    t = params.get("type") or params.get("event_type")
    payload = params.get("payload")
    metadata = params.get("metadata")
    if not isinstance(t, str) or not t:
        return {"success": False, "data": None, "error": "type is required and must be a string"}
    return lead_service.log_event(event_type=t, payload=payload, metadata=metadata)
