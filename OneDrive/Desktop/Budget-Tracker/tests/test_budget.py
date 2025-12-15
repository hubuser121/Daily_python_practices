"""Unit tests for budget tracker"""

import pytest
import os
import tempfile
from src.transaction import Transaction, TransactionType
from src.storage import BudgetStorage
from src.analytics import BudgetAnalytics


class TestTransaction:
    """Test Transaction model"""
    
    def test_transaction_creation(self):
        """Test creating a transaction"""
        trans = Transaction(
            amount=50.00,
            trans_type="Expense",
            category="Food",
            description="Lunch"
        )
        assert trans.amount == 50.00
        assert trans.trans_type == "Expense"
        assert trans.category == "Food"
        assert trans.description == "Lunch"
    
    def test_transaction_to_dict(self):
        """Test converting transaction to dictionary"""
        trans = Transaction(
            amount=100.00,
            trans_type="Income",
            category="Salary",
            description="Monthly salary",
            date="2024-12-15"
        )
        trans_dict = trans.to_dict()
        
        assert trans_dict["amount"] == 100.00
        assert trans_dict["type"] == "Income"
        assert trans_dict["category"] == "Salary"
        assert trans_dict["date"] == "2024-12-15"
    
    def test_transaction_csv_serialization(self):
        """Test converting transaction to/from CSV"""
        trans = Transaction(
            amount=75.50,
            trans_type="Expense",
            category="Transport",
            description="Gas",
            date="2024-12-15"
        )
        
        csv_row = trans.to_csv_row()
        assert "75.5" in csv_row
        assert "Expense" in csv_row
        assert "Transport" in csv_row
    
    def test_transaction_default_date(self):
        """Test transaction defaults to today's date"""
        trans = Transaction(
            amount=50.00,
            trans_type="Expense",
            category="Food"
        )
        # Date should be set to today in YYYY-MM-DD format
        assert len(trans.date) == 10
        assert trans.date[4] == "-"
        assert trans.date[7] == "-"


class TestBudgetStorage:
    """Test BudgetStorage"""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = BudgetStorage(os.path.join(tmpdir, "test.csv"))
            yield storage
    
    def test_storage_file_creation(self, temp_storage):
        """Test that storage creates CSV file"""
        assert os.path.exists(temp_storage.data_path)
    
    def test_add_transaction(self, temp_storage):
        """Test adding transaction to storage"""
        trans = Transaction(
            amount=50.00,
            trans_type="Expense",
            category="Food",
            description="Lunch"
        )
        temp_storage.add_transaction(trans)
        
        transactions = temp_storage.get_all_transactions()
        assert len(transactions) == 1
        assert transactions[0].amount == 50.00
    
    def test_get_all_transactions(self, temp_storage):
        """Test retrieving all transactions"""
        trans1 = Transaction(50.00, "Expense", "Food", "Lunch")
        trans2 = Transaction(100.00, "Income", "Salary", "Monthly")
        
        temp_storage.add_transaction(trans1)
        temp_storage.add_transaction(trans2)
        
        transactions = temp_storage.get_all_transactions()
        assert len(transactions) == 2
    
    def test_get_transactions_by_type(self, temp_storage):
        """Test filtering by transaction type"""
        trans1 = Transaction(50.00, "Expense", "Food")
        trans2 = Transaction(100.00, "Income", "Salary")
        trans3 = Transaction(75.00, "Expense", "Transport")
        
        temp_storage.add_transaction(trans1)
        temp_storage.add_transaction(trans2)
        temp_storage.add_transaction(trans3)
        
        expenses = temp_storage.get_transactions_by_type("Expense")
        assert len(expenses) == 2
        
        income = temp_storage.get_transactions_by_type("Income")
        assert len(income) == 1
    
    def test_get_transactions_by_category(self, temp_storage):
        """Test filtering by category"""
        trans1 = Transaction(50.00, "Expense", "Food")
        trans2 = Transaction(100.00, "Income", "Salary")
        trans3 = Transaction(40.00, "Expense", "Food")
        
        temp_storage.add_transaction(trans1)
        temp_storage.add_transaction(trans2)
        temp_storage.add_transaction(trans3)
        
        food_trans = temp_storage.get_transactions_by_category("Food")
        assert len(food_trans) == 2
        assert all(t.category == "Food" for t in food_trans)
    
    def test_delete_transaction(self, temp_storage):
        """Test deleting a transaction"""
        trans1 = Transaction(50.00, "Expense", "Food")
        trans2 = Transaction(100.00, "Income", "Salary")
        
        temp_storage.add_transaction(trans1)
        temp_storage.add_transaction(trans2)
        
        transactions = temp_storage.get_all_transactions()
        trans_id = transactions[0].id
        
        success = temp_storage.delete_transaction(trans_id)
        assert success
        
        remaining = temp_storage.get_all_transactions()
        assert len(remaining) == 1
    
    def test_delete_nonexistent_transaction(self, temp_storage):
        """Test deleting a transaction that doesn't exist"""
        success = temp_storage.delete_transaction("nonexistent")
        assert not success


class TestBudgetAnalytics:
    """Test BudgetAnalytics"""
    
    @pytest.fixture
    def sample_transactions(self):
        """Create sample transactions for testing"""
        return [
            Transaction(100.00, "Income", "Salary", "Monthly", "2024-12-01"),
            Transaction(50.00, "Expense", "Food", "Lunch", "2024-12-05"),
            Transaction(30.00, "Expense", "Transport", "Gas", "2024-12-10"),
            Transaction(200.00, "Income", "Bonus", "Year-end", "2024-12-15"),
            Transaction(75.00, "Expense", "Food", "Dinner", "2024-12-20"),
        ]
    
    def test_total_income(self, sample_transactions):
        """Test total income calculation"""
        analytics = BudgetAnalytics(sample_transactions)
        assert analytics.get_total_income() == 300.00
    
    def test_total_expense(self, sample_transactions):
        """Test total expense calculation"""
        analytics = BudgetAnalytics(sample_transactions)
        assert analytics.get_total_expense() == 155.00
    
    def test_balance(self, sample_transactions):
        """Test balance calculation"""
        analytics = BudgetAnalytics(sample_transactions)
        assert analytics.get_balance() == 145.00
    
    def test_expenses_by_category(self, sample_transactions):
        """Test expenses grouped by category"""
        analytics = BudgetAnalytics(sample_transactions)
        expenses = analytics.get_expenses_by_category()
        
        assert expenses["Food"] == 125.00
        assert expenses["Transport"] == 30.00
    
    def test_income_by_category(self, sample_transactions):
        """Test income grouped by category"""
        analytics = BudgetAnalytics(sample_transactions)
        income = analytics.get_income_by_category()
        
        assert income["Salary"] == 100.00
        assert income["Bonus"] == 200.00
    
    def test_monthly_summary(self, sample_transactions):
        """Test monthly breakdown"""
        analytics = BudgetAnalytics(sample_transactions)
        monthly = analytics.get_monthly_summary()
        
        assert "2024-12" in monthly
        assert monthly["2024-12"]["income"] == 300.00
        assert monthly["2024-12"]["expense"] == 155.00
    
    def test_empty_transactions(self):
        """Test analytics with empty transaction list"""
        analytics = BudgetAnalytics([])
        
        assert analytics.get_total_income() == 0.0
        assert analytics.get_total_expense() == 0.0
        assert analytics.get_balance() == 0.0
        assert len(analytics.get_expenses_by_category()) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
