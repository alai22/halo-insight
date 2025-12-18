# IMPORTANT: Set Werkzeug max header size BEFORE importing Flask
# This must be done before Flask/Werkzeug initializes the request handler
import werkzeug.serving
werkzeug.serving.WSGIRequestHandler.max_header_size = 32768  # 32KB (default is 8KB)

from flask import Flask, send_from_directory, g
from flask_cors import CORS
import os
import secrets
from datetime import timedelta
from app import app as api_app, get_service_container
from backend.utils.config import Config

# Initialize services (they initialize themselves when imported)
print("Initializing services...")
try:
    from backend.services.claude_service import ClaudeService
    from backend.services.conversation_service import ConversationService
    print("✅ Services initialized successfully")
except Exception as e:
    print(f"⚠️ Warning: Failed to initialize services: {e}")

# Create main app
app = Flask(__name__, static_folder="build")

# Configure session secret key (required for session management, including Google OAuth state)
# IMPORTANT: In production, set FLASK_SECRET_KEY in .env for session persistence
secret_key = Config.FLASK_SECRET_KEY or os.getenv('FLASK_SECRET_KEY') or secrets.token_hex(32)
if not Config.FLASK_SECRET_KEY and not os.getenv('FLASK_SECRET_KEY'):
    print("⚠️ Warning: FLASK_SECRET_KEY not set - sessions will not persist across restarts. Set FLASK_SECRET_KEY in .env for production.")
app.secret_key = secret_key
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # Sessions last 24 hours

# Enable CORS with credentials support (required for session cookies)
CORS(app, supports_credentials=True)

# Set up service container for each request (critical for dependency injection)
@app.before_request
def before_request():
    """Initialize service container for each request"""
    try:
        g.service_container = get_service_container()
    except Exception as e:
        # Log error but don't crash - routes will handle None gracefully
        print(f"Warning: Failed to initialize service container: {str(e)}")
        g.service_container = None

# Copy only the API routes from api_app, excluding built-in Flask routes and root route
for rule in api_app.url_map.iter_rules():
    # Skip built-in Flask routes like 'static', 'index', and static asset routes
    if rule.endpoint not in ['static', 'index', 'favicon', 'robots']:
        app.add_url_rule(
            rule.rule,
            endpoint=rule.endpoint,
            view_func=api_app.view_functions[rule.endpoint],
            methods=rule.methods
        )

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"Starting Gladly Conversation Analyzer on {host}:{port}")
    print(f"Max header size: {werkzeug.serving.WSGIRequestHandler.max_header_size} bytes")
    app.run(host=host, port=port, debug=False)
