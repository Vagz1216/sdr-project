"""Response evaluation agent for email safety validation."""

import json
import logging
from typing import Dict, Any

from config.logging import setup_logging
from agents import Agent, ModelSettings, Runner
from config import settings
from schema import ResponseEvaluation

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


class ResponseEvaluator:
    """Agent that evaluates email responses before sending."""
    
    def __init__(self):
        self.agent = Agent(
            name="EmailResponseEvaluator",
            instructions="""
You are an email response quality evaluator. Your job is simple: determine if an email response is safe and appropriate to send.

Evaluate the response for:
- Professional tone and language
- Appropriate content for business context  
- No inappropriate, offensive, or unprofessional content
- Clear and helpful response to the inquiry

Return a simple pass/fail decision with brief reasoning.

Respond with JSON only: {"approved": true, "reason": "..."}
""",
            model_settings=ModelSettings(
                model=settings.intent_model,  # Reuse same model as intent extraction
                temperature=0.2,  # Low temperature for consistent evaluation  
                max_tokens=200
            )
        )
    
    async def evaluate_response(self, response_text: str, email_context: Dict[str, Any]) -> ResponseEvaluation:
        """Evaluate an email response - simple pass/fail decision."""
        sender_email = email_context.get('from_', [''])[0]
        subject = email_context.get('subject', '')
        intent = email_context.get('intent', 'unknown')
        
        context = f"Response: {response_text}\nRecipient: {sender_email}\nSubject: {subject}\nIntent: {intent}"        
        try:
            result = await Runner.run(self.agent, context)
            evaluation = ResponseEvaluation(**json.loads(result.final_output))
            logger.info(f"Response evaluation: {'APPROVED' if evaluation.approved else 'REJECTED'} - {evaluation.reason}")
            return evaluation
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return ResponseEvaluation(approved=False, reason="Evaluation failed")
            return ResponseEvaluation(
                approved=False,
                reason=f"Evaluation error: {str(e)}"
            )