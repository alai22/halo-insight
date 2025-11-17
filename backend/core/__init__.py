"""
Core package for dependency injection and service management
"""

from .service_container import ServiceContainer
from .interfaces import IStorageService, IClaudeService, IConversationService

__all__ = ['ServiceContainer', 'IStorageService', 'IClaudeService', 'IConversationService']

