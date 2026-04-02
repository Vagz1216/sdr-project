"""Pydantic schemas for the Squad3 application."""

from .email import EmailIntent, EmailActionResult, WebhookEvent, ResponseEvaluation, MeetingResult, MeetingDetails, EmailResponse
from .tools import SendEmailResult, LeadOut, StaffOut

__all__ = [
    "EmailIntent",
    "EmailActionResult", 
    "WebhookEvent",
    "ResponseEvaluation",
    "MeetingResult",
    "MeetingDetails",
    "EmailResponse",
    "SendEmailResult"
    "SendEmailResult",
    "LeadOut",
    "StaffOut"
]