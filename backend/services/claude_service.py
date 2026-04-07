"""
Claude API service
"""

import json
import hashlib
import time
import requests
from typing import Optional, Dict, Any, Generator, List
from ..utils.config import Config
from ..utils.logging import get_logger
from ..models.response import ClaudeResponse
from ..core.interfaces import IClaudeService, ICacheService
from ..core.exceptions import ConfigurationError, ClaudeAPIError, RateLimitError, TimeoutError

logger = get_logger('claude_service')


def _parse_retry_after_seconds(response: requests.Response) -> Optional[float]:
    """Parse Retry-After header as seconds, if present and numeric."""
    raw = response.headers.get('retry-after') or response.headers.get('Retry-After')
    if not raw:
        return None
    try:
        return float(raw.strip())
    except (TypeError, ValueError):
        return None


def _backoff_seconds_for_429(attempt_index: int, response: requests.Response) -> float:
    """Combine exponential backoff with optional Retry-After (capped)."""
    base = max(0.1, float(Config.CLAUDE_RETRY_BASE_DELAY_SEC))
    cap = max(base, float(Config.CLAUDE_RETRY_MAX_DELAY_SEC))
    exp = min(cap, base * (2 ** attempt_index))
    ra = _parse_retry_after_seconds(response)
    if ra is not None:
        return min(cap, max(exp, ra))
    return exp


class ClaudeService(IClaudeService):
    """Service for interacting with Claude API"""
    
    def __init__(self, api_key: Optional[str] = None, cache_service: Optional[ICacheService] = None):
        """Initialize Claude service"""
        self.api_key = api_key or Config.ANTHROPIC_API_KEY
        if not self.api_key:
            raise ConfigurationError(
                "API key not provided. Set ANTHROPIC_API_KEY in config or environment variable",
                details={'config_key': 'ANTHROPIC_API_KEY'}
            )
        
        self.base_url = "https://api.anthropic.com/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # Cache service (optional - only used if caching is enabled)
        self.cache_service = cache_service if Config.CACHE_ENABLED and cache_service else None
        if self.cache_service:
            logger.info("ClaudeService: Caching enabled")
        else:
            logger.info("ClaudeService: Caching disabled")
    
    def _generate_cache_key(
        self,
        message: str,
        model: str,
        max_tokens: int,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """Generate a cache key for Claude API request"""
        # Create deterministic key from request parameters
        key_data: Dict[str, Any] = {
            'message': message,
            'model': model,
            'max_tokens': max_tokens,
            'system_prompt': system_prompt or '',
            'conversation_history': conversation_history or []
        }
        if temperature is not None:
            key_data['temperature'] = temperature
        key_string = json.dumps(key_data, sort_keys=True)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        return f"claude:response:{key_hash}"
    
    def send_message(self, 
                    message: str, 
                    model: str = None,
                    max_tokens: int = 1000,
                    system_prompt: Optional[str] = None,
                    conversation_history: Optional[List[Dict[str, str]]] = None,
                    temperature: Optional[float] = None) -> ClaudeResponse:
        """Send a message to Claude API with automatic model fallback and caching
        
        Args:
            message: The current user message
            model: Claude model to use
            max_tokens: Maximum tokens for response
            system_prompt: Optional system prompt
            conversation_history: Optional list of previous messages in format [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
            temperature: If set, sent to the API (e.g. 0 for near-greedy decoding). If None, API default applies.
        """
        # Resolve model through aliases and fallbacks
        requested_model = model or Config.CLAUDE_MODEL
        model = Config.resolve_model(requested_model)
        
        # Check cache first (if caching is enabled and no conversation history)
        # Note: We skip caching when conversation_history is provided to ensure fresh responses
        if self.cache_service and not conversation_history:
            cache_key = self._generate_cache_key(
                message, model, max_tokens, system_prompt, conversation_history, temperature
            )
            cached_response = self.cache_service.get(cache_key)
            if cached_response:
                logger.info(f"Cache HIT for Claude API request: {cache_key[:32]}...")
                # Reconstruct ClaudeResponse from cached dict
                return ClaudeResponse(
                    content=cached_response['content'],
                    model=cached_response['model'],
                    tokens_used=cached_response['tokens_used'],
                    streamed=cached_response.get('streamed', False)
                )
            logger.debug(f"Cache MISS for Claude API request: {cache_key[:32]}...")
        
        # Build messages array - include conversation history if provided
        messages = []
        if conversation_history:
            messages.extend(conversation_history)
        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })
        
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        if temperature is not None:
            payload["temperature"] = temperature
        
        try:
            timeout = Config.CLAUDE_API_TIMEOUT
            logger.info(f"Sending message to Claude: model={model}, max_tokens={max_tokens}, timeout={timeout}s")
            max_attempts = max(1, int(Config.CLAUDE_RETRY_MAX_ATTEMPTS))
            response: Optional[requests.Response] = None
            for attempt in range(max_attempts):
                response = requests.post(
                    f"{self.base_url}/messages",
                    headers=self.headers,
                    json=payload,
                    timeout=timeout
                )
                if response.status_code == 429:
                    if attempt + 1 >= max_attempts:
                        ra = _parse_retry_after_seconds(response)
                        logger.error(
                            "Claude API rate limit (429) after %s attempts; retry_after=%s",
                            max_attempts,
                            ra,
                        )
                        raise RateLimitError(
                            "Claude API rate limit exceeded. Please wait before making another request.",
                            details={
                                'status_code': 429,
                                'model': model,
                                'attempts': max_attempts,
                                'retry_after_seconds': ra,
                                'suggestion': 'Wait and retry, or reduce backlog overview scope.',
                            },
                        )
                    delay = _backoff_seconds_for_429(attempt, response)
                    logger.warning(
                        "Claude API 429; sleeping %.2fs before retry %s/%s",
                        delay,
                        attempt + 2,
                        max_attempts,
                    )
                    time.sleep(delay)
                    continue
                break

            assert response is not None
            response.raise_for_status()

            response_data = response.json()
            logger.info(f"Claude response received: tokens_used={response_data.get('usage', {}).get('output_tokens', 0)}")

            claude_response = ClaudeResponse.from_api_response(response_data, model)
            
            # Cache the response (if caching is enabled and no conversation history)
            # Note: We skip caching when conversation_history is provided to ensure fresh responses
            if self.cache_service and not conversation_history:
                cache_key = self._generate_cache_key(
                    message, model, max_tokens, system_prompt, conversation_history, temperature
                )
                # Store as dict for caching (dataclass is not directly JSON-serializable)
                cache_value = {
                    'content': claude_response.content,
                    'model': claude_response.model,
                    'tokens_used': claude_response.tokens_used,
                    'streamed': claude_response.streamed
                }
                self.cache_service.set(cache_key, cache_value, ttl=Config.CACHE_CLAUDE_TTL)
                logger.debug(f"Cached Claude API response: {cache_key[:32]}... (ttl={Config.CACHE_CLAUDE_TTL}s)")
            
            return claude_response
        
        except requests.exceptions.Timeout as e:
            logger.error(f"Claude API request timed out after {Config.CLAUDE_API_TIMEOUT} seconds. The request may be too complex or the API is slow.")
            raise TimeoutError(
                f"Request to Claude API timed out after {Config.CLAUDE_API_TIMEOUT} seconds. The query may be too complex or there may be network issues. Please try again or simplify your query.",
                details={
                    'timeout_seconds': Config.CLAUDE_API_TIMEOUT,
                    'model': model,
                    'suggestion': 'Try simplifying your query or increasing CLAUDE_API_TIMEOUT if needed.'
                }
            ) from e
        
        except requests.exceptions.RequestException as e:
            # Check for rate limit (429)
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 429:
                    logger.error(f"Claude API rate limit exceeded (429)")
                    raise RateLimitError(
                        "Claude API rate limit exceeded. Please wait before making another request.",
                        details={
                            'status_code': 429,
                            'model': model,
                            'suggestion': 'Wait a few moments before retrying your request.'
                        }
                    ) from e
                
                # If model not found error, try fallback models
                error_data = e.response.json() if e.response.headers.get('content-type', '').startswith('application/json') else {}
                error_type = error_data.get('error', {}).get('type', '')
                
                if error_type == 'not_found_error':
                    # Try fallback models from VERIFIED_MODELS (skip the one we just tried)
                    models_to_try = [m for m in Config.VERIFIED_MODELS if m != model]
                    
                    for fallback_model in models_to_try:
                        try:
                            logger.warning(f"Model '{model}' not found, trying fallback '{fallback_model}'")
                            payload['model'] = fallback_model
                            response = requests.post(
                                f"{self.base_url}/messages",
                                headers=self.headers,
                                json=payload,
                                timeout=Config.CLAUDE_API_TIMEOUT
                            )
                            response.raise_for_status()
                            response_data = response.json()
                            logger.info(f"Claude response received with fallback model '{fallback_model}': tokens_used={response_data.get('usage', {}).get('output_tokens', 0)}")
                            
                            claude_response = ClaudeResponse.from_api_response(response_data, fallback_model)
                            
                            # Cache the response (if caching is enabled and no conversation history)
                            if self.cache_service and not conversation_history:
                                cache_key = self._generate_cache_key(
                                    message, fallback_model, max_tokens, system_prompt, conversation_history, temperature
                                )
                                cache_value = {
                                    'content': claude_response.content,
                                    'model': claude_response.model,
                                    'tokens_used': claude_response.tokens_used,
                                    'streamed': claude_response.streamed
                                }
                                self.cache_service.set(cache_key, cache_value, ttl=Config.CACHE_CLAUDE_TTL)
                                logger.debug(f"Cached Claude API response (fallback): {cache_key[:32]}...")
                            
                            return claude_response
                        except requests.exceptions.RequestException as fallback_error:
                            # Try next fallback model
                            logger.warning(f"Fallback model '{fallback_model}' also failed: {str(fallback_error)}")
                            continue
                    
                    # If all fallbacks failed, raise ClaudeAPIError
                    logger.error(f"All model fallbacks failed. Original model: '{model}', tried: {models_to_try}")
                    raise ClaudeAPIError(
                        f"Model '{model}' not found and all fallback models failed",
                        details={
                            'requested_model': model,
                            'fallback_models_tried': models_to_try,
                            'error_type': error_type
                        }
                    ) from e
            
            # Generic Claude API error
            error_details = {'model': model}
            if hasattr(e, 'response') and e.response is not None:
                error_details['status_code'] = e.response.status_code
                try:
                    error_details['response_text'] = e.response.text[:500]  # Limit response text
                except:
                    pass
            
            logger.error(f"Claude API request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None and getattr(e.response, 'text', None):
                logger.error("Claude API response body (truncated): %s", (e.response.text or '')[:800])
            raise ClaudeAPIError(
                f"Claude API request failed: {str(e)}",
                details=error_details
            ) from e
    
    def stream_message(self, 
                      message: str, 
                      model: str = None,
                      max_tokens: int = 1000,
                      system_prompt: Optional[str] = None) -> Generator[Dict[str, Any], None, None]:
        """Stream a message from Claude API with automatic model fallback"""
        # Resolve model through aliases and fallbacks
        requested_model = model or Config.CLAUDE_MODEL
        model = Config.resolve_model(requested_model)
        
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "stream": True,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            timeout = Config.CLAUDE_API_TIMEOUT
            logger.info(f"Streaming message to Claude: model={model}, max_tokens={max_tokens}, timeout={timeout}s")
            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=timeout
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]  # Remove 'data: ' prefix
                        if data.strip() == '[DONE]':
                            break
                        try:
                            chunk = json.loads(data)
                            yield chunk
                        except json.JSONDecodeError:
                            continue
        
        except requests.exceptions.Timeout as e:
            logger.error(f"Claude API streaming request timed out after {Config.CLAUDE_API_TIMEOUT} seconds.")
            raise TimeoutError(
                f"Streaming request to Claude API timed out after {Config.CLAUDE_API_TIMEOUT} seconds. The query may be too complex or there may be network issues.",
                details={
                    'timeout_seconds': Config.CLAUDE_API_TIMEOUT,
                    'model': model,
                    'suggestion': 'Try simplifying your query or increasing CLAUDE_API_TIMEOUT if needed.'
                }
            ) from e
        
        except requests.exceptions.RequestException as e:
            error_details = {'model': model}
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 429:
                    raise RateLimitError(
                        "Claude API rate limit exceeded during streaming. Please wait before making another request.",
                        details={
                            'status_code': 429,
                            'model': model,
                            'suggestion': 'Wait a few moments before retrying your request.'
                        }
                    ) from e
                error_details['status_code'] = e.response.status_code
            
            logger.error(f"Claude streaming request failed: {str(e)}")
            raise ClaudeAPIError(
                f"Claude streaming request failed: {str(e)}",
                details=error_details
            ) from e
    
    def is_available(self) -> bool:
        """Check if Claude service is available, trying fallback models if needed"""
        # Resolve the configured model first
        model = Config.resolve_model()
        
        # Try configured/aliased model first
        models_to_try = [model]
        
        # Add fallback if it's different
        if Config.FALLBACK_MODEL not in models_to_try:
            models_to_try.append(Config.FALLBACK_MODEL)
        
        # Try verified models as last resort
        for verified_model in Config.VERIFIED_MODELS:
            if verified_model not in models_to_try:
                models_to_try.append(verified_model)
                break  # Only need one fallback
        
        # Use shorter timeout for health check
        health_check_timeout = min(30, Config.CLAUDE_API_TIMEOUT // 4)
        
        for test_model in models_to_try:
            try:
                response = requests.post(
                    f"{self.base_url}/messages",
                    headers=self.headers,
                    json={
                        "model": test_model,
                        "max_tokens": 10,
                        "messages": [{"role": "user", "content": "test"}]
                    },
                    timeout=health_check_timeout
                )
                if response.status_code == 200:
                    if test_model != model:
                        logger.info(f"Health check: '{model}' unavailable, using working model '{test_model}'")
                    return True
                else:
                    logger.warning(f"Model '{test_model}' health check returned status {response.status_code}")
            except requests.exceptions.Timeout:
                logger.warning(f"Model '{test_model}' health check timed out")
                continue
            except requests.exceptions.RequestException as e:
                logger.warning(f"Model '{test_model}' health check failed: {str(e)}")
                continue
            except Exception as e:
                logger.warning(f"Model '{test_model}' health check error: {str(e)}")
                continue
        
        return False
