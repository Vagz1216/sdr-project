"""Tool wrappers for email operations."""
from typing import Dict, Any
from services import email_service

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
def save_email_tool(params: Dict[str, Any] | None = None, **kwargs) -> Dict[str, Any]:
    params = dict(params or {})
    params.update(kwargs)
    lead_id = params.get("lead_id")
    campaign_id = params.get("campaign_id")
    subject = params.get("subject")
    body = params.get("body")
    if not isinstance(lead_id, int) or not isinstance(campaign_id, int):
        return {"success": False, "data": None, "error": "lead_id and campaign_id must be integers"}
    if subject is None or body is None:
        return {"success": False, "data": None, "error": "subject and body are required"}
    return email_service.save_email(lead_id=lead_id, campaign_id=campaign_id, subject=subject, body=body)


@function_tool
def fetch_inbound_messages_tool(params: Dict[str, Any] | None = None, **kwargs) -> Dict[str, Any]:
    # params not used; kept for compatibility
    return email_service.fetch_inbound_messages()


@function_tool
def mark_processed_tool(params: Dict[str, Any] | None = None, **kwargs) -> Dict[str, Any]:
    params = dict(params or {})
    params.update(kwargs)
    message_id = params.get("message_id")
    intent = params.get("intent")
    if not isinstance(message_id, int) or not isinstance(intent, str):
        return {"success": False, "data": None, "error": "message_id must be int and intent must be string"}
    return email_service.mark_processed(message_id=message_id, intent=intent)
