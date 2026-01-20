"""
Survicate API Client Service

Handles authentication and API calls to Survicate Data Export API
"""

import requests
from typing import List, Dict, Optional, Any
from datetime import datetime
from ..utils.config import Config
from ..utils.logging import get_logger

logger = get_logger('survicate_api_client')


class SurvicateAPIClient:
    """Client for Survicate Data Export API"""
    
    def __init__(self, api_key: Optional[str] = None, workspace_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize Survicate API client"""
        import os
        
        # Log what we're getting from environment vs config
        api_key_env = os.getenv('SURVICATE_API_KEY')
        workspace_key_env = os.getenv('SURVICATE_WORKSPACE_KEY')
        
        self.api_key = api_key or Config.SURVICATE_API_KEY
        self.workspace_key = workspace_key or Config.SURVICATE_WORKSPACE_KEY
        self.base_url = base_url or Config.SURVICATE_API_BASE_URL
        
        if not self.api_key:
            logger.error("SURVICATE_API_KEY not configured - checked env and Config")
            raise ValueError("SURVICATE_API_KEY not configured")
        
        # Build authorization header
        # According to Postman testing: Authorization header with value "Basic <API_KEY>"
        # Use the API key directly without base64 encoding
        auth_header = f'Basic {self.api_key}'
        
        self.headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Store auth method
        self._auth_method = 'basic'
        
        # Log initialization details (after _auth_method is set)
        logger.info(f"SurvicateAPIClient init - API key from env: {bool(api_key_env)}, from config: {bool(Config.SURVICATE_API_KEY)}, final: {bool(self.api_key)}")
        logger.info(f"SurvicateAPIClient init - Workspace key from env: {bool(workspace_key_env)}, from config: {bool(Config.SURVICATE_WORKSPACE_KEY)}, final: {bool(self.workspace_key)}")
        logger.info(f"SurvicateAPIClient init - Auth method: {self._auth_method}, Base URL: {self.base_url}")
    
    def list_surveys(self) -> List[Dict[str, Any]]:
        """List all surveys (handles pagination automatically)"""
        try:
            all_surveys = []
            url = f"{self.base_url}/surveys"
            next_url = None
            
            while True:
                if next_url:
                    if next_url.startswith('http'):
                        request_url = next_url
                    else:
                        request_url = f"{self.base_url}{next_url}"
                    params = {}
                else:
                    request_url = url
                    params = {'items_per_page': 100}  # Request max per page
                
                logger.info(f"Requesting {request_url} with auth method: {self._auth_method}")
                if not next_url:
                    logger.info(f"Authorization header: {self.headers.get('Authorization', 'NOT SET')[:20]}...")
                
                response = requests.get(request_url, headers=self.headers, params=params, timeout=30)
                
                # Log response details for debugging
                logger.info(f"Response status: {response.status_code}")
                
                # If Basic auth fails with 403, log error
                if response.status_code == 403:
                    logger.error("Basic auth failed with 403 - check API key permissions and Data Export API access")
                    try:
                        error_body = response.text[:1000]
                        logger.error(f"Survicate API 403 error response (first 1000 chars): {error_body}")
                        if '<html' in error_body.lower() or '<body' in error_body.lower():
                            logger.error("Survicate returned HTML instead of JSON - this may indicate wrong endpoint or authentication format")
                    except:
                        pass
                
                response.raise_for_status()
                data = response.json()
                
                # According to Survicate API docs, response structure is:
                # {
                #   "pagination_data": {...},
                #   "data": [...]
                # }
                if isinstance(data, dict):
                    surveys = data.get('data', [])
                    if isinstance(surveys, list):
                        all_surveys.extend(surveys)
                        logger.info(f"Fetched {len(surveys)} surveys (total: {len(all_surveys)})")
                        
                        # Check for more pages
                        pagination = data.get('pagination_data', {})
                        if pagination.get('has_more', False):
                            next_url = pagination.get('next_url')
                            if next_url:
                                logger.info(f"More surveys available, fetching next page...")
                                continue  # Fetch next page
                        break  # No more pages
                    else:
                        logger.warning(f"Expected 'data' to be a list, got {type(surveys)}")
                        break
                elif isinstance(data, list):
                    # Fallback: API might return surveys directly as a list
                    all_surveys.extend(data)
                    logger.info(f"Survicate API returned {len(data)} surveys (as list)")
                    break  # No pagination info in this format
                else:
                    logger.error(f"Unexpected response type from Survicate API: {type(data)}")
                    break
            
            logger.info(f"Successfully fetched {len(all_surveys)} total surveys")
            return all_surveys
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to list surveys: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_body = e.response.text[:500]
                    logger.error(f"API error response body: {error_body}")
                except:
                    pass
            raise
    
    def get_survey_questions(self, survey_id: str) -> Dict[int, str]:
        """
        Get all questions for a survey and return a mapping of question_id -> question_text
        Questions are returned in order, which we use to map question_id to sequential Q#1, Q#2, etc.
        
        Args:
            survey_id: Survey ID
            
        Returns:
            Dict mapping question_id (int) to question_text (str)
            Questions are in the order they appear in the survey
        """
        try:
            questions_map = {}
            url = f"{self.base_url}/surveys/{survey_id}/questions"
            next_url = None
            
            while True:
                if next_url:
                    if next_url.startswith('http'):
                        request_url = next_url
                    else:
                        request_url = f"{self.base_url}{next_url}"
                    params = {}
                else:
                    request_url = url
                    params = {'items_per_page': 100}
                
                response = requests.get(request_url, headers=self.headers, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                # Extract questions from response (maintain order)
                questions = data.get('data', [])
                for question in questions:
                    question_id = question.get('id')
                    question_text = question.get('question', '')
                    question_type = question.get('type', '')
                    
                    # Only include questions that have text (skip empty/CTA questions)
                    if question_id is not None:
                        # Use question text if available, otherwise use introduction or type
                        if question_text:
                            questions_map[question_id] = question_text
                        elif question.get('introduction'):
                            questions_map[question_id] = question.get('introduction')
                        elif question_type:
                            questions_map[question_id] = f"[{question_type}]"
                        else:
                            # Still include it so we can map it, but with a placeholder
                            questions_map[question_id] = f"[Question {question_id}]"
                
                # Check for more pages
                pagination = data.get('pagination_data', {})
                if pagination.get('has_more'):
                    next_url = pagination.get('next_url')
                else:
                    break
            
            logger.info(f"Fetched {len(questions_map)} questions for survey {survey_id}")
            if questions_map:
                # Log first few questions to verify order
                question_ids = list(questions_map.keys())
                logger.info(f"Question order (first 5): {question_ids[:5]}")
                # Log first question text, sanitizing Unicode for Windows console
                first_q_text = list(questions_map.values())[0][:100] if questions_map else 'N/A'
                # Replace problematic Unicode characters for logging
                first_q_text_safe = first_q_text.encode('ascii', 'replace').decode('ascii')
                logger.info(f"First question text: {first_q_text_safe}")
            return questions_map
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch survey questions: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_body = e.response.text[:500]
                    logger.error(f"API error response body: {error_body}")
                except:
                    pass
            raise
    
    def get_responses(
        self,
        survey_id: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
        attributes: Optional[List[str]] = None,
        filters: Optional[List[Dict[str, Any]]] = None,
        items_per_page: int = 100,
        next_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get survey responses with pagination (matches Survicate API documentation)
        
        Args:
            survey_id: Survey ID
            start: ISO 8601 timestamp with microseconds (e.g., '2023-01-01T00:00:00.000000Z')
            end: ISO 8601 timestamp with microseconds (e.g., '2023-01-01T00:00:00.000000Z')
            attributes: List of respondent attributes to include (e.g., ['email', 'first_name'])
            filters: List of filter objects (OsFilter, DeviceFilter, PlatformFilter, TranslationFilter, 
                     UrlFilter, CustomAttributeFilter, or QuestionAnswerFilter)
            items_per_page: Number of items per page (1-100, default 100)
            next_url: URL for next page (from pagination_data.next_url)
        
        Returns:
            Dict with 'data' list and 'pagination_data' dict
        """
        try:
            # If next_url is provided, use it directly (Survicate provides full URL)
            if next_url:
                # next_url might be relative or absolute
                if next_url.startswith('http'):
                    url = next_url
                else:
                    # Relative URL - prepend base URL
                    url = f"{self.base_url}{next_url}"
                params = {}
            else:
                url = f"{self.base_url}/surveys/{survey_id}/responses"
                params = {
                    'items_per_page': min(max(items_per_page, 1), 100)  # API range is 1-100
                }
            
            # Add optional parameters (only if not using next_url)
            if not next_url:
                if start:
                    params['start'] = start
                if end:
                    params['end'] = end
                if attributes:
                    # Survicate expects attributes as array parameter
                    for attr in attributes:
                        params[f'attributes[]'] = attr
                if filters:
                    # Survicate expects filters as array parameter
                    # Filters should be JSON objects, so we need to send them as JSON in the request body
                    # However, GET requests typically don't have bodies, so filters might need to be
                    # sent as query parameters. Let's try sending them as JSON-encoded query params
                    import json
                    for i, filter_obj in enumerate(filters):
                        # Survicate API might expect filters as filters[]=JSON_STRING
                        params[f'filters[{i}]'] = json.dumps(filter_obj)
            
            response = requests.get(url, headers=self.headers, params=params, timeout=60)
            
            # If Basic auth fails with 403, log error (no fallback - Basic is the correct method)
            if response.status_code == 403:
                logger.error("Basic auth failed with 403 - check API key permissions and Data Export API access")
            
            # Log response body for 403 errors
            if response.status_code == 403:
                try:
                    error_body = response.text[:1000]  # First 1000 chars
                    logger.error(f"Survicate API 403 error response (first 1000 chars): {error_body}")
                    if '<html' in error_body.lower() or '<body' in error_body.lower():
                        logger.error("Survicate returned HTML instead of JSON - this may indicate wrong endpoint or authentication format")
                except:
                    pass
            
            response.raise_for_status()
            result = response.json()
            # Ensure result has expected structure
            if 'data' not in result:
                result['data'] = []
            if 'pagination_data' not in result:
                result['pagination_data'] = {'has_more': False, 'next_url': None}
            return result
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                error_msg = "Survicate API access denied. Check SURVICATE_API_KEY and ensure it has Data Export API access. If you have a workspace key, set SURVICATE_WORKSPACE_KEY."
                logger.error(f"{error_msg} - {e}")
                raise ValueError(error_msg) from e
            elif e.response.status_code == 401:
                error_msg = "Survicate API authentication failed. Check SURVICATE_API_KEY."
                logger.error(f"{error_msg} - {e}")
                raise ValueError(error_msg) from e
            else:
                logger.error(f"Failed to get responses: {e}")
                raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get responses: {e}")
            raise
    
    def get_all_responses(
        self,
        survey_id: Optional[str] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        attributes: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all responses for a survey (handles pagination automatically)
        Uses Survicate's pagination_data.next_url for pagination
        
        Args:
            survey_id: Survey ID (defaults to Config.SURVICATE_SURVEY_ID)
            start: ISO 8601 timestamp with microseconds (e.g., '2023-01-01T00:00:00.000000Z')
            end: ISO 8601 timestamp with microseconds (e.g., '2023-01-01T00:00:00.000000Z')
            attributes: List of respondent attributes
        
        Returns:
            List of all response objects from 'data' array
        """
        survey_id = survey_id or Config.SURVICATE_SURVEY_ID
        all_responses = []
        items_per_page = 100
        next_url = None
        
        # Default attributes to include
        if attributes is None:
            attributes = ['email', 'first_name', 'last_name', 'braze_id', 'sso_id', 'user_id']
        
        logger.info(f"Fetching all responses for survey {survey_id}")
        
        while True:
            try:
                result = self.get_responses(
                    survey_id=survey_id,
                    start=start,
                    end=end,
                    attributes=attributes,
                    items_per_page=items_per_page,
                    next_url=next_url
                )
                
                # Survicate API returns responses in 'data' array
                responses = result.get('data', [])
                if not responses:
                    break
                
                all_responses.extend(responses)
                
                # Check pagination
                pagination = result.get('pagination_data', {})
                has_more = pagination.get('has_more', False)
                next_url = pagination.get('next_url')
                
                # Only log every 1000 responses or at milestones to reduce noise
                if len(all_responses) % 1000 == 0 or not has_more:
                    logger.info(f"Fetched {len(all_responses)} responses (has_more: {has_more})")
                else:
                    logger.debug(f"Fetched {len(all_responses)} responses (has_more: {has_more})")
                
                # If no more pages, break
                if not has_more or not next_url:
                    break
                
            except Exception as e:
                logger.error(f"Error fetching responses: {e}")
                raise
        
        logger.info(f"Successfully fetched {len(all_responses)} total responses")
        return all_responses
    
    def get_response(self, survey_id: str, response_id: str) -> Dict[str, Any]:
        """Get a single response by ID"""
        try:
            url = f"{self.base_url}/surveys/{survey_id}/responses/{response_id}"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get response {response_id}: {e}")
            raise
    
    def test_connection(self) -> Dict[str, Any]:
        """Test API connection and return status"""
        # Log configuration status for debugging
        api_key_set = bool(self.api_key)
        workspace_key_set = bool(self.workspace_key)
        logger.info(f"Testing Survicate API connection - API key set: {api_key_set}, Workspace key set: {workspace_key_set}, Auth method: {self._auth_method}")
        
        try:
            surveys = self.list_surveys()
            return {
                'connected': True,
                'surveys_count': len(surveys),
                'surveys': surveys[:5]  # Return first 5 for preview
            }
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if hasattr(e, 'response') else None
            error_detail = str(e)
            
            if status_code == 403:
                error_msg = 'API access denied. Check SURVICATE_API_KEY and ensure it has Data Export API access.'
                if workspace_key_set:
                    error_msg += ' SURVICATE_WORKSPACE_KEY is set - ensure it matches your workspace.'
                else:
                    error_msg += ' If you have a workspace key, set SURVICATE_WORKSPACE_KEY.'
                
                logger.error(f"Survicate API 403 error - API key set: {api_key_set}, Workspace key set: {workspace_key_set}, Error: {error_detail}")
                return {
                    'connected': False,
                    'error': error_msg,
                    'status_code': 403,
                    'api_key_set': api_key_set,
                    'workspace_key_set': workspace_key_set,
                    'auth_method': self._auth_method
                }
            elif status_code == 401:
                error_msg = 'API authentication failed. Check SURVICATE_API_KEY.'
                if workspace_key_set:
                    error_msg += ' Also verify SURVICATE_WORKSPACE_KEY is correct.'
                
                logger.error(f"Survicate API 401 error - API key set: {api_key_set}, Workspace key set: {workspace_key_set}, Error: {error_detail}")
                return {
                    'connected': False,
                    'error': error_msg,
                    'status_code': 401,
                    'api_key_set': api_key_set,
                    'workspace_key_set': workspace_key_set,
                    'auth_method': self._auth_method
                }
            else:
                logger.error(f"Survicate API error {status_code}: {error_detail}")
                return {
                    'connected': False,
                    'error': f'API error: {status_code} - {error_detail}',
                    'status_code': status_code,
                    'api_key_set': api_key_set,
                    'workspace_key_set': workspace_key_set
                }
        except ValueError as e:
            # This catches the ValueError raised when API key is not configured
            logger.error(f"Survicate API configuration error: {e}")
            return {
                'connected': False,
                'error': str(e),
                'api_key_set': api_key_set,
                'workspace_key_set': workspace_key_set
            }
        except Exception as e:
            logger.error(f"Survicate API connection test failed: {e}", exc_info=True)
            return {
                'connected': False,
                'error': str(e),
                'api_key_set': api_key_set,
                'workspace_key_set': workspace_key_set,
                'auth_method': self._auth_method
            }

