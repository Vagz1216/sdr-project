"""Tool wrappers for meeting operations."""
from typing import Dict, Any, Optional
from services import meeting_service

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
def schedule_meeting_tool(params: Dict[str, Any] | None = None, **kwargs) -> Dict[str, Any]:
    params = dict(params or {})
    params.update(kwargs)
    lead_id = params.get("lead_id")
    staff_id = params.get("staff_id")
    start_time = params.get("start_time")
    meet_link = params.get("meet_link")
    if not isinstance(lead_id, int) or not isinstance(staff_id, int):
        return {"success": False, "data": None, "error": "lead_id and staff_id must be integers"}
    if not isinstance(start_time, str) or not start_time:
        return {"success": False, "data": None, "error": "start_time must be an ISO string"}
    return meeting_service.schedule_meeting(lead_id=lead_id, staff_id=staff_id, start_time=start_time, meet_link=meet_link)
