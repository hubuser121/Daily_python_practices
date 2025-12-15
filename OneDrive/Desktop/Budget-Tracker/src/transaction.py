"""
Transaction model for budget tracking.

This module provides the Transaction class for representing individual financial
transactions and managing their data.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List
import uuid


class TransactionType(Enum):
    """Transaction types enumeration."""
    INCOME = "Income"
    EXPENSE = "Expense"


class Transaction:
    """
    Represents a single financial transaction.
    
    Attributes:
        id: Unique transaction identifier
        date: Transaction date in YYYY-MM-DD format
        amount: Transaction amount in dollars
        trans_type: 'Income' or 'Expense'
        category: Transaction category
        description: Optional description
    """
    
    CATEGORIES: Dict[str, List[str]] = {
        "Income": ["Salary", "Bonus", "Investment", "Other Income"],
        "Expense": ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Health", "Other Expense"]
    }
    
    def __init__(
        self,
        amount: float,
        trans_type: str,
        category: str,
        description: str = "",
        date: Optional[str] = None,
        trans_id: Optional[str] = None
    ) -> None:
        """
        Initialize a transaction.
        
        Args:
            amount: Transaction amount (positive number)
            trans_type: "Income" or "Expense"
            category: Category of transaction
            description: Optional description
            date: Transaction date (YYYY-MM-DD format, defaults to today)
            trans_id: Optional transaction ID (auto-generated if not provided)
            
        Raises:
            ValueError: If amount is negative or invalid
        """
        self.amount: float = float(amount)
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        
        self.trans_type: str = trans_type
        self.category: str = category
        self.description: str = description
        self.date: str = date or datetime.now().strftime("%Y-%m-%d")
        self.id: str = trans_id or self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique ID based on UUID."""
        return str(uuid.uuid4())
    
    def to_dict(self) -> Dict[str, any]:
        """
        Convert transaction to dictionary.
        
        Returns:
            Dictionary representation of transaction
        """
        return {
            "id": self.id,
            "date": self.date,
            "type": self.trans_type,
            "category": self.category,
            "amount": self.amount,
            "description": self.description
        }
    
    def to_csv_row(self) -> str:
        """
        Format transaction as CSV row.
        
        Returns:
            CSV formatted string
        """
        return f"{self.id},{self.date},{self.trans_type},{self.category},{self.amount},{self.description}"
    
    @classmethod
    def from_csv_row(cls, row: str) -> "Transaction":
        """
        Create transaction from CSV row.
        
        Args:
            row: CSV formatted string
            
        Returns:
            Transaction instance
            
        Raises:
            ValueError: If CSV row is invalid
        """
        parts = row.strip().split(",")
        if len(parts) < 5:
            raise ValueError(f"Invalid CSV row: {row}")
        
        trans = cls(
            amount=float(parts[4]),
            trans_type=parts[2],
            category=parts[3],
            description=parts[5] if len(parts) > 5 else "",
            date=parts[1],
            trans_id=parts[0]
        )
        return trans
    
    def __repr__(self) -> str:
        """Professional string representation."""
        return (f"Transaction(id={self.id}, date={self.date}, "
                f"type={self.trans_type}, category={self.category}, "
                f"amount=${self.amount:.2f})")
