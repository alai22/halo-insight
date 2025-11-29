"""
API routes for RAG-powered analysis
"""

from flask import Blueprint, request, jsonify, g
from ...utils.logging import get_logger
from ...utils.config import Config
from ...core.exceptions import ValidationError, ServiceUnavailableError

logger = get_logger('rag_routes')

# Create blueprint
rag_bp = Blueprint('rag', __name__, url_prefix='/api/conversations')


@rag_bp.route('/ask', methods=['POST'])
def conversations_ask():
    """Ask Claude about conversation data with detailed RAG process information"""
    # Get services from container (injected via Flask's g)
    service_container = getattr(g, 'service_container', None)
    if not service_container:
        logger.error("Service container not available in request context")
        raise ServiceUnavailableError(
            "Service container not initialized",
            details={'suggestion': 'Check application initialization'}
        )
    
    claude_service = service_container.get_claude_service()
    rag_service = service_container.get_rag_service()
    
    data = request.get_json() or {}
    question = data.get('question')
    # Default to configured model (falls back to working model via fallback system if needed)
    model = data.get('model', Config.CLAUDE_MODEL)
    max_tokens = data.get('max_tokens', 2000)
    
    if not question:
        raise ValidationError(
            "Question is required",
            details={'field': 'question', 'suggestion': 'Provide a question in the request body'}
        )
    
    logger.info(f"RAG query request: question={question[:100]}, model={model}, max_tokens={max_tokens}")
    
    # Check if Claude service is initialized
    if claude_service is None or rag_service is None:
        error_msg = "Claude API service is not initialized. Please check ANTHROPIC_API_KEY configuration."
        logger.error(error_msg)
        raise ServiceUnavailableError(
            error_msg,
            details={
                'service': 'Claude API',
                'suggestion': 'ANTHROPIC_API_KEY environment variable is not set or invalid. Please configure it in your .env file or environment.'
            }
        )
    
    # Skip aggressive availability check - let the actual API call handle errors
    # The is_available() check makes an HTTP request which can fail due to network issues
    # and is not a reliable indicator. We'll let the actual API call fail gracefully if needed.
    
    result = rag_service.process_query(question, model, max_tokens)
    
    return jsonify(result)

@rag_bp.route('/refresh', methods=['POST'])
def refresh_conversations():
    """Refresh conversation data from storage"""
    # Get service from container (injected via Flask's g)
    service_container = getattr(g, 'service_container', None)
    if not service_container:
        logger.error("Service container not available in request context")
        raise ServiceUnavailableError(
            "Service container not initialized",
            details={'suggestion': 'Check application initialization'}
        )
    
    conversation_service = service_container.get_conversation_service()
    
    logger.info("Refreshing conversation data for RAG system")
    conversation_service.refresh_conversations()
    
    return jsonify({
        'success': True,
        'message': f'Conversation data refreshed: {len(conversation_service.conversations)} conversations loaded',
        'data': {
            'total_conversations': len(conversation_service.conversations),
            'is_available': conversation_service.is_available()
        }
    })