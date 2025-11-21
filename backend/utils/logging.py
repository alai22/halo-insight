"""
Logging utilities with request ID support
"""

import logging
import sys
from typing import Optional
from flask import g, has_request_context


class RequestIDFilter(logging.Filter):
    """
    Logging filter that automatically adds request_id to log records.
    Works both inside and outside Flask request context.
    """
    
    def filter(self, record):
        """Add request_id to log record if available"""
        if has_request_context():
            record.request_id = getattr(g, 'request_id', 'no-request-id')
        else:
            record.request_id = 'no-context'
        return True


def setup_logging(level: str = 'INFO', log_file: Optional[str] = None) -> logging.Logger:
    """Setup structured logging with request ID support"""
    
    # Create logger
    logger = logging.getLogger('gladly_analyzer')
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter with request ID support
    # Format: timestamp - logger_name - level - [req:request_id] - message
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [req:%(request_id)s] - %(message)s'
    )
    
    # Add request ID filter to logger
    request_id_filter = RequestIDFilter()
    logger.addFilter(request_id_filter)
    
    # Console handler with UTF-8 encoding support for Windows
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    # Add request ID filter to handler as well (for redundancy)
    console_handler.addFilter(request_id_filter)
    # Configure handler to handle encoding errors gracefully
    if hasattr(console_handler.stream, 'reconfigure'):
        try:
            console_handler.stream.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, ValueError):
            pass  # Stream doesn't support reconfigure (e.g., some file streams)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(request_id_filter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance with request ID support.
    All log messages from this logger will automatically include request_id.
    """
    logger = logging.getLogger(f'gladly_analyzer.{name}')
    
    # Ensure request ID filter is added (in case logger was created before setup_logging)
    if not any(isinstance(f, RequestIDFilter) for f in logger.filters):
        logger.addFilter(RequestIDFilter())
    
    return logger


# Default logger instance
logger = get_logger('main')
