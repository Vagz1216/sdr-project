"""Tool to notify staff members about scheduled meetings."""

import logging
from config.logging import setup_logging
from agents import function_tool
from tools.send_email import send_agent_email
from schema import SendEmailResult

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@function_tool
def notify_staff_about_meeting(
    staff_email: str,
    client_email: str, 
    meeting_subject: str,
    meeting_description: str,
    meeting_time: str,
    original_email_content: str = ""
) -> SendEmailResult:
    """Send notification email to staff member about scheduled meeting.
    
    Args:
        staff_email: Staff member's email address
        client_email: Client's email address
        meeting_subject: Subject of the scheduled meeting
        meeting_description: Description/agenda of the meeting
        meeting_time: Meeting start time
        original_email_content: Original client email content for context
        
    Returns:
        SendEmailResult with success status
    """
    try:
        # Create staff notification email
        staff_subject = f"Meeting Scheduled: {meeting_subject}"
        
        staff_body = f"""Hi there,

A meeting has been automatically scheduled with a client. Here are the details:

CLIENT: {client_email}
MEETING: {meeting_subject}
TIME: {meeting_time}
AGENDA: {meeting_description}

ORIGINAL CLIENT MESSAGE:
{original_email_content[:500]}{'...' if len(original_email_content) > 500 else ''}

The client has been sent a calendar invitation. Please review your calendar and prepare for the meeting.

If you need to reschedule or have any questions, please contact the client directly.

Best regards,
Automated Meeting System"""

        # Send notification to staff
        result = send_agent_email(
            email=staff_email,
            name="Team Member",
            subject=staff_subject,
            body=staff_body
        )
        
        if result.ok:
            logger.info(f"Staff notification sent to {staff_email} for meeting with {client_email}")
        else:
            logger.error(f"Failed to send staff notification: {result.error}")
            
        return result
        
    except Exception as e:
        logger.error(f"Error sending staff notification: {e}")
        return SendEmailResult(
            ok=False,
            error=f"Failed to send staff notification: {str(e)}"
        )