"""
Unified data models for cross-source RAG queries
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class UnifiedDataItem:
    """Unified data model for all sources (Gladly, Survicate, Zoom)"""
    # Common fields
    id: str
    source: str  # 'gladly', 'survicate', 'zoom'
    timestamp: str
    content: Dict[str, Any]
    searchable_text: str
    
    # Source-specific metadata
    source_metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Optional fields that may exist in some sources
    customer_id: Optional[str] = None
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None
    email: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'source': self.source,
            'timestamp': self.timestamp,
            'content': self.content,
            'searchable_text': self.searchable_text,
            'source_metadata': self.source_metadata,
            'customer_id': self.customer_id,
            'conversation_id': self.conversation_id,
            'user_id': self.user_id,
            'email': self.email
        }
    
    @classmethod
    def from_gladly_conversation_dict(cls, item_dict: Dict[str, Any]) -> 'UnifiedDataItem':
        """Convert Gladly conversation item dict to unified format"""
        content = item_dict.get('content', {})
        return cls(
            id=item_dict.get('id', ''),
            source='gladly',
            timestamp=item_dict.get('timestamp', ''),
            content=content,
            searchable_text=cls._extract_searchable_text_from_gladly(item_dict),
            source_metadata={'content_type': content.get('type', 'Unknown')},
            customer_id=item_dict.get('customerId'),
            conversation_id=item_dict.get('conversationId')
        )
    
    @classmethod
    def from_gladly_conversation_item(cls, item) -> 'UnifiedDataItem':
        """Convert Gladly ConversationItem object to unified format"""
        return cls(
            id=item.id or str(item.conversation_id),
            source='gladly',
            timestamp=item.timestamp,
            content=item.content,
            searchable_text=item.searchable_text or '',
            source_metadata={'content_type': item.content_type},
            customer_id=item.customer_id,
            conversation_id=item.conversation_id
        )
    
    @classmethod
    def from_survicate_survey_dict(cls, survey_dict: Dict[str, Any]) -> 'UnifiedDataItem':
        """Convert Survicate survey dict to unified format"""
        return cls(
            id=survey_dict.get('response_uuid') or survey_dict.get('uuid', ''),
            source='survicate',
            timestamp=survey_dict.get('date_time', ''),
            content={
                'answers': survey_dict.get('answers', {}),
                'questions': survey_dict.get('questions', {})
            },
            searchable_text=cls._extract_searchable_text_from_survicate(survey_dict),
            source_metadata={'survey_id': survey_dict.get('survey_id')},
            user_id=survey_dict.get('user_id'),
            email=survey_dict.get('email')
        )
    
    @classmethod
    def from_survicate_survey(cls, survey) -> 'UnifiedDataItem':
        """Convert Survicate SurveyResponse object to unified format"""
        return cls(
            id=survey.response_uuid or '',
            source='survicate',
            timestamp=survey.date_time or '',
            content={'answers': survey.answers, 'metadata': survey.metadata},
            searchable_text=survey.searchable_text or '',
            source_metadata={},
            user_id=survey.user_id,
            email=survey.email
        )
    
    @classmethod
    def from_zoom_chat(cls, message: Dict[str, Any], session_id: str) -> 'UnifiedDataItem':
        """Convert Zoom chat message to unified format"""
        return cls(
            id=f"{session_id}_{message.get('id', '')}",
            source='zoom',
            timestamp=message.get('date_time') or message.get('timestamp', ''),
            content={
                'message': message.get('message', ''),
                'sender': message.get('sender', {})
            },
            searchable_text=message.get('message', ''),
            source_metadata={
                'session_id': session_id,
                'message_type': message.get('message_type')
            },
            user_id=message.get('sender', {}).get('id')
        )
    
    @staticmethod
    def _extract_searchable_text_from_gladly(item_dict: Dict[str, Any]) -> str:
        """Extract searchable text from Gladly conversation item"""
        text_parts = []
        content = item_dict.get('content', {})
        
        if 'content' in content:
            text_parts.append(str(content['content']))
        if 'subject' in content:
            text_parts.append(str(content['subject']))
        if 'body' in content:
            text_parts.append(str(content['body']))
        
        return ' '.join(text_parts).lower()
    
    @staticmethod
    def _extract_searchable_text_from_survicate(survey_dict: Dict[str, Any]) -> str:
        """Extract searchable text from Survicate survey"""
        text_parts = []
        answers = survey_dict.get('answers', {})
        
        for question, answer in answers.items():
            if answer:
                if isinstance(answer, dict):
                    answer_text = answer.get('Answer', '') or answer.get('answer', '')
                    comment_text = answer.get('Comment', '') or answer.get('comment', '')
                    if answer_text:
                        text_parts.append(str(answer_text))
                    if comment_text:
                        text_parts.append(str(comment_text))
                else:
                    text_parts.append(str(answer))
        
        if survey_dict.get('email'):
            text_parts.append(survey_dict['email'])
        
        return ' '.join(text_parts).lower()

