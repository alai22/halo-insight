"""
Unified RAG (Retrieval-Augmented Generation) service
Supports querying across Gladly conversations, Survicate surveys, and Zoom chats
"""

from typing import Dict, Any, List, Optional, Set
from ..utils.logging import get_logger
from ..utils.helpers import extract_json_from_text
from ..models.response import RAGProcess
from ..models.unified_data import UnifiedDataItem
from ..core.interfaces import (
    IUnifiedRAGService, IClaudeService, IConversationService, 
    ISurveyService
)
from ..core.exceptions import ClaudeAPIError

logger = get_logger('unified_rag_service')


class UnifiedRAGService(IUnifiedRAGService):
    """Unified RAG service for querying across all data sources"""
    
    def __init__(self, 
                 claude_service: IClaudeService,
                 conversation_service: IConversationService,
                 survey_service: ISurveyService,
                 zoom_service: Optional[Any] = None):  # Zoom service TBD
        """Initialize unified RAG service"""
        self.claude_service = claude_service
        self.conversation_service = conversation_service
        self.survey_service = survey_service
        self.zoom_service = zoom_service
    
    def process_query(self, 
                     question: str, 
                     model: str = None, 
                     max_tokens: int = 2000,
                     sources: Optional[List[str]] = None,
                     conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """Process a RAG query across multiple data sources"""
        logger.info(f"Starting unified RAG query: {question[:100]}, sources={sources}")
        
        # Determine which sources to query
        available_sources = self._get_available_sources()
        sources_to_query = self._determine_sources(question, sources, available_sources)
        
        if not sources_to_query:
            logger.warning("No available sources to query")
            return {
                'success': False,
                'error': 'No data sources available. Please ensure at least one data source is loaded.',
                'available_sources': list(available_sources)
            }
        
        logger.info(f"Querying sources: {sources_to_query}")
        
        # Initialize RAG process
        rag_process = RAGProcess(steps=[])
        
        # Step 1: Query Planning
        plan = self._plan_query(question, model, rag_process, sources_to_query)
        
        # Step 2: Data Retrieval (from all selected sources)
        relevant_data = self._retrieve_data(plan, rag_process, sources_to_query)
        
        # Step 3: Data Analysis
        response = self._analyze_data(
            question, relevant_data, plan, model, max_tokens, 
            rag_process, sources_to_query, conversation_history
        )
        
        logger.info(f"Unified RAG query completed: sources={sources_to_query}, "
                   f"data_retrieved={len(relevant_data)}, tokens_used={response.tokens_used}")
        
        return {
            'success': True,
            'response': {
                'content': [{'type': 'text', 'text': response.content}],
                'usage': {'output_tokens': response.tokens_used}
            },
            'rag_process': {
                'steps': [
                    {
                        'step': step.step,
                        'name': step.name,
                        'description': step.description,
                        'status': step.status,
                        'details': step.details,
                        'warning': step.warning
                    } for step in rag_process.steps
                ],
                'plan': rag_process.plan,
                'retrieval_stats': rag_process.retrieval_stats,
                'data_summary': rag_process.data_summary
            },
            'data_retrieved': len(relevant_data),
            'sources_queried': sources_to_query,
            'plan': plan
        }
    
    def _get_available_sources(self) -> Set[str]:
        """Get list of available data sources"""
        sources = set()
        
        if self.conversation_service and self.conversation_service.is_available():
            sources.add('gladly')
        
        if self.survey_service and self.survey_service.is_available():
            sources.add('survicate')
        
        if self.zoom_service:  # TODO: Add zoom availability check
            sources.add('zoom')
        
        return sources
    
    def _determine_sources(self, 
                          question: str, 
                          requested_sources: Optional[List[str]],
                          available_sources: Set[str]) -> List[str]:
        """Determine which sources to query based on question and availability"""
        if requested_sources:
            # Filter to only available sources
            return [s for s in requested_sources if s in available_sources]
        
        # Auto-detect based on question (simple keyword matching for now)
        question_lower = question.lower()
        
        sources = []
        if 'survey' in question_lower or 'churn' in question_lower or 'cancellation' in question_lower:
            if 'survicate' in available_sources:
                sources.append('survicate')
        
        if 'zoom' in question_lower or 'chat' in question_lower or 'meeting' in question_lower:
            if 'zoom' in available_sources:
                sources.append('zoom')
        
        if 'conversation' in question_lower or 'support' in question_lower or 'ticket' in question_lower:
            if 'gladly' in available_sources:
                sources.append('gladly')
        
        # If no specific sources detected, use all available
        if not sources:
            sources = list(available_sources)
        
        return sources if sources else list(available_sources)
    
    def _plan_query(self, 
                   question: str, 
                   model: str, 
                   rag_process: RAGProcess,
                   sources: List[str]) -> Dict[str, Any]:
        """Step 1: Query Planning with source awareness"""
        rag_process.add_step(1, 'Query Planning', 
                           f'Claude analyzes your question and creates a retrieval plan for sources: {sources}')
        
        # Build data source descriptions
        source_descriptions = []
        if 'gladly' in sources:
            source_descriptions.append("""
- GLADLY (Support Conversations):
  * CHAT_MESSAGE: Customer and agent chat messages
  * EMAIL: Email communications with subjects and content
  * CONVERSATION_NOTE: Agent notes and internal documentation
  * CONVERSATION_STATUS_CHANGE: Status updates (OPEN/CLOSED)
  * PHONE_CALL: Phone call records
  * TOPIC_CHANGE: Topic changes in conversations
  Each item has: timestamp, customerId, conversationId, and content (which varies by type).
""")
        
        if 'survicate' in sources:
            source_descriptions.append("""
- SURVICATE (Cancellation Surveys):
  * Survey responses with answers to Q#1 through Q#19
  * Date & Time (UTC) for each response
  * User information (email, name, user_id)
  * Questions cover cancellation reasons, GPS issues, battery problems, training, customer service
  Each response contains: Date/time of response, answers to multiple-choice and open-ended questions
""")
        
        if 'zoom' in sources:
            source_descriptions.append("""
- ZOOM (Chat Messages):
  * Team chat messages and conversations
  * Direct messages between users
  * Meeting chat messages
  * Timestamps and sender information
""")
        
        query_planning_prompt = f"""You are a data analysis assistant. I have customer data from multiple sources:

{''.join(source_descriptions)}

Question: "{question}"

Based on this question, provide a JSON response with:
1. "search_terms": List of specific terms to search for across all sources
2. "sources": List of sources to focus on (e.g., ["gladly", "survicate", "zoom"] or ["all"])
3. "content_types": For Gladly only - content types to focus on (e.g., ["CHAT_MESSAGE", "EMAIL"])
4. "questions_of_interest": For Survicate only - question keys that might be relevant (e.g., ["Q1", "Q2"])
5. "time_filters": Any time-based filtering needed (e.g., "last_24_hours", "last_30_days", "all")
6. "analysis_focus": What specific aspects to focus on in the analysis
7. "max_items_per_source": Maximum items to retrieve per source (suggest 50-100)
8. "cross_source_analysis": Whether to look for patterns across sources (true/false)

Be specific and comprehensive in your search terms. Think about synonyms and different ways the same issue might be expressed.

Respond with valid JSON only."""
        
        try:
            planning_response = self.claude_service.send_message(
                message=query_planning_prompt,
                model=model,
                max_tokens=500
            )
            
            plan = extract_json_from_text(planning_response.content)
            if not plan:
                raise ClaudeAPIError(
                    "Could not extract JSON from planning response",
                    details={'response_preview': planning_response.content[:200] if planning_response.content else 'No content'}
                )
            
            # Ensure sources in plan match requested sources
            if 'sources' in plan:
                plan['sources'] = [s for s in plan['sources'] if s in sources]
            else:
                plan['sources'] = sources
            
            rag_process.plan = plan
            rag_process.update_step(1, 'completed', {
                'search_terms': plan.get('search_terms', []),
                'sources': plan.get('sources', sources),
                'time_filters': plan.get('time_filters', 'all'),
                'analysis_focus': plan.get('analysis_focus', 'general analysis'),
                'max_items_per_source': plan.get('max_items_per_source', 100)
            })
            
        except Exception as e:
            logger.warning(f"Query planning failed, using fallback: {str(e)}")
            plan = {
                "search_terms": [question],
                "sources": sources,
                "content_types": ["CHAT_MESSAGE", "EMAIL", "CONVERSATION_NOTE"] if 'gladly' in sources else [],
                "questions_of_interest": [] if 'survicate' in sources else [],
                "time_filters": "all",
                "analysis_focus": "general analysis",
                "max_items_per_source": 100,
                "cross_source_analysis": False
            }
            rag_process.plan = plan
            rag_process.update_step(1, 'completed', plan, f"Planning failed, using fallback: {str(e)}")
        
        return plan
    
    def _retrieve_data(self, 
                      plan: Dict[str, Any], 
                      rag_process: RAGProcess,
                      sources: List[str]) -> List[UnifiedDataItem]:
        """Step 2: Data Retrieval from multiple sources"""
        rag_process.add_step(2, 'Data Retrieval', 
                           f'Semantic search retrieves relevant data from {len(sources)} source(s)')
        
        all_data: List[UnifiedDataItem] = []
        retrieval_stats = {
            'total_searched': 0,
            'by_source': {},
            'by_search_term': {},
            'sources_queried': sources,
            'diagnostics': {}
        }
        
        search_terms = plan.get('search_terms', [])
        max_items_per_source = plan.get('max_items_per_source', 100)
        
        # Retrieve from each source
        if 'gladly' in sources:
            gladly_data = self._retrieve_gladly_data(plan, search_terms, max_items_per_source)
            all_data.extend(gladly_data)
            retrieval_stats['by_source']['gladly'] = {
                'count': len(gladly_data),
                'total_available': len(self.conversation_service.conversations) if self.conversation_service.is_available() else 0
            }
        
        if 'survicate' in sources:
            survicate_data = self._retrieve_survicate_data(plan, search_terms, max_items_per_source)
            all_data.extend(survicate_data)
            retrieval_stats['by_source']['survicate'] = {
                'count': len(survicate_data),
                'total_available': len(self.survey_service.surveys) if self.survey_service.is_available() else 0
            }
        
        if 'zoom' in sources and self.zoom_service:
            zoom_data = self._retrieve_zoom_data(plan, search_terms, max_items_per_source)
            all_data.extend(zoom_data)
            retrieval_stats['by_source']['zoom'] = {
                'count': len(zoom_data),
                'total_available': 0  # TODO: Get from zoom service
            }
        
        retrieval_stats['total_searched'] = len(all_data)
        retrieval_stats['final_count'] = len(all_data)
        
        rag_process.retrieval_stats = retrieval_stats
        rag_process.update_step(2, 'completed', retrieval_stats, 
                               f"Retrieved {len(all_data)} items from {len(sources)} source(s)")
        
        return all_data
    
    def _retrieve_gladly_data(self, 
                             plan: Dict[str, Any], 
                             search_terms: List[str],
                             max_items: int) -> List[UnifiedDataItem]:
        """Retrieve data from Gladly conversations"""
        if not self.conversation_service.is_available():
            logger.warning("Gladly conversation service not available")
            return []
        
        data = []
        for term in search_terms:
            term_limit = max(1, max_items // max(len(search_terms), 1))
            results = self.conversation_service.semantic_search_conversations(term, limit=term_limit)
            for item_dict in results:
                # Convert dict to UnifiedDataItem
                try:
                    unified_item = UnifiedDataItem.from_gladly_conversation_dict(item_dict)
                    data.append(unified_item)
                except Exception as e:
                    logger.warning(f"Failed to convert Gladly item to unified format: {e}")
                    continue
        
        # Apply content type filter if specified
        content_types = plan.get('content_types', [])
        if content_types and content_types != ["all"]:
            data = [item for item in data 
                   if item.source_metadata.get('content_type') in content_types]
        
        # Remove duplicates and limit
        seen_ids = set()
        unique_data = []
        for item in data:
            if item.id not in seen_ids:
                seen_ids.add(item.id)
                unique_data.append(item)
                if len(unique_data) >= max_items:
                    break
        
        return unique_data
    
    def _retrieve_survicate_data(self, 
                                plan: Dict[str, Any], 
                                search_terms: List[str],
                                max_items: int) -> List[UnifiedDataItem]:
        """Retrieve data from Survicate surveys"""
        if not self.survey_service.is_available():
            logger.warning("Survicate survey service not available")
            return []
        
        data = []
        for term in search_terms:
            term_limit = max(1, max_items // max(len(search_terms), 1))
            results = self.survey_service.semantic_search_surveys(term, limit=term_limit)
            for survey_dict in results:
                # Convert dict to UnifiedDataItem
                try:
                    unified_item = UnifiedDataItem.from_survicate_survey_dict(survey_dict)
                    data.append(unified_item)
                except Exception as e:
                    logger.warning(f"Failed to convert Survicate survey to unified format: {e}")
                    continue
        
        # Apply question filter if specified
        questions_of_interest = plan.get('questions_of_interest', [])
        if questions_of_interest:
            # Filter surveys that have answers to questions of interest
            filtered_data = []
            for item in data:
                answers = item.content.get('answers', {})
                if any(q in answers for q in questions_of_interest):
                    filtered_data.append(item)
            data = filtered_data
        
        # Remove duplicates and limit
        seen_ids = set()
        unique_data = []
        for item in data:
            if item.id not in seen_ids:
                seen_ids.add(item.id)
                unique_data.append(item)
                if len(unique_data) >= max_items:
                    break
        
        return unique_data
    
    def _retrieve_zoom_data(self, 
                           plan: Dict[str, Any], 
                           search_terms: List[str],
                           max_items: int) -> List[UnifiedDataItem]:
        """Retrieve data from Zoom chats"""
        # TODO: Implement when Zoom service is available
        # For now, return empty list
        logger.warning("Zoom data retrieval not yet implemented")
        return []
    
    def _analyze_data(self, 
                     question: str, 
                     relevant_data: List[UnifiedDataItem], 
                     plan: Dict[str, Any], 
                     model: str, 
                     max_tokens: int, 
                     rag_process: RAGProcess,
                     sources: List[str],
                     conversation_history: Optional[List[Dict[str, str]]] = None):
        """Step 3: Data Analysis across sources"""
        rag_process.add_step(3, 'Analysis', 
                           f'Claude analyzes retrieved data from {len(sources)} source(s) to answer your question')
        
        # Get summaries from each source
        summaries = []
        if 'gladly' in sources and self.conversation_service.is_available():
            try:
                summary = self.conversation_service.get_summary()
                summaries.append(f"Gladly Conversations: {summary.to_string()}")
            except Exception as e:
                logger.warning(f"Failed to get Gladly summary: {e}")
        
        if 'survicate' in sources and self.survey_service.is_available():
            try:
                summary = self.survey_service.get_summary()
                summaries.append(f"Survicate Surveys: {summary.to_string()}")
            except Exception as e:
                logger.warning(f"Failed to get Survicate summary: {e}")
        
        summary_text = "\n\n".join(summaries) if summaries else "No summary data available"
        
        # Format unified data for Claude
        formatted_data = self._format_unified_data_for_claude(relevant_data, sources)
        
        # Create system prompt
        system_prompt = self._create_unified_system_prompt(
            summary_text, formatted_data, plan, question, sources
        )
        
        response = self.claude_service.send_message(
            message=question,
            model=model,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
            conversation_history=conversation_history
        )
        
        rag_process.update_step(3, 'completed', {
            'tokens_used': response.tokens_used,
            'model_used': model,
            'sources_analyzed': sources
        })
        
        # Create data summary
        by_source = {}
        for item in relevant_data:
            source = item.source
            if source not in by_source:
                by_source[source] = 0
            by_source[source] += 1
        
        rag_process.data_summary = {
            'total_items': len(relevant_data),
            'by_source': by_source,
            'sources_queried': sources,
            'cross_source_analysis': plan.get('cross_source_analysis', False)
        }
        
        return response
    
    def _format_unified_data_for_claude(self, 
                                       data: List[UnifiedDataItem], 
                                       sources: List[str]) -> str:
        """Format unified data items for Claude prompt"""
        if not data:
            return "No data was retrieved from the search. This could mean:\n- The search terms did not match any data\n- The data sources have not been loaded yet\n\nPlease inform the user that no data was found and suggest they try different search terms or check if data has been loaded."
        
        # Group by source
        by_source = {}
        for item in data:
            if item.source not in by_source:
                by_source[item.source] = []
            by_source[item.source].append(item)
        
        formatted_parts = []
        for source in sources:
            if source in by_source:
                source_data = by_source[source]
                formatted_parts.append(f"\n{'='*60}")
                formatted_parts.append(f"{source.upper()} DATA ({len(source_data)} items)")
                formatted_parts.append(f"{'='*60}\n")
                
                # Limit to 50 items per source for performance
                items_to_show = source_data[:50]
                for item in items_to_show:
                    timestamp = item.timestamp or 'No timestamp'
                    text_preview = item.searchable_text[:200] if item.searchable_text else 'No content'
                    formatted_parts.append(f"[{timestamp}] {item.source}: {text_preview}")
                
                if len(source_data) > 50:
                    formatted_parts.append(f"\n[Note: Showing first 50 items of {len(source_data)} total for {source} source]")
        
        return "\n".join(formatted_parts)
    
    def _create_unified_system_prompt(self, 
                                     summary: str, 
                                     data_text: str, 
                                     plan: Dict[str, Any],
                                     question: str,
                                     sources: List[str]) -> str:
        """Create system prompt for unified analysis"""
        sources_list = ", ".join(sources)
        cross_source_note = ""
        if plan.get('cross_source_analysis', False) and len(sources) > 1:
            cross_source_note = """
IMPORTANT: This query requires cross-source analysis. Look for:
- Patterns and relationships across different data sources
- How issues appear in different contexts (support vs surveys vs chats)
- Customer journey across touchpoints
- Correlations between support issues and churn reasons
"""
        
        return f"""You are a data analysis assistant with access to customer data from multiple sources: {sources_list}.

DATA SUMMARY:
{summary}
{cross_source_note}
RETRIEVED DATA:
{data_text}

ANALYSIS PLAN:
- Focus: {plan.get('analysis_focus', 'general analysis')}
- Sources: {sources}
- Cross-source analysis: {plan.get('cross_source_analysis', False)}

QUESTION: {question}

Analyze the retrieved data to answer the question. If cross-source analysis is enabled, look for patterns and relationships across different data sources. Provide insights that leverage the combined data from all sources.

IMPORTANT: Format your response using proper Markdown formatting:
- Use **bold** for headings and important terms
- Use bullet points (- or *) for lists
- Use proper indentation for sub-items
- Use numbered lists (1., 2., 3.) for sequential items
- Use ## for main headings and ### for sub-headings
- Use `code formatting` for IDs and specific terms when needed
- Use tables when comparing data across sources or time periods

Make your response well-structured and easy to read with clear visual hierarchy."""


