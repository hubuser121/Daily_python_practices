"""Storage layer for managing transaction data"""

import os
import csv
from typing import List, Optional
from .transaction import Transaction


class BudgetStorage:
    """Handles reading/writing transaction data to CSV"""
    
    def __init__(self, data_path: str = "data/transactions.csv"):
        """
        Initialize storage.
        
        Args:
            data_path: Path to CSV file for storing transactions
        """
        self.data_path = data_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Create CSV file with headers if it doesn't exist"""
        os.makedirs(os.path.dirname(self.data_path) or ".", exist_ok=True)
        
        if not os.path.exists(self.data_path):
            with open(self.data_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Date", "Type", "Category", "Amount", "Description"])
    
    def add_transaction(self, transaction: Transaction) -> None:
        """Add transaction to storage"""
        with open(self.data_path, "a", newline="") as f:
            writer = csv.writer(f)
            parts = transaction.to_csv_row().split(",")
            writer.writerow(parts)
    
    def get_all_transactions(self) -> List[Transaction]:
        """Retrieve all transactions"""
        transactions = []
        try:
            with open(self.data_path, "r") as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if row:  # Skip empty rows
                        trans = Transaction(
                            amount=float(row[4]),
                            trans_type=row[2],
                            category=row[3],
                            description=row[5] if len(row) > 5 else "",
                            date=row[1]
                        )
                        trans.id = row[0]
                        transactions.append(trans)
        except FileNotFoundError:
            pass
        return transactions
    
    def get_transactions_by_type(self, trans_type: str) -> List[Transaction]:
        """Get transactions filtered by type"""
        return [t for t in self.get_all_transactions() if t.trans_type == trans_type]
    
    def get_transactions_by_category(self, category: str) -> List[Transaction]:
        """Get transactions filtered by category"""
        return [t for t in self.get_all_transactions() if t.category == category]
    
    def get_transactions_by_date(self, date: str) -> List[Transaction]:
        """Get transactions for a specific date"""
        return [t for t in self.get_all_transactions() if t.date == date]
    
    def delete_transaction(self, trans_id: str) -> bool:
        """Delete transaction by ID"""
        transactions = self.get_all_transactions()
        filtered = [t for t in transactions if t.id != trans_id]
        
        if len(filtered) == len(transactions):
            return False  # Transaction not found
        
        self._write_all_transactions(filtered)
        return True
    
    def _write_all_transactions(self, transactions: List[Transaction]) -> None:
        """Overwrite all transactions (used for delete operations)"""
        with open(self.data_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Date", "Type", "Category", "Amount", "Description"])
            for trans in transactions:
                parts = trans.to_csv_row().split(",")
                writer.writerow(parts)
    
    def clear_all(self) -> None:
        """Clear all transactions (for testing)"""
        with open(self.data_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Date", "Type", "Category", "Amount", "Description"])
