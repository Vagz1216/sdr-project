"""Intent extraction agent for email content analysis."""

import json
import logging
from typing import Any

from config.logging import setup_logging
from agents import Agent, ModelSettings, Runner
from schema import EmailIntent
from config import settings

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


class IntentExtractorAgent:
    """Agent that extracts intent from email content."""
    
    def __init__(self):
        self.agent = Agent(
            name="EmailIntentExtractor",
            instructions="""
Analyze email content and classify the sender's intent with confidence.

Classify into one of these intents:
- meeting_request: Explicitly asking to schedule a meeting/call
- question: Has specific questions about services
- interest: Expressing interest but no specific questions
- opt_out: Requesting to be removed or unsubscribed
- neutral: General inquiry or acknowledgment
- bounce: Automated bounce/out-of-office message
- spam: Spam or irrelevant content

Provide confidence score 0.0-1.0 based on clarity of intent.

Respond with JSON only: {"intent": "...", "confidence": 0.0}
""",
            model_settings=ModelSettings(
                model=settings.intent_model,
                temperature=settings.intent_temperature,
                max_tokens=settings.intent_max_tokens
            )
        )
    
    async def extract_intent(self, email_content: str, subject: str = "") -> EmailIntent:
        """Extract intent from email content."""
        context = f"Subject: {subject}\nContent: {email_content}"
        
        try:
            result = await Runner.run(self.agent, context)
            return EmailIntent(**json.loads(result.final_output))
        except Exception as e:
            logger.error(f"Failed to extract intent: {e}")
            return EmailIntent(intent="neutral", confidence=0.5)