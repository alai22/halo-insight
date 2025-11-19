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
        # According to Survicate Data Export API docs: Authorization: Basic {apiKey}
        # Use Basic auth with API key only (no password/workspace key in Basic auth)
        import base64
        # Basic auth format: base64(apiKey:)
        credentials = f"{self.api_key}:"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        auth_header = f'Basic {encoded_credentials}'
        
        self.headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json'
        }
        
        # Store auth method
        self._auth_method = 'basic'
        
        # Log initialization details (after _auth_method is set)
        logger.info(f"SurvicateAPIClient init - API key from env: {bool(api_key_env)}, from config: {bool(Config.SURVICATE_API_KEY)}, final: {bool(self.api_key)}")
        logger.info(f"SurvicateAPIClient init - Workspace key from env: {bool(workspace_key_env)}, from config: {bool(Config.SURVICATE_WORKSPACE_KEY)}, final: {bool(self.workspace_key)}")
        logger.info(f"SurvicateAPIClient init - Auth method: {self._auth_method}, Base URL: {self.base_url}")
    
    def list_surveys(self) -> List[Dict[str, Any]]:
        """List all surveys"""
        try:
            url = f"{self.base_url}/surveys"
            logger.info(f"Requesting {url} with auth method: {self._auth_method}")
            logger.info(f"Authorization header: {self.headers.get('Authorization', 'NOT SET')[:20]}...")
            response = requests.get(url, headers=self.headers, timeout=30)
            
            # Log response details for debugging
            logger.info(f"Response status: {response.status_code}")
            
            # If Basic auth fails with 403, log error (no fallback - Basic is the correct method)
            if response.status_code == 403:
                logger.error("Basic auth failed with 403 - check API key permissions and Data Export API access")
            
            # Log response body for 403 errors to see what Survicate says
            if response.status_code == 403:
                try:
                    error_body = response.text[:1000]  # First 1000 chars to see full HTML
                    logger.error(f"Survicate API 403 error response (first 1000 chars): {error_body}")
                    # Try to extract meaningful error from HTML if possible
                    if '<html' in error_body.lower() or '<body' in error_body.lower():
                        logger.error("Survicate returned HTML instead of JSON - this may indicate wrong endpoint or authentication format")
                except:
                    pass
            
            response.raise_for_status()
            data = response.json()
            return data.get('surveys', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to list surveys: {e}")
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
                
                logger.info(f"Fetched {len(all_responses)} responses (has_more: {has_more})")
                
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

