"""
Analytics Service for tracking pageviews, visitors, and sessions
Stores data in S3 using JSONL format
"""

import json
import boto3
import threading
import time
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import deque
from ..utils.config import Config
from ..utils.logging import get_logger

logger = get_logger('analytics_service')


class AnalyticsService:
    """Service for tracking and storing analytics events in S3"""
    
    def __init__(self, batch_size: int = 50, batch_interval_seconds: int = 300):
        """
        Initialize analytics service
        
        Args:
            batch_size: Number of events to buffer before writing to S3
            batch_interval_seconds: Maximum time (in seconds) to wait before writing batch
        """
        self.batch_size = batch_size
        self.batch_interval_seconds = batch_interval_seconds
        
        # Event buffer
        self.event_buffer: deque = deque()
        self.buffer_lock = threading.Lock()
        self.last_write_time = time.time()
        
        # S3 client (uses IAM role on EC2)
        self.s3_client = None
        self.bucket_name = Config.S3_BUCKET_NAME
        
        if self.bucket_name:
            try:
                self.s3_client = boto3.client('s3', region_name=Config.S3_REGION)
                logger.info(f"AnalyticsService initialized with S3 bucket: {self.bucket_name}")
            except Exception as e:
                logger.warning(f"Failed to initialize S3 client for analytics: {e}")
                self.s3_client = None
        else:
            logger.warning("S3_BUCKET_NAME not configured - analytics will not be stored")
    
    def _parse_user_agent(self, user_agent: str) -> Dict[str, str]:
        """
        Parse user agent string to extract device, browser, OS info
        
        Args:
            user_agent: User agent string
            
        Returns:
            Dict with device, browser, browser_version, os
        """
        if not user_agent:
            return {
                'device': 'Unknown',
                'browser': 'Unknown',
                'browser_version': 'Unknown',
                'os': 'Unknown'
            }
        
        user_agent_lower = user_agent.lower()
        
        # Device detection
        device = 'Desktop'
        if 'mobile' in user_agent_lower or 'android' in user_agent_lower:
            device = 'Mobile'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            device = 'Tablet'
        
        # Browser detection
        browser = 'Unknown'
        browser_version = 'Unknown'
        
        if 'chrome' in user_agent_lower and 'edg' not in user_agent_lower:
            browser = 'Chrome'
            # Try to extract version
            match = re.search(r'chrome/(\d+)', user_agent_lower)
            if match:
                browser_version = match.group(1)
        elif 'firefox' in user_agent_lower:
            browser = 'Firefox'
            match = re.search(r'firefox/(\d+)', user_agent_lower)
            if match:
                browser_version = match.group(1)
        elif 'safari' in user_agent_lower and 'chrome' not in user_agent_lower:
            browser = 'Safari'
            match = re.search(r'version/(\d+)', user_agent_lower)
            if match:
                browser_version = match.group(1)
        elif 'edg' in user_agent_lower or 'edge' in user_agent_lower:
            browser = 'Edge'
            match = re.search(r'edg[ea]?/(\d+)', user_agent_lower)
            if match:
                browser_version = match.group(1)
        
        # OS detection
        os_name = 'Unknown'
        if 'windows' in user_agent_lower:
            os_name = 'Windows'
        elif 'mac' in user_agent_lower or 'darwin' in user_agent_lower:
            os_name = 'macOS'
        elif 'linux' in user_agent_lower:
            os_name = 'Linux'
        elif 'android' in user_agent_lower:
            os_name = 'Android'
        elif 'ios' in user_agent_lower or 'iphone' in user_agent_lower or 'ipad' in user_agent_lower:
            os_name = 'iOS'
        
        return {
            'device': device,
            'browser': browser,
            'browser_version': browser_version,
            'os': os_name
        }
    
    def track_event(self, event_data: Dict[str, Any]) -> bool:
        """
        Track an analytics event (buffers and writes to S3 in batches)
        
        Args:
            event_data: Event data dictionary with:
                - timestamp: ISO format timestamp
                - session_id: Session identifier
                - ip_address: IP address
                - user_agent: User agent string
                - page_path: Page/endpoint path
                - referrer: Referrer URL (optional)
                - query_params: Query parameters dict (optional)
                - request_id: Request ID (optional)
                - method: HTTP method (optional)
        
        Returns:
            True if event was queued successfully
        """
        try:
            # Parse user agent if not already parsed
            if 'user_agent' in event_data and 'device' not in event_data:
                parsed_ua = self._parse_user_agent(event_data.get('user_agent', ''))
                event_data.update(parsed_ua)
            
            # Ensure timestamp is present
            if 'timestamp' not in event_data:
                event_data['timestamp'] = datetime.utcnow().isoformat() + 'Z'
            
            # Add to buffer
            with self.buffer_lock:
                self.event_buffer.append(event_data)
                buffer_size = len(self.event_buffer)
            
            # Check if we should flush
            should_flush = False
            time_since_write = time.time() - self.last_write_time
            
            if buffer_size >= self.batch_size:
                should_flush = True
                logger.debug(f"Buffer reached batch size ({buffer_size}), flushing to S3")
            elif time_since_write >= self.batch_interval_seconds:
                should_flush = True
                logger.debug(f"Batch interval reached ({time_since_write}s), flushing to S3")
            
            if should_flush:
                self._flush_buffer()
            
            return True
            
        except Exception as e:
            logger.error(f"Error tracking analytics event: {e}", exc_info=True)
            return False
    
    def _flush_buffer(self):
        """Flush event buffer to S3"""
        if not self.s3_client or not self.bucket_name:
            logger.warning("S3 not configured, cannot flush analytics buffer")
            with self.buffer_lock:
                self.event_buffer.clear()
            return
        
        events_to_write = []
        with self.buffer_lock:
            if not self.event_buffer:
                return
            
            # Move events from buffer to write list
            while self.event_buffer:
                events_to_write.append(self.event_buffer.popleft())
            
            self.last_write_time = time.time()
        
        if not events_to_write:
            return
        
        try:
            # Group events by date for S3 path organization
            events_by_date: Dict[str, List[Dict[str, Any]]] = {}
            
            for event in events_to_write:
                # Parse timestamp to get date
                timestamp_str = event.get('timestamp', '')
                try:
                    if timestamp_str.endswith('Z'):
                        dt = datetime.fromisoformat(timestamp_str[:-1])
                    else:
                        dt = datetime.fromisoformat(timestamp_str.replace('Z', ''))
                    
                    date_key = dt.strftime('%Y/%m/%d')
                    if date_key not in events_by_date:
                        events_by_date[date_key] = []
                    events_by_date[date_key].append(event)
                except Exception as e:
                    logger.warning(f"Failed to parse timestamp {timestamp_str}: {e}")
                    # Use current date as fallback
                    date_key = datetime.utcnow().strftime('%Y/%m/%d')
                    if date_key not in events_by_date:
                        events_by_date[date_key] = []
                    events_by_date[date_key].append(event)
            
            # Write events grouped by date
            for date_key, date_events in events_by_date.items():
                self._write_events_to_s3(date_events, date_key)
            
            logger.info(f"Flushed {len(events_to_write)} analytics events to S3")
            
        except Exception as e:
            logger.error(f"Error flushing analytics buffer to S3: {e}", exc_info=True)
            # Re-add events to buffer on error (to avoid data loss)
            with self.buffer_lock:
                self.event_buffer.extendleft(reversed(events_to_write))
    
    def _write_events_to_s3(self, events: List[Dict[str, Any]], date_path: str):
        """
        Write events to S3 in JSONL format
        
        Args:
            events: List of event dictionaries
            date_path: Date path in format YYYY/MM/DD
        """
        try:
            # Create S3 key: analytics/YYYY/MM/DD/events-{timestamp}.jsonl
            timestamp = datetime.utcnow().strftime('%H%M%S')
            s3_key = f"analytics/{date_path}/events-{timestamp}.jsonl"
            
            # Convert events to JSONL format
            jsonl_lines = [json.dumps(event, ensure_ascii=False) for event in events]
            jsonl_content = '\n'.join(jsonl_lines)
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=jsonl_content.encode('utf-8'),
                ContentType='application/json'
            )
            
            logger.debug(f"Wrote {len(events)} events to s3://{self.bucket_name}/{s3_key}")
            
        except Exception as e:
            logger.error(f"Error writing events to S3: {e}", exc_info=True)
            raise
    
    def flush(self):
        """Manually flush the buffer (useful for shutdown)"""
        self._flush_buffer()
    
    def query_events(self, start_date: str, end_date: str, page_path_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Query events from S3 for a date range
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            page_path_filter: Optional page path to filter by
            
        Returns:
            List of event dictionaries
        """
        if not self.s3_client or not self.bucket_name:
            logger.warning("S3 not configured, cannot query events")
            return []
        
        try:
            # Parse dates
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Generate date range
            current_dt = start_dt
            all_events = []
            
            while current_dt <= end_dt:
                date_path = current_dt.strftime('%Y/%m/%d')
                prefix = f"analytics/{date_path}/"
                
                # List objects in this date folder
                try:
                    paginator = self.s3_client.get_paginator('list_objects_v2')
                    pages = paginator.paginate(Bucket=self.bucket_name, Prefix=prefix)
                    
                    for page in pages:
                        if 'Contents' not in page:
                            continue
                        
                        for obj in page['Contents']:
                            key = obj['Key']
                            if not key.endswith('.jsonl'):
                                continue
                            
                            # Read JSONL file
                            try:
                                response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
                                content = response['Body'].read().decode('utf-8')
                                
                                # Parse JSONL
                                for line in content.strip().split('\n'):
                                    if not line.strip():
                                        continue
                                    try:
                                        event = json.loads(line)
                                        # Apply page path filter if specified
                                        if page_path_filter:
                                            event_path = event.get('page_path', '')
                                            if page_path_filter not in event_path:
                                                continue
                                        all_events.append(event)
                                    except json.JSONDecodeError as e:
                                        logger.warning(f"Failed to parse JSON line in {key}: {e}")
                                        continue
                            except Exception as e:
                                logger.warning(f"Error reading S3 object {key}: {e}")
                                continue
                
                except Exception as e:
                    logger.warning(f"Error listing S3 objects for {prefix}: {e}")
                
                # Move to next day
                current_dt += timedelta(days=1)
            
            logger.info(f"Queried {len(all_events)} events from S3 for date range {start_date} to {end_date}")
            return all_events
            
        except Exception as e:
            logger.error(f"Error querying events from S3: {e}", exc_info=True)
            return []

