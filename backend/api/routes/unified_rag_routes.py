"""
API routes for unified RAG-powered analysis across all data sources
"""

from flask import Blueprint, request, jsonify, g
from ...utils.logging import get_logger
from ...utils.config import Config
from ...core.exceptions import ValidationError, ServiceUnavailableError

logger = get_logger('unified_rag_routes')

# Create blueprint
unified_rag_bp = Blueprint('unified_rag', __name__, url_prefix='/api/unified')


@unified_rag_bp.route('/ask', methods=['POST'])
def unified_ask():
    """Ask Claude about data across all sources (Gladly, Survicate, Zoom)"""
    service_container = getattr(g, 'service_container', None)
    if not service_container:
        logger.error("Service container not available in request context")
        raise ServiceUnavailableError(
            "Service container not initialized",
            details={'suggestion': 'Check application initialization'}
        )
    
    unified_rag_service = service_container.get_unified_rag_service()
    if not unified_rag_service:
        raise ServiceUnavailableError(
            "Unified RAG service not available. Please check Claude API configuration.",
            details={
                'service': 'Unified RAG',
                'suggestion': 'ANTHROPIC_API_KEY environment variable is not set or invalid.'
            }
        )
    
    data = request.get_json() or {}
    question = data.get('question')
    model = data.get('model', Config.CLAUDE_MODEL)
    max_tokens = data.get('max_tokens', 2000)
    sources = data.get('sources')  # Optional: ['gladly', 'survicate', 'zoom'] or None for all
    conversation_history = data.get('conversation_history')
    
    if not question:
        raise ValidationError(
            "Question is required",
            details={'field': 'question', 'suggestion': 'Provide a question in the request body'}
        )
    
    logger.info(f"Unified RAG query: question={question[:100]}, sources={sources}, "
               f"has_history={bool(conversation_history)}")
    
    result = unified_rag_service.process_query(
        question=question,
        model=model,
        max_tokens=max_tokens,
        sources=sources,
        conversation_history=conversation_history
    )
    
    return jsonify(result)


