"""
Validation module for user input and data integrity.
Provides schemas and validators for API requests.
"""

from typing import Dict, Any, Tuple, Optional
import re
from datetime import datetime


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class TransactionValidator:
    """Validates transaction data."""
    
    VALID_TYPES = ['Income', 'Expense']
    MIN_AMOUNT = 0.01
    MAX_AMOUNT = 1_000_000.00
    DESCRIPTION_MAX_LENGTH = 500
    DATE_FORMAT = '%Y-%m-%d'
    
    @classmethod
    def validate_transaction(cls, data: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate transaction data.
        
        Args:
            data: Transaction data dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Required fields
            if 'type' not in data:
                return False, "Transaction type is required"
            if 'category' not in data:
                return False, "Category is required"
            if 'amount' not in data:
                return False, "Amount is required"
            
            # Type validation
            if data['type'] not in cls.VALID_TYPES:
                return False, f"Invalid type. Must be one of: {', '.join(cls.VALID_TYPES)}"
            
            # Amount validation
            try:
                amount = float(data['amount'])
                if amount < cls.MIN_AMOUNT:
                    return False, f"Amount must be at least ${cls.MIN_AMOUNT}"
                if amount > cls.MAX_AMOUNT:
                    return False, f"Amount cannot exceed ${cls.MAX_AMOUNT}"
            except (ValueError, TypeError):
                return False, "Amount must be a valid number"
            
            # Category validation
            if not isinstance(data['category'], str) or not data['category'].strip():
                return False, "Category must be a non-empty string"
            
            # Description validation
            if 'description' in data:
                if not isinstance(data['description'], str):
                    return False, "Description must be a string"
                if len(data['description']) > cls.DESCRIPTION_MAX_LENGTH:
                    return False, f"Description cannot exceed {cls.DESCRIPTION_MAX_LENGTH} characters"
            
            # Date validation (if provided)
            if 'date' in data and data['date']:
                try:
                    datetime.strptime(data['date'], cls.DATE_FORMAT)
                except ValueError:
                    return False, f"Date must be in format: {cls.DATE_FORMAT}"
            
            return True, ""
        
        except Exception as e:
            return False, f"Validation error: {str(e)}"


class QueryValidator:
    """Validates query parameters."""
    
    @classmethod
    def validate_filters(cls, filters: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate query filters.
        
        Args:
            filters: Filter parameters
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        valid_types = ['Income', 'Expense']
        
        # Validate transaction type filter
        if 'type' in filters and filters['type']:
            if filters['type'] not in valid_types:
                return False, f"Invalid type filter. Must be one of: {', '.join(valid_types)}"
        
        # Validate category filter
        if 'category' in filters and filters['category']:
            if not isinstance(filters['category'], str) or not filters['category'].strip():
                return False, "Category filter must be a non-empty string"
        
        return True, ""


class APIValidator:
    """Validates API request/response."""
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 500) -> str:
        """
        Sanitize string input.
        
        Args:
            value: String to sanitize
            max_length: Maximum length
            
        Returns:
            Sanitized string
        """
        if not isinstance(value, str):
            return ""
        # Remove extra whitespace
        value = ' '.join(value.split())
        # Limit length
        value = value[:max_length]
        return value
