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
        
        logger.debug(f"SurvicateAPIClient init - API key from env: {bool(api_key_env)}, from config: {bool(Config.SURVICATE_API_KEY)}, final: {bool(self.api_key)}")
        logger.debug(f"SurvicateAPIClient init - Workspace key from env: {bool(workspace_key_env)}, from config: {bool(Config.SURVICATE_WORKSPACE_KEY)}, final: {bool(self.workspace_key)}")
        
        if not self.api_key:
            logger.error("SURVICATE_API_KEY not configured - checked env and Config")
            raise ValueError("SURVICATE_API_KEY not configured")
        
        # Build authorization header
        # Survicate API may use Basic auth with API key, or Bearer token
        # Try Basic auth first (API key as username, empty password or workspace key as password)
        if self.workspace_key:
            # If workspace key is provided, use it in Basic auth
            import base64
            credentials = f"{self.api_key}:{self.workspace_key}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            auth_header = f'Basic {encoded_credentials}'
        else:
            # Try Bearer token first (most common for API keys)
            # If that fails, we'll try Basic auth
            auth_header = f'Bearer {self.api_key}'
        
        self.headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json'
        }
        
        # Store original auth method for fallback
        self._auth_method = 'bearer' if not self.workspace_key else 'basic'
    
    def list_surveys(self) -> List[Dict[str, Any]]:
        """List all surveys"""
        try:
            url = f"{self.base_url}/surveys"
            response = requests.get(url, headers=self.headers, timeout=30)
            
            # If Bearer auth fails with 403, try Basic auth
            if response.status_code == 403 and self._auth_method == 'bearer' and not self.workspace_key:
                logger.info("Bearer auth failed, trying Basic auth with API key only")
                import base64
                credentials = f"{self.api_key}:"
                encoded_credentials = base64.b64encode(credentials.encode()).decode()
                self.headers['Authorization'] = f'Basic {encoded_credentials}'
                self._auth_method = 'basic'
                response = requests.get(url, headers=self.headers, timeout=30)
            
            response.raise_for_status()
            data = response.json()
            return data.get('surveys', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to list surveys: {e}")
            raise
    
    def get_responses(
        self,
        survey_id: str,
        since: Optional[str] = None,
        until: Optional[str] = None,
        attributes: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get survey responses with pagination
        
        Args:
            survey_id: Survey ID
            since: ISO 8601 date string (e.g., '2024-01-01T00:00:00Z')
            until: ISO 8601 date string (e.g., '2024-01-31T23:59:59Z')
            attributes: List of respondent attributes to include (e.g., ['email', 'first_name'])
            limit: Number of responses per page (max 100)
            offset: Pagination offset
        
        Returns:
            Dict with 'responses' list and 'total' count
        """
        try:
            url = f"{self.base_url}/surveys/{survey_id}/responses"
            params = {
                'limit': min(limit, 100),  # API max is 100
                'offset': offset
            }
            
            if since:
                params['since'] = since
            if until:
                params['until'] = until
            if attributes:
                for attr in attributes:
                    params[f'attributes[]'] = attr
            
            response = requests.get(url, headers=self.headers, params=params, timeout=60)
            
            # If Bearer auth fails with 403, try Basic auth
            if response.status_code == 403 and self._auth_method == 'bearer' and not self.workspace_key:
                logger.info("Bearer auth failed, trying Basic auth with API key only")
                import base64
                credentials = f"{self.api_key}:"
                encoded_credentials = base64.b64encode(credentials.encode()).decode()
                self.headers['Authorization'] = f'Basic {encoded_credentials}'
                self._auth_method = 'basic'
                response = requests.get(url, headers=self.headers, params=params, timeout=60)
            
            response.raise_for_status()
            return response.json()
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
        since: Optional[str] = None,
        until: Optional[str] = None,
        attributes: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all responses for a survey (handles pagination automatically)
        
        Args:
            survey_id: Survey ID (defaults to Config.SURVICATE_SURVEY_ID)
            since: ISO 8601 date string
            until: ISO 8601 date string
            attributes: List of respondent attributes
        
        Returns:
            List of all response objects
        """
        survey_id = survey_id or Config.SURVICATE_SURVEY_ID
        all_responses = []
        offset = 0
        limit = 100
        
        # Default attributes to include
        if attributes is None:
            attributes = ['email', 'first_name', 'last_name', 'braze_id', 'sso_id', 'user_id']
        
        logger.info(f"Fetching all responses for survey {survey_id}")
        
        while True:
            try:
                result = self.get_responses(
                    survey_id=survey_id,
                    since=since,
                    until=until,
                    attributes=attributes,
                    limit=limit,
                    offset=offset
                )
                
                responses = result.get('responses', [])
                if not responses:
                    break
                
                all_responses.extend(responses)
                total = result.get('total', len(responses))
                
                logger.info(f"Fetched {len(all_responses)}/{total} responses")
                
                # Check if we've fetched all responses
                if len(all_responses) >= total or len(responses) < limit:
                    break
                
                offset += limit
                
            except Exception as e:
                logger.error(f"Error fetching responses at offset {offset}: {e}")
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

