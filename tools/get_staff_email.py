"""Tool to get available staff member for meeting scheduling."""

import logging
from config.logging import setup_logging
from agents import function_tool
from schema import MeetingResult

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@function_tool
def get_staff_member_email(department: str = "sales", availability_required: bool = True) -> str:
    """Get an available staff member email for meeting scheduling.
    
    Args:
        department: Department to get staff from (sales, support, engineering)
        availability_required: Whether to check availability
        
    Returns:
        Email address of available staff member
    """
    # For now, return a default staff member
    # In production, this would query a database/calendar system for availability
    
    staff_members = {
        "sales": "sales.manager@company.com",
        "support": "support.lead@company.com", 
        "engineering": "tech.lead@company.com"
    }
    
    # Default to sales if department not found
    staff_email = staff_members.get(department.lower(), staff_members["sales"])
    
    logger.info(f"Assigned staff member: {staff_email} for department: {department}")
    return staff_email