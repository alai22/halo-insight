"""
Survicate API Response Parser

Converts Survicate API JSON responses to SurveyResponse objects
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from ..models.survey import SurveyResponse
from ..utils.logging import get_logger

logger = get_logger('survicate_api_parser')


class SurvicateAPIParser:
    """Parser for Survicate API responses"""
    
    @staticmethod
    def parse_responses(api_responses: List[Dict[str, Any]]) -> List[SurveyResponse]:
        """
        Parse API response objects into SurveyResponse objects
        
        Args:
            api_responses: List of response objects from Survicate API
        
        Returns:
            List of SurveyResponse objects
        """
        parsed_responses = []
        
        for api_response in api_responses:
            try:
                survey_response = SurvicateAPIParser._parse_single_response(api_response)
                if survey_response:
                    parsed_responses.append(survey_response)
            except Exception as e:
                logger.warning(f"Failed to parse response {api_response.get('id', 'unknown')}: {e}")
                continue
        
        logger.info(f"Parsed {len(parsed_responses)}/{len(api_responses)} responses")
        return parsed_responses
    
    @staticmethod
    def _parse_single_response(api_response: Dict[str, Any]) -> Optional[SurveyResponse]:
        """Parse a single API response object"""
        # Extract basic fields
        response_id = api_response.get('id', '')
        respondent_id = api_response.get('respondentId', '')
        
        # Parse date/time
        created_at = api_response.get('createdAt', '')
        if created_at:
            # Convert ISO 8601 to our format: 'YYYY-MM-DD HH:MM:SS'
            try:
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                date_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                date_time = created_at
        else:
            date_time = ''
        
        if not response_id or not date_time:
            return None
        
        # Extract respondent attributes
        attributes = api_response.get('attributes', {}) or {}
        email = attributes.get('email') or None
        first_name = attributes.get('first_name') or None
        last_name = attributes.get('last_name') or None
        user_id = attributes.get('user_id') or attributes.get('sso_id') or attributes.get('braze_id') or None
        
        # Extract metadata
        metadata = {
            'device': api_response.get('device', {}).get('type') if isinstance(api_response.get('device'), dict) else None,
            'platform': api_response.get('device', {}).get('os') if isinstance(api_response.get('device'), dict) else None,
            'page': api_response.get('page', ''),
            'braze_id': attributes.get('braze_id'),
            'sso_id': attributes.get('sso_id'),
        }
        
        # Extract answers
        answers = {}
        api_answers = api_response.get('answers', []) or []
        
        for answer_obj in api_answers:
            question_id = answer_obj.get('questionId', '')
            question_text = answer_obj.get('questionText', '')
            
            # Generate question key (Q1, Q2, etc.)
            question_key = SurvicateAPIParser._extract_question_key(question_id, question_text)
            if not question_key:
                continue
            
            # Extract answer value
            answer_value = SurvicateAPIParser._extract_answer_value(answer_obj)
            comment_value = answer_obj.get('comment') or answer_obj.get('text') or None
            
            if answer_value or comment_value:
                answers[question_key] = {
                    'Answer': answer_value,
                    'Comment': comment_value
                }
        
        return SurveyResponse(
            response_uuid=response_id,
            respondent_uuid=respondent_id,
            date_time=date_time,
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_id=user_id,
            answers=answers,
            metadata=metadata
        )
    
    @staticmethod
    def _extract_question_key(question_id: str, question_text: str) -> Optional[str]:
        """Extract question key from question ID or text"""
        # Try to extract Q# pattern from question text
        import re
        
        # Look for Q# pattern in question text
        match = re.search(r'Q#?(\d+)', question_text, re.IGNORECASE)
        if match:
            return f"Q{match.group(1)}"
        
        # If question_id looks like a number, use it
        if question_id.isdigit():
            return f"Q{question_id}"
        
        # Try to extract number from question_id
        match = re.search(r'(\d+)', question_id)
        if match:
            return f"Q{match.group(1)}"
        
        # Fallback: use question_id as-is if it's short
        if len(question_id) < 20:
            return question_id
        
        return None
    
    @staticmethod
    def _extract_answer_value(answer_obj: Dict[str, Any]) -> Optional[str]:
        """Extract answer value from answer object"""
        # Try different answer fields
        if answer_obj.get('answer'):
            return str(answer_obj['answer'])
        
        if answer_obj.get('value'):
            return str(answer_obj['value'])
        
        if answer_obj.get('text'):
            return str(answer_obj['text'])
        
        # Handle choice answers
        choices = answer_obj.get('choices', [])
        if choices:
            choice_texts = [str(c.get('text', c.get('label', ''))) for c in choices if c]
            return ', '.join([c for c in choice_texts if c])
        
        # Handle single choice
        choice = answer_obj.get('choice')
        if choice:
            return str(choice.get('text', choice.get('label', '')))
        
        return None

