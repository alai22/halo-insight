"""
Helper functions for common validation and error scenarios
"""

from typing import Dict, List, Optional
from datetime import datetime
from ..core.exceptions import ValidationError


def validate_required_fields(data: Dict, required_fields: List[str]) -> None:
    """
    Validate required fields, raise ValidationError if missing
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
        
    Raises:
        ValidationError: If any required field is missing
    """
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise ValidationError(
            f"Missing required fields: {', '.join(missing_fields)}",
            details={'missing_fields': missing_fields, 'required_fields': required_fields}
        )


def validate_date_format(date_str: str, field_name: str) -> None:
    """
    Validate date format (YYYY-MM-DD), raise ValidationError if invalid
    
    Args:
        date_str: Date string to validate
        field_name: Name of the field being validated (for error message)
        
    Raises:
        ValidationError: If date format is invalid
    """
    if not date_str:
        raise ValidationError(
            f"{field_name} is required",
            details={'field': field_name, 'format': 'YYYY-MM-DD'}
        )
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValidationError(
            f"Invalid date format for {field_name}. Expected YYYY-MM-DD, got: {date_str}",
            details={'field': field_name, 'provided': date_str, 'expected_format': 'YYYY-MM-DD'}
        )


def validate_date_range(start_date: str, end_date: str) -> None:
    """
    Validate date range, raise ValidationError if invalid
    
    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        
    Raises:
        ValidationError: If date range is invalid
    """
    # Validate formats first
    validate_date_format(start_date, 'start_date')
    validate_date_format(end_date, 'end_date')
    
    # Parse dates
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Validate range
    if start > end:
        raise ValidationError(
            f"Start date ({start_date}) must be before or equal to end date ({end_date})",
            details={
                'start_date': start_date,
                'end_date': end_date,
                'suggestion': 'Ensure start_date is before end_date'
            }
        )


def validate_list_items(data: List, item_validator: callable, field_name: str) -> None:
    """
    Validate items in a list using a validator function
    
    Args:
        data: List to validate
        item_validator: Function that validates each item (raises ValidationError if invalid)
        field_name: Name of the field being validated
        
    Raises:
        ValidationError: If any item fails validation
    """
    if not isinstance(data, list):
        raise ValidationError(
            f"{field_name} must be a list",
            details={'field': field_name, 'provided_type': type(data).__name__}
        )
    
    for idx, item in enumerate(data):
        try:
            item_validator(item, idx)
        except ValidationError as e:
            # Add index context to the error
            raise ValidationError(
                f"Invalid item at index {idx} in {field_name}: {e.message}",
                details={'field': field_name, 'index': idx, **e.details}
            )


def validate_message_format(message: Dict, index: Optional[int] = None) -> None:
    """
    Validate message format for conversation history
    
    Args:
        message: Message dictionary to validate
        index: Optional index in the list (for error messages)
        
    Raises:
        ValidationError: If message format is invalid
    """
    if not isinstance(message, dict):
        idx_str = f" at index {index}" if index is not None else ""
        raise ValidationError(
            f"Message{idx_str} must be a dictionary",
            details={'index': index, 'provided_type': type(message).__name__}
        )
    
    if 'role' not in message:
        idx_str = f" at index {index}" if index is not None else ""
        raise ValidationError(
            f"Message{idx_str} missing required field 'role'",
            details={'index': index, 'missing_field': 'role'}
        )
    
    if 'content' not in message:
        idx_str = f" at index {index}" if index is not None else ""
        raise ValidationError(
            f"Message{idx_str} missing required field 'content'",
            details={'index': index, 'missing_field': 'content'}
        )
    
    if message['role'] not in ['user', 'assistant']:
        idx_str = f" at index {index}" if index is not None else ""
        raise ValidationError(
            f"Message{idx_str} role must be 'user' or 'assistant', got: {message['role']}",
            details={'index': index, 'provided_role': message['role'], 'valid_roles': ['user', 'assistant']}
        )

