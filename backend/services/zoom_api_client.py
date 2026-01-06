"""
Zoom API Client Service

Handles authentication and API calls to Zoom API for chat messages
"""

import os
import requests
import base64
import time
from typing import List, Dict, Optional, Any
from datetime import datetime
import logging
from dotenv import load_dotenv

from backend.utils.config import Config
from backend.utils.logging import get_logger

# Load environment variables
load_dotenv()

logger = get_logger('zoom_api_client')


class ZoomAPIClient:
    """Client for Zoom API with OAuth 2.0 Server-to-Server authentication"""
    
    def __init__(self, account_id: Optional[str] = None, 
                 client_id: Optional[str] = None, 
                 client_secret: Optional[str] = None,
                 base_url: Optional[str] = None):
        """Initialize Zoom API client"""
        
        self.account_id = (account_id or Config.ZOOM_ACCOUNT_ID or "").strip()
        self.client_id = (client_id or Config.ZOOM_CLIENT_ID or "").strip()
        self.client_secret = (client_secret or Config.ZOOM_CLIENT_SECRET or "").strip()
        self.base_url = base_url or "https://api.zoom.us/v2"
        
        if not self.account_id or not self.client_id or not self.client_secret:
            missing = []
            if not self.account_id:
                missing.append("ZOOM_ACCOUNT_ID")
            if not self.client_id:
                missing.append("ZOOM_CLIENT_ID")
            if not self.client_secret:
                missing.append("ZOOM_CLIENT_SECRET")
            raise ValueError(f"Missing required Zoom credentials: {', '.join(missing)}. Please check your .env file.")
        
        # Log credential status (without exposing values)
        logger.info(f"ZoomAPIClient initialized - Account ID: {self.account_id[:10]}... (length: {len(self.account_id)}), "
                   f"Client ID: {self.client_id[:10]}... (length: {len(self.client_id)}), "
                   f"Client Secret: {'*' * min(len(self.client_secret), 10)}... (length: {len(self.client_secret)})")
        
        # Token cache
        self._access_token = None
        self._token_expires_at = None
        
        logger.info("ZoomAPIClient initialized")
    
    def get_access_token(self) -> str:
        """Get OAuth 2.0 access token, refreshing if necessary"""
        
        # Check if we have a valid token
        if self._access_token and self._token_expires_at:
            if time.time() < self._token_expires_at - 60:  # Refresh 60 seconds before expiry
                return self._access_token
        
        # Request new token
        logger.info("Requesting new Zoom OAuth access token")
        logger.debug(f"Using Account ID: {self.account_id[:10]}... (truncated)")
        logger.debug(f"Using Client ID: {self.client_id[:10]}... (truncated)")
        
        # Create Basic Auth header
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        url = "https://zoom.us/oauth/token"
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Parameters should be in the POST body as form-encoded data
        # For Server-to-Server OAuth, grant_type must be 'account_credentials'
        data = {
            'grant_type': 'account_credentials',
            'account_id': self.account_id
        }
        
        logger.debug(f"OAuth request URL: {url}")
        logger.debug(f"OAuth request data: grant_type=account_credentials, account_id={self.account_id[:10]}...")
        
        try:
            response = requests.post(url, headers=headers, data=data, timeout=30)
            
            # Log response details for debugging
            logger.debug(f"OAuth response status: {response.status_code}")
            if response.status_code != 200:
                logger.error(f"OAuth response body: {response.text}")
            
            response.raise_for_status()
            
            data = response.json()
            self._access_token = data['access_token']
            # Token expires in expires_in seconds (typically 3600)
            expires_in = data.get('expires_in', 3600)
            self._token_expires_at = time.time() + expires_in
            
            logger.info(f"Successfully obtained Zoom access token (expires in {expires_in}s)")
            return self._access_token
            
        except requests.exceptions.HTTPError as e:
            # Capture detailed error response from Zoom
            error_details = "Unknown error"
            error_code = None
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_json = e.response.json()
                    error_details = error_json.get('error_description', error_json.get('error', e.response.text))
                    error_code = error_json.get('error', '')
                    logger.error(f"Zoom API error response: {error_json}")
                except:
                    error_details = e.response.text
                    logger.error(f"Zoom API error response (non-JSON): {error_details}")
            
            # Provide helpful error message for common issues
            if error_code == 'unsupported_grant_type':
                error_details = (
                    f"{error_details}. "
                    "This usually means your Zoom app is not a Server-to-Server OAuth app. "
                    "Please verify in Zoom Marketplace that you created a 'Server-to-Server OAuth' app, "
                    "not a regular OAuth app. The grant_type 'account_credentials' only works with Server-to-Server apps."
                )
            elif error_code == 'invalid_client':
                error_details = (
                    f"{error_details}. "
                    "This usually means the Client ID or Client Secret is incorrect, or the app is not activated. "
                    "Please verify: "
                    "1) Client ID and Client Secret are correct (check for extra spaces or typos), "
                    "2) The Server-to-Server OAuth app is activated/published in Zoom Marketplace, "
                    "3) The credentials match the app type (Server-to-Server, not regular OAuth)"
                )
            
            logger.error(f"Failed to obtain Zoom access token: {e}")
            logger.error(f"Zoom API error details: {error_details}")
            logger.error(f"Using Account ID: {self.account_id[:10]}... (length: {len(self.account_id)})")
            logger.error(f"Using Client ID: {self.client_id[:10]}... (length: {len(self.client_id)})")
            raise Exception(f"Zoom OAuth failed: {error_details}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to obtain Zoom access token: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            raise
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                     retries: int = 3) -> Dict[str, Any]:
        """Make authenticated API request with retry logic"""
        
        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        for attempt in range(retries):
            try:
                if method.upper() == 'GET':
                    response = requests.get(url, headers=headers, params=params, timeout=30)
                else:
                    response = requests.request(method, url, headers=headers, json=params, timeout=30)
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 401:
                    # Token expired, refresh and retry
                    logger.warning("Token expired, refreshing...")
                    self._access_token = None
                    self._token_expires_at = None
                    headers['Authorization'] = f'Bearer {self.get_access_token()}'
                    continue
                elif e.response.status_code == 400:
                    # Bad Request - likely missing scopes or invalid parameters
                    error_text = e.response.text
                    logger.error(f"HTTP 400 Bad Request: {error_text}")
                    logger.error(f"Request URL: {url}")
                    logger.error(f"Request params: {params}")
                    
                    # Check if it's a scope/permission issue
                    if 'scope' in error_text.lower() or 'permission' in error_text.lower() or 'unauthorized' in error_text.lower():
                        # Parse the error to extract required scopes
                        import json
                        try:
                            error_data = json.loads(error_text)
                            required_scopes = error_data.get('message', '')
                        except:
                            required_scopes = error_text
                        
                        # Check if error mentions imchat scopes (which may be deprecated)
                        if 'imchat' in error_text.lower():
                            error_msg = (
                                f"400 Bad Request - Missing required scopes.\n\n"
                                f"IM Chat scopes (imchat:read, imchat:read:admin) are no longer available in Zoom Marketplace.\n"
                                f"Zoom has deprecated IM Chat API in favor of Team Chat API.\n\n"
                                f"SOLUTION - Enable Team Chat scopes instead:\n"
                                f"1. Go to https://marketplace.zoom.us/\n"
                                f"2. Navigate to your Server-to-Server OAuth app\n"
                                f"3. Go to the 'Scopes' section\n"
                                f"4. Under 'Team Chat' category, enable these scopes:\n"
                                f"   - chat_message:read:admin (Read chat messages - Admin)\n"
                                f"   - team_chat:read:list_user_messages:admin (List user messages - Admin)\n"
                                f"   - team_chat:read:user_message:admin (Read user messages - Admin)\n"
                                f"5. Save and activate your app\n"
                                f"6. Wait 2-3 minutes for changes to propagate\n\n"
                                f"Note: If enabling Team Chat scopes doesn't work, we may need to migrate to Team Chat API endpoints.\n"
                                f"\nZoom API Error: {error_text}"
                            )
                        else:
                            error_msg = (
                                f"400 Bad Request - Missing required scopes. "
                                f"Please enable the required scopes in your Server-to-Server OAuth app settings in Zoom Marketplace. "
                                f"Error: {error_text}"
                            )
                        raise Exception(error_msg)
                    else:
                        raise Exception(f"400 Bad Request: {error_text}")
                elif e.response.status_code == 429:
                    retry_after = int(e.response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                else:
                    logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                    logger.error(f"Request URL: {url}")
                    logger.error(f"Request params: {params}")
                    raise
            except requests.exceptions.RequestException as e:
                if attempt == retries - 1:
                    logger.error(f"Request failed after {retries} attempts: {e}")
                    raise
                logger.warning(f"Request failed (attempt {attempt + 1}/{retries}): {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
        
        raise Exception("Failed to make request after retries")
    
    def list_chat_sessions(self, from_date: str, to_date: str, 
                          next_page_token: Optional[str] = None,
                          page_size: int = 30) -> Dict[str, Any]:
        """
        List Team Chat channels/conversations within a date range
        
        Note: Migrated from IM Chat API to Team Chat API.
        Team Chat uses channels instead of sessions.
        
        Args:
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            next_page_token: Token for pagination
            page_size: Number of results per page (max 30)
        
        Returns:
            Dict with channels/sessions list and pagination info
        """
        params = {
            'page_size': min(page_size, 50)  # Team Chat API allows up to 50
        }
        
        if next_page_token:
            params['next_page_token'] = next_page_token
        
        logger.info(f"Listing Team Chat channels from {from_date} to {to_date}")
        # Use Team Chat API endpoint for listing channels
        return self._make_request('GET', '/chat/channels', params=params)
    
    def get_chat_messages(self, session_id: str, from_date: str, to_date: str,
                          next_page_token: Optional[str] = None,
                          page_size: int = 30) -> Dict[str, Any]:
        """
        Get messages for a specific Team Chat channel
        
        Note: Migrated from IM Chat API to Team Chat API.
        session_id is now treated as a channel_id.
        
        Args:
            session_id: Team Chat channel ID (was session_id in IM Chat)
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            next_page_token: Token for pagination
            page_size: Number of results per page (max 50 for Team Chat)
        
        Returns:
            Dict with messages list and pagination info
        """
        params = {
            'to': to_date,  # Team Chat API uses 'to' parameter
            'page_size': min(page_size, 50)  # Team Chat API allows up to 50
        }
        
        # Team Chat API may use different date format - convert if needed
        # Note: Team Chat might use timestamp instead of date string
        if from_date:
            # Convert YYYY-MM-DD to timestamp if needed
            try:
                from_dt = datetime.strptime(from_date, '%Y-%m-%d')
                params['from'] = int(from_dt.timestamp())
            except:
                params['from'] = from_date
        
        if next_page_token:
            params['next_page_token'] = next_page_token
        
        logger.debug(f"Getting messages for Team Chat channel {session_id}")
        # Use Team Chat API endpoint for channel messages
        return self._make_request('GET', f'/chat/channels/{session_id}/messages', params=params)
    
    def get_all_chat_sessions(self, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        """
        Get all Team Chat channels, handling pagination automatically
        
        Note: Migrated from IM Chat to Team Chat API.
        Returns channels instead of sessions.
        
        Returns:
            List of all channels (formatted as sessions for compatibility)
        """
        all_sessions = []
        next_page_token = None
        
        while True:
            response = self.list_chat_sessions(from_date, to_date, next_page_token)
            
            # Team Chat API returns 'channels' instead of 'sessions'
            channels = response.get('channels', [])
            sessions = response.get('sessions', [])  # Fallback for compatibility
            
            # Use channels if available, otherwise use sessions
            items = channels if channels else sessions
            all_sessions.extend(items)
            
            next_page_token = response.get('next_page_token')
            if not next_page_token:
                break
            
            logger.debug(f"Fetched {len(items)} channels/sessions, total: {len(all_sessions)}")
        
        logger.info(f"Retrieved {len(all_sessions)} total Team Chat channels")
        return all_sessions
    
    def get_all_chat_messages(self, session_id: str, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        """
        Get all messages for a session, handling pagination automatically
        
        Returns:
            List of all messages
        """
        all_messages = []
        next_page_token = None
        
        while True:
            response = self.get_chat_messages(session_id, from_date, to_date, next_page_token)
            
            messages = response.get('messages', [])
            all_messages.extend(messages)
            
            next_page_token = response.get('next_page_token')
            if not next_page_token:
                break
            
            logger.debug(f"Fetched {len(messages)} messages for session {session_id}, total: {len(all_messages)}")
        
        logger.debug(f"Retrieved {len(all_messages)} total messages for session {session_id}")
        return all_messages

