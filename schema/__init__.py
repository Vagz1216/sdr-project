"""Pydantic schemas for the Squad3 application."""

from .email import EmailIntent, EmailActionResult, WebhookEvent, ResponseEvaluation, MeetingResult, MeetingDetails, EmailResponse
from .tools import SendEmailResult

__all__ = [
    "EmailIntent",
    "EmailActionResult", 
    "WebhookEvent",
    "ResponseEvaluation",
    "MeetingResult",
    "MeetingDetails",
    "EmailResponse",
    "SendEmailResult"
]