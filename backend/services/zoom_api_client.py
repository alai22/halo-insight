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
        
        self.account_id = account_id or Config.ZOOM_ACCOUNT_ID
        self.client_id = client_id or Config.ZOOM_CLIENT_ID
        self.client_secret = client_secret or Config.ZOOM_CLIENT_SECRET
        self.base_url = base_url or "https://api.zoom.us/v2"
        
        if not self.account_id or not self.client_id or not self.client_secret:
            raise ValueError("ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, and ZOOM_CLIENT_SECRET must be set")
        
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
        
        # Create Basic Auth header
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        url = "https://zoom.us/oauth/token"
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Parameters should be in the POST body, not query string
        data = {
            'grant_type': 'account_credentials',
            'account_id': self.account_id
        }
        
        try:
            response = requests.post(url, headers=headers, data=data, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            self._access_token = data['access_token']
            # Token expires in expires_in seconds (typically 3600)
            expires_in = data.get('expires_in', 3600)
            self._token_expires_at = time.time() + expires_in
            
            logger.info(f"Successfully obtained Zoom access token (expires in {expires_in}s)")
            return self._access_token
            
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
                elif e.response.status_code == 429:
                    retry_after = int(e.response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                else:
                    logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
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
        List IM chat sessions within a date range
        
        Args:
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            next_page_token: Token for pagination
            page_size: Number of results per page (max 30)
        
        Returns:
            Dict with sessions list and pagination info
        """
        params = {
            'from': from_date,
            'to': to_date,
            'page_size': min(page_size, 30)  # Zoom API max is 30
        }
        
        if next_page_token:
            params['next_page_token'] = next_page_token
        
        logger.info(f"Listing chat sessions from {from_date} to {to_date}")
        return self._make_request('GET', '/im/chat/sessions', params=params)
    
    def get_chat_messages(self, session_id: str, from_date: str, to_date: str,
                          next_page_token: Optional[str] = None,
                          page_size: int = 30) -> Dict[str, Any]:
        """
        Get messages for a specific chat session
        
        Args:
            session_id: Chat session ID
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            next_page_token: Token for pagination
            page_size: Number of results per page (max 30)
        
        Returns:
            Dict with messages list and pagination info
        """
        params = {
            'from': from_date,
            'to': to_date,
            'page_size': min(page_size, 30)  # Zoom API max is 30
        }
        
        if next_page_token:
            params['next_page_token'] = next_page_token
        
        logger.debug(f"Getting messages for session {session_id}")
        return self._make_request('GET', f'/im/chat/sessions/{session_id}', params=params)
    
    def get_all_chat_sessions(self, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        """
        Get all chat sessions in date range, handling pagination automatically
        
        Returns:
            List of all chat sessions
        """
        all_sessions = []
        next_page_token = None
        
        while True:
            response = self.list_chat_sessions(from_date, to_date, next_page_token)
            
            sessions = response.get('sessions', [])
            all_sessions.extend(sessions)
            
            next_page_token = response.get('next_page_token')
            if not next_page_token:
                break
            
            logger.debug(f"Fetched {len(sessions)} sessions, total: {len(all_sessions)}")
        
        logger.info(f"Retrieved {len(all_sessions)} total chat sessions")
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

