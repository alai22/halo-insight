# Request ID Middleware Implementation

**Date**: November 2025  
**Status**: ✅ Complete

## Overview

Enhanced request ID middleware has been implemented to provide distributed tracing and better debugging capabilities. Every HTTP request now gets a unique identifier that is:

1. **Generated** as a UUID (or extracted from `X-Request-ID` header)
2. **Included** in all log messages automatically
3. **Returned** in response headers (`X-Request-ID`)
4. **Available** throughout the request lifecycle via Flask's `g` object

## Implementation Details

### 1. Request ID Generation (`backend/api/middleware/request_logging.py`)

**Features:**
- Generates UUID-based request IDs (first 8 chars for readability)
- Supports incoming `X-Request-ID` headers for distributed tracing
- Stores both short ID (for logs) and full UUID (for internal use)

**Code:**
```python
@app.before_request
def generate_request_id():
    incoming_id = request.headers.get('X-Request-ID')
    
    if incoming_id:
        g.request_id = incoming_id  # Use client's ID for distributed systems
    else:
        full_uuid = str(uuid.uuid4())
        g.request_id = full_uuid[:8]  # Short ID: "a3f8b2c1"
        g.request_id_full = full_uuid  # Full UUID for internal use
```

### 2. Automatic Logging Integration (`backend/utils/logging.py`)

**Features:**
- `RequestIDFilter` automatically adds `request_id` to all log records
- Works both inside and outside Flask request context
- Updated formatter includes request ID in log output

**Log Format:**
```
2025-11-21 09:10:26 - gladly_analyzer.request_logging - INFO - [req:a3f8b2c1] - [REQUEST] POST /api/conversations/ask
```

### 3. Response Headers (`backend/api/middleware/request_logging.py`)

**Features:**
- Adds `X-Request-ID` header to all HTTP responses
- Clients can use this for support requests and debugging

**Example Response Headers:**
```
HTTP/1.1 200 OK
X-Request-ID: a3f8b2c1
Content-Type: application/json
```

### 4. Error Handler Integration (`backend/api/middleware/error_handlers.py`)

**Features:**
- All error responses include request ID in:
  - Response headers (`X-Request-ID`)
  - JSON response body (`request_id` field)
  - Log messages

## Usage Examples

### For Developers

**Access request ID in routes:**
```python
from flask import g

@app.route('/api/example')
def example():
    request_id = g.request_id  # e.g., "a3f8b2c1"
    logger.info(f"Processing request {request_id}")
    return jsonify({'data': 'example', 'request_id': request_id})
```

**Logging automatically includes request ID:**
```python
from backend.utils.logging import get_logger

logger = get_logger('my_service')
logger.info("This message will automatically include request ID")
# Output: 2025-11-21 09:10:26 - gladly_analyzer.my_service - INFO - [req:a3f8b2c1] - This message will automatically include request ID
```

### For Support/Debugging

**Client receives request ID in response:**
```bash
curl -X POST http://localhost:5000/api/conversations/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'

# Response headers include:
# X-Request-ID: a3f8b2c1
```

**Search logs by request ID:**
```bash
# Find all logs for a specific request
grep "req:a3f8b2c1" /var/log/app.log

# Or with structured logging tools
jq 'select(.request_id == "a3f8b2c1")' /var/log/app.json
```

### Distributed Tracing

**Pass request ID between services:**
```python
import requests

# Client sends request ID
response = requests.post(
    'http://api.example.com/endpoint',
    headers={'X-Request-ID': 'a3f8b2c1'},
    json={'data': 'example'}
)

# Server uses the same request ID for tracing
```

## Benefits

1. **Easier Debugging**: Find all logs related to a specific request
2. **Better Support**: Users can provide request ID for troubleshooting
3. **Distributed Tracing**: Track requests across multiple services
4. **Error Correlation**: Link errors to specific requests
5. **Performance Analysis**: Track request duration and identify bottlenecks

## Log Output Examples

### Before (without request ID):
```
[REQUEST] POST /api/conversations/ask | Remote: 192.168.1.1
[RESPONSE] POST /api/conversations/ask | Status: 200 | Duration: 2.345s
```

### After (with request ID):
```
2025-11-21 09:10:26 - gladly_analyzer.request_logging - INFO - [req:a3f8b2c1] - [REQUEST] POST /api/conversations/ask | Remote: 192.168.1.1
2025-11-21 09:10:28 - gladly_analyzer.request_logging - INFO - [req:a3f8b2c1] - [RESPONSE] POST /api/conversations/ask | Status: 200 | Duration: 2.345s
```

## Testing

To verify the implementation:

```bash
# Start the app
python app.py

# Make a request
curl -X POST http://localhost:5000/api/health

# Check response headers
curl -v -X POST http://localhost:5000/api/health 2>&1 | grep X-Request-ID

# Check logs for request ID
# Look for [req:xxxx] in log output
```

## Files Modified

1. `backend/api/middleware/request_logging.py` - Enhanced with UUID generation and response headers
2. `backend/utils/logging.py` - Added RequestIDFilter for automatic log inclusion
3. `backend/api/middleware/error_handlers.py` - Added request ID to error responses

## Next Steps

Future enhancements could include:
- Integration with distributed tracing systems (Jaeger, Zipkin)
- Request ID in database queries for audit trails
- Request ID in external API calls for end-to-end tracing
- Dashboard/UI to search logs by request ID

---

**Status**: ✅ Complete and tested

