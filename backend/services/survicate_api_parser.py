"""
Survicate API Response Parser

Converts Survicate API JSON responses to SurveyResponse objects
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from ..models.survey import SurveyResponse
from ..utils.logging import get_logger

logger = get_logger('survicate_api_parser')


class SurvicateAPIParser:
    """Parser for Survicate API responses"""
    
    def __init__(self):
        """Initialize parser with optional questions map"""
        self.questions_map = {}  # Maps question_id -> question_text
    
    def parse_responses(self, api_responses: List[Dict[str, Any]]) -> List[SurveyResponse]:
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
                survey_response = self._parse_single_response(api_response)
                if survey_response:
                    parsed_responses.append(survey_response)
            except Exception as e:
                logger.warning(f"Failed to parse response {api_response.get('uuid', 'unknown')}: {e}")
                continue
        
        logger.info(f"Parsed {len(parsed_responses)}/{len(api_responses)} responses")
        return parsed_responses
    
    def _parse_single_response(self, api_response: Dict[str, Any]) -> Optional[SurveyResponse]:
        """
        Parse a single API response object according to Survicate API documentation
        
        Expected structure:
        {
            "uuid": "...",
            "respondent_uuid": "...",
            "collected_at": "2023-01-01T00:00:00.000000Z",
            "url": "...",
            "device_type": "Desktop|Mobile|Tablet|Tv",
            "operating_system": "Android|iOS|...",
            "language": "en",
            "questions": [...],
            "attributes": [{"name": "...", "value": "..."}]
        }
        """
        # Extract basic fields (matching Survicate API docs)
        response_uuid = api_response.get('uuid', '').strip()
        respondent_uuid = api_response.get('respondent_uuid', '').strip()
        
        # Parse date/time (collected_at in Survicate API)
        collected_at = api_response.get('collected_at', '')
        if collected_at:
            # Convert ISO 8601 with microseconds to our format: 'YYYY-MM-DD HH:MM:SS'
            try:
                # Handle microseconds format: '2023-01-01T00:00:00.000000Z'
                dt_str = collected_at.replace('Z', '+00:00')
                dt = datetime.fromisoformat(dt_str)
                date_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                logger.warning(f"Failed to parse collected_at '{collected_at}': {e}")
                date_time = collected_at
        else:
            date_time = ''
        
        if not response_uuid or not date_time:
            logger.warning(f"Missing required fields: uuid={bool(response_uuid)}, collected_at={bool(collected_at)}")
            return None
        
        # Extract respondent attributes (array of {name, value} objects in Survicate API)
        attributes_array = api_response.get('attributes', []) or []
        attributes_dict = {}
        for attr in attributes_array:
            if isinstance(attr, dict):
                name = attr.get('name', '').strip()
                value = attr.get('value', '').strip()
                if name:
                    attributes_dict[name] = value
        
        email = attributes_dict.get('email') or None
        first_name = attributes_dict.get('first_name') or None
        last_name = attributes_dict.get('last_name') or None
        user_id = attributes_dict.get('user_id') or attributes_dict.get('sso_id') or attributes_dict.get('braze_id') or None
        
        # Extract metadata (matching Survicate API structure)
        metadata = {
            'device': api_response.get('device_type') or None,
            'platform': api_response.get('operating_system') or None,
            'page': api_response.get('url') or None,
            'braze_id': attributes_dict.get('braze_id'),
            'sso_id': attributes_dict.get('sso_id'),
        }
        
        # Extract answers from answers array (Survicate API v2 format)
        answers = {}
        answers_array = api_response.get('answers', []) or []
        questions_array = api_response.get('questions', []) or []
        
        # Handle both formats: 'answers' array (v2 API) or 'questions' array (v1 API)
        if answers_array:
            # Survicate API v2 format: answers array with question_id, question_type, and answer
            logger.debug(f"Response {response_uuid} has 'answers' array with {len(answers_array)} items")
            
            for answer_item in answers_array:
                if not isinstance(answer_item, dict):
                    continue
                
                question_id = answer_item.get('question_id')
                if question_id is None:
                    logger.debug(f"Answer item missing question_id, skipping: {list(answer_item.keys())}")
                    continue
                
                question_type = answer_item.get('question_type', '')
                answer_data = answer_item.get('answer')
                
                # Generate question key (Q#1, Q#2, etc.) to match manual export format
                # Note: question_id is numeric (e.g., 2780078), but we need sequential Q#1, Q#2
                # For now, use the question_id directly - we'll need a mapping later
                question_key = f"Q#{question_id}"
                
                # Extract answer based on question type
                answer_value = None
                comment_value = None
                
                if question_type == 'text':
                    # Text questions: answer is a string
                    if isinstance(answer_data, str):
                        answer_value = answer_data
                    elif answer_data is not None:
                        answer_value = str(answer_data)
                elif question_type in ('single', 'dropdown_list'):
                    # Single choice/dropdown: answer is an object with {id, content, comment}
                    if isinstance(answer_data, dict):
                        answer_value = answer_data.get('content', '')
                        comment_value = answer_data.get('comment') or ''
                elif question_type == 'empty':
                    # Empty/CTA questions: skip or handle action_performed
                    if answer_item.get('action_performed'):
                        answer_value = 'Yes'  # CTA was performed
                    else:
                        continue  # Skip empty questions without action
                else:
                    # Fallback: try to extract from answer object
                    if isinstance(answer_data, dict):
                        answer_value = answer_data.get('content') or answer_data.get('answer', '')
                        comment_value = answer_data.get('comment') or ''
                    elif answer_data is not None:
                        answer_value = str(answer_data)
                
                # Store answer if we have any value
                if answer_value or comment_value:
                    answers[question_key] = {
                        'Answer': answer_value or '',
                        'Comment': comment_value or ''
                    }
        
        elif questions_array:
            # Survicate API v1 format: questions array (legacy)
            logger.debug(f"Response {response_uuid} has 'questions' array with {len(questions_array)} items")
            
            for question_obj in questions_array:
                question_id = question_obj.get('question_id')
                if question_id is None:
                    logger.warning(f"Question object missing question_id: {question_obj.keys()}")
                    continue
                
                # Generate question key (Q#1, Q#2, etc.) to match manual export format
                question_key = f"Q#{question_id}"
                
                # Extract answer based on question type
                answer_value, comment_value = self._extract_answer_from_question(question_obj)
                
                if answer_value or comment_value:
                    answers[question_key] = {
                        'Answer': answer_value,
                        'Comment': comment_value
                    }
        
        else:
            # No answers or questions found
            logger.warning(f"Response {response_uuid} has no questions/answers array. Full response keys: {list(api_response.keys())}")
        
        return SurveyResponse(
            response_uuid=response_uuid,
            respondent_uuid=respondent_uuid,
            date_time=date_time,
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_id=user_id,
            answers=answers,
            metadata=metadata
        )
    
    def _extract_answer_from_question(self, question_obj: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract answer value and comment from question object (matching Survicate API structure)
        
        Returns:
            Tuple of (answer_value, comment_value)
        """
        question_type = question_obj.get('question_type', '')
        answer_value = None
        comment_value = None
        
        # Handle different answer types according to Survicate API docs
        
        # SingleChoiceAnswer, RatingAnswer, NpsAnswer - has 'answer' object
        if 'answer' in question_obj:
            answer_obj = question_obj['answer']
            
            # Check if answer is a string (OpenQuestionAnswer)
            if isinstance(answer_obj, str):
                answer_value = answer_obj
            # Otherwise it's an object
            elif isinstance(answer_obj, dict):
                # Extract content
                if 'content' in answer_obj:
                    answer_value = str(answer_obj['content'])
                elif 'rating' in answer_obj:
                    answer_value = str(answer_obj['rating'])
                
                # Extract comment
                if 'comment' in answer_obj:
                    comment_value = str(answer_obj['comment'])
        
        # MultipleChoiceAnswer, MatrixAnswer, RankingAnswer - has 'answers' array
        if 'answers' in question_obj:
            answers_array = question_obj['answers']
            answer_parts = []
            comments = []
            
            for ans in answers_array:
                if isinstance(ans, dict):
                    # Extract content/score/rank
                    if 'content' in ans:
                        answer_parts.append(str(ans['content']))
                    elif 'score' in ans:
                        answer_parts.append(str(ans['score']))
                    elif 'rank' in ans:
                        answer_parts.append(f"Rank {ans['rank']}: {ans.get('content', '')}")
                    
                    # Extract comment
                    if 'comment' in ans and ans['comment']:
                        comments.append(str(ans['comment']))
            
            if answer_parts:
                answer_value = ', '.join(answer_parts)
            if comments:
                comment_value = ' | '.join(comments)
        
        # FormAnswer - has 'fields' array
        if 'fields' in question_obj:
            fields = question_obj['fields']
            field_parts = []
            
            for field in fields:
                if isinstance(field, dict):
                    field_type = field.get('type', '')
                    field_content = field.get('content', '')
                    if field_content:
                        field_parts.append(f"{field_type}: {field_content}")
            
            if field_parts:
                answer_value = ' | '.join(field_parts)
        
        # CtaAnswer - has 'action_performed' boolean
        if 'action_performed' in question_obj:
            answer_value = "Yes" if question_obj['action_performed'] else "No"
        
        return (answer_value, comment_value)

