"""
Exception handling for Budget Tracker application.
Provides custom exceptions for different error scenarios.
"""


class BudgetTrackerException(Exception):
    """Base exception for Budget Tracker application."""
    pass


class ValidationException(BudgetTrackerException):
    """Raised when data validation fails."""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


class StorageException(BudgetTrackerException):
    """Raised when data storage operations fail."""
    pass


class TransactionException(BudgetTrackerException):
    """Raised when transaction operations fail."""
    pass


class AnalyticsException(BudgetTrackerException):
    """Raised when analytics operations fail."""
    pass


class ConfigException(BudgetTrackerException):
    """Raised when configuration is invalid."""
    pass
