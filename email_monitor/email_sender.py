"""Email sender agent - intelligent agent with access to email and meeting tools."""

import logging
from typing import Dict, Any

from config.logging import setup_logging
from agents import Agent, ModelSettings, Runner
from tools import (
    send_reply_email, 
    create_google_meeting,
    get_staff_member_email,
    notify_staff_about_meeting,
    generate_meeting_details
)
from schema import EmailActionResult
from config import settings

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)


class EmailSenderAgent:
    """Intelligent agent that can send emails, create meetings, and take other actions."""
    
    def __init__(self):
        self.agent = Agent(
            name="EmailSenderAgent",
            instructions="""
You are a professional email and meeting coordination agent. Based on the approved response and email context, take appropriate actions.

Your available actions:
- Send email replies using send_reply_email tool  
- Generate meeting details using generate_meeting_details tool
- Get staff member email using get_staff_member_email tool
- Create Google Calendar meetings using create_google_meeting tool
- Send meeting notifications to staff using notify_staff_about_meeting tool

IMPORTANT WORKFLOW FOR MEETINGS:
1. Always send the approved response using send_reply_email tool first
2. If the response mentions scheduling a meeting, call, or appointment:
   a) Generate meeting details using generate_meeting_details tool
   b) Get staff member email using get_staff_member_email tool
   c) Create meeting with create_google_meeting tool (include client + staff emails)
   d) Send notification to staff using notify_staff_about_meeting tool

Execute tools in the correct sequence for meeting scenarios.
""",
            tools=[
                send_reply_email, 
                generate_meeting_details,
                create_google_meeting,
                get_staff_member_email,
                notify_staff_about_meeting
            ],
            model_settings=ModelSettings(
                model=settings.response_model,
                temperature=0.3,  # Lower temperature for precise execution
                max_tokens=500
            )
        )
    
    async def execute_action(self, approved_response: str, email_data: Dict[str, Any]) -> EmailActionResult:
        """Execute the appropriate action (send email, create meeting, etc.) based on the approved response."""
        sender_email = email_data.get('from_', [''])[0]
        thread_id = email_data.get('thread_id')
        subject = email_data.get('subject', '')
        
        # Build context for the agent 
        intent_data = email_data.get('intent', {})
        conversation_history = email_data.get('conversation_history', '')
        email_content = email_data.get('text', '') or email_data.get('preview', '')
        
        context = f"""
The following response has been approved and should be sent:

APPROVED RESPONSE:
{approved_response}

EMAIL CONTEXT:
- From: {sender_email}
- Subject: {subject}  
- Thread ID: {thread_id}
- Content: {email_content}
- Client Intent: {intent_data.get('intent', 'unknown')} (confidence: {intent_data.get('confidence', 0.0)})
- Conversation History: {conversation_history or "No previous conversation."}

INSTRUCTIONS:
1. Always send the approved response using send_reply_email tool
2. If the response mentions scheduling a meeting/call/appointment:
   a) Use generate_meeting_details tool with the email context
   b) Get staff email using get_staff_member_email tool  
   c) Create meeting with create_google_meeting tool (include client + staff emails)
   d) Send notification to staff using notify_staff_about_meeting tool

Execute the appropriate combination of tools based on the approved response content.
"""
        
        try:
            result = await Runner.run(self.agent, context)
            
            logger.info(f"Email action executed for {sender_email}")
            return EmailActionResult(
                action_taken="sent",
                success=True,
                message_id=None,  # Will be populated by the tool
                thread_id=thread_id
            )
            
        except Exception as e:
            logger.error(f"Error executing email action: {e}")
            return EmailActionResult(
                action_taken="error",
                success=False,
                error=str(e)
            )