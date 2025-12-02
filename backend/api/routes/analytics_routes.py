"""
Analytics API routes
"""

from flask import Blueprint, request, jsonify, g, session
from ...utils.logging import get_logger
from datetime import datetime, timedelta
import hashlib
import secrets

logger = get_logger('analytics_routes')

# Create blueprint
analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@analytics_bp.route('/track', methods=['POST'])
def track_event():
    """Track a pageview event from frontend"""
    try:
        # Get analytics service from service container
        analytics_service = g.service_container.get_analytics_service() if hasattr(g, 'service_container') else None
        
        if not analytics_service:
            logger.warning("AnalyticsService not available")
            return jsonify({
                'success': False,
                'error': 'Analytics service not available'
            }), 503
        
        # Get data from request
        data = request.get_json() or {}
        page_path = data.get('page_path', '/')
        query_params = data.get('query_params', {})
        referrer = data.get('referrer', '')
        
        # Get session ID
        session_id = None
        try:
            if session:
                session_id = session.get('session_id')
                if not session_id:
                    # Generate a session ID if not exists
                    session_key = session.get('_permanent_session_lifetime', secrets.token_hex(16))
                    session_id = hashlib.sha256(str(session_key).encode()).hexdigest()[:16]
                    session['session_id'] = session_id
        except Exception as e:
            logger.debug(f"Could not get session ID: {e}")
            # Generate a temporary session ID
            session_id = hashlib.sha256(secrets.token_hex(16).encode()).hexdigest()[:16]
        
        # Get IP address (check X-Forwarded-For for proxies)
        ip_address = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
        if not ip_address:
            ip_address = request.remote_addr or 'Unknown'
        
        # Get user agent
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        # Get request ID if available
        request_id = g.get('request_id', None)
        
        # Create event data
        event_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'session_id': session_id,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'page_path': page_path,
            'referrer': referrer,
            'query_params': query_params,
            'request_id': request_id,
            'method': 'PAGEVIEW'
        }
        
        # Track the event
        success = analytics_service.track_event(event_data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Event tracked'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to track event'
            }), 500
            
    except Exception as e:
        logger.error(f"Error tracking analytics event: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred while tracking event'
        }), 500


@analytics_bp.route('/status', methods=['GET'])
def get_analytics_status():
    """Get analytics service status and buffer information"""
    try:
        # Get analytics service from service container
        analytics_service = g.service_container.get_analytics_service() if hasattr(g, 'service_container') else None
        
        if not analytics_service:
            return jsonify({
                'success': False,
                'error': 'Analytics service not available'
            }), 503
        
        status = analytics_service.get_buffer_status()
        buffered_count = len(analytics_service.get_buffered_events())
        
        return jsonify({
            'success': True,
            'status': {
                **status,
                'buffered_events': buffered_count,
                's3_configured': analytics_service.s3_client is not None and analytics_service.bucket_name is not None
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting analytics status: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred while getting analytics status'
        }), 500


@analytics_bp.route('/flush', methods=['POST'])
def flush_analytics():
    """Manually flush analytics buffer to S3"""
    try:
        # Get analytics service from service container
        analytics_service = g.service_container.get_analytics_service() if hasattr(g, 'service_container') else None
        
        if not analytics_service:
            return jsonify({
                'success': False,
                'error': 'Analytics service not available'
            }), 503
        
        # Get buffer status before flush
        status_before = analytics_service.get_buffer_status()
        buffered_before = status_before['buffer_size']
        
        # Flush buffer
        analytics_service.flush()
        
        # Get status after flush
        status_after = analytics_service.get_buffer_status()
        
        return jsonify({
            'success': True,
            'message': f'Flushed {buffered_before} events to S3',
            'events_flushed': buffered_before,
            'buffer_size_after': status_after['buffer_size']
        }), 200
        
    except Exception as e:
        logger.error(f"Error flushing analytics buffer: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred while flushing analytics buffer'
        }), 500


@analytics_bp.route('/query', methods=['GET'])
def query_analytics():
    """Query analytics data from S3 (includes buffered events)"""
    try:
        # Get analytics service from service container
        analytics_service = g.service_container.get_analytics_service() if hasattr(g, 'service_container') else None
        
        if not analytics_service:
            logger.warning("AnalyticsService not available")
            return jsonify({
                'success': False,
                'error': 'Analytics service not available'
            }), 503
        
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page_path = request.args.get('page_path')  # Optional filter
        include_buffer = request.args.get('include_buffer', 'true').lower() == 'true'  # Default to true
        
        # Default to last 30 days if not specified
        if not end_date:
            end_date = datetime.utcnow().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # Validate dates
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }), 400
        
        # Query events (includes buffered events by default)
        events = analytics_service.query_events(start_date, end_date, page_path, include_buffer=include_buffer)
        
        # Get buffer status for info
        buffer_status = analytics_service.get_buffer_status()
        
        # Aggregate data
        total_pageviews = len(events)
        unique_visitors = len(set(e.get('session_id') for e in events if e.get('session_id')))
        unique_ips = len(set(e.get('ip_address') for e in events if e.get('ip_address')))
        
        # Pageviews over time (by date)
        pageviews_by_date = {}
        for event in events:
            timestamp_str = event.get('timestamp', '')
            try:
                if timestamp_str.endswith('Z'):
                    dt = datetime.fromisoformat(timestamp_str[:-1])
                else:
                    dt = datetime.fromisoformat(timestamp_str.replace('Z', ''))
                date_key = dt.strftime('%Y-%m-%d')
                pageviews_by_date[date_key] = pageviews_by_date.get(date_key, 0) + 1
            except Exception:
                continue
        
        # Top pages
        page_counts = {}
        for event in events:
            page_path = event.get('page_path', 'Unknown')
            page_counts[page_path] = page_counts.get(page_path, 0) + 1
        
        top_pages = sorted(page_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Device breakdown
        device_counts = {}
        for event in events:
            device = event.get('device', 'Unknown')
            device_counts[device] = device_counts.get(device, 0) + 1
        
        # Browser breakdown
        browser_counts = {}
        for event in events:
            browser = event.get('browser', 'Unknown')
            browser_counts[browser] = browser_counts.get(browser, 0) + 1
        
        # OS breakdown
        os_counts = {}
        for event in events:
            os_name = event.get('os', 'Unknown')
            os_counts[os_name] = os_counts.get(os_name, 0) + 1
        
        # Unique visitors over time
        unique_visitors_by_date = {}
        visitors_by_date = {}
        for event in events:
            timestamp_str = event.get('timestamp', '')
            session_id = event.get('session_id')
            if not session_id:
                continue
            try:
                if timestamp_str.endswith('Z'):
                    dt = datetime.fromisoformat(timestamp_str[:-1])
                else:
                    dt = datetime.fromisoformat(timestamp_str.replace('Z', ''))
                date_key = dt.strftime('%Y-%m-%d')
                if date_key not in visitors_by_date:
                    visitors_by_date[date_key] = set()
                visitors_by_date[date_key].add(session_id)
            except Exception:
                continue
        
        for date_key, visitors_set in visitors_by_date.items():
            unique_visitors_by_date[date_key] = len(visitors_set)
        
        # IP addresses (with privacy - hash last octet for display)
        ip_list = []
        ip_seen = set()
        for event in events:
            ip = event.get('ip_address', '')
            if ip and ip not in ip_seen and ip != 'Unknown':
                ip_seen.add(ip)
                # Hash last octet for privacy
                if '.' in ip:
                    parts = ip.split('.')
                    if len(parts) == 4:
                        parts[-1] = 'xxx'
                        masked_ip = '.'.join(parts)
                    else:
                        masked_ip = ip
                else:
                    masked_ip = ip
                ip_list.append({
                    'ip': masked_ip,
                    'full_ip': ip  # Keep full IP for backend analysis
                })
        
        # Convert pageviews_by_date to sorted list for chart
        pageviews_timeseries = sorted([
            {'date': date, 'pageviews': count}
            for date, count in pageviews_by_date.items()
        ], key=lambda x: x['date'])
        
        # Convert unique_visitors_by_date to sorted list
        visitors_timeseries = sorted([
            {'date': date, 'visitors': count}
            for date, count in unique_visitors_by_date.items()
        ], key=lambda x: x['date'])
        
        return jsonify({
            'success': True,
            'data': {
                'summary': {
                    'total_pageviews': total_pageviews,
                    'unique_visitors': unique_visitors,
                    'unique_ips': unique_ips,
                    'date_range': {
                        'start': start_date,
                        'end': end_date
                    },
                    'buffer_status': {
                        'buffered_events': buffer_status['buffer_size'],
                        'will_flush_when': buffer_status['will_flush_when']
                    }
                },
                'pageviews_over_time': pageviews_timeseries,
                'visitors_over_time': visitors_timeseries,
                'top_pages': [{'page': page, 'count': count} for page, count in top_pages],
                'device_breakdown': [{'device': device, 'count': count} for device, count in device_counts.items()],
                'browser_breakdown': [{'browser': browser, 'count': count} for browser, count in browser_counts.items()],
                'os_breakdown': [{'os': os_name, 'count': count} for os_name, count in os_counts.items()],
                'ip_addresses': ip_list[:100]  # Limit to 100 for performance
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error querying analytics: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred while querying analytics'
        }), 500

