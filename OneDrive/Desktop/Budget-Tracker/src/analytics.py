"""Analytics and reporting for budget tracking"""

from typing import List, Dict, Tuple
from datetime import datetime
from collections import defaultdict
from .transaction import Transaction


class BudgetAnalytics:
    """Calculate analytics and summaries from transactions"""
    
    def __init__(self, transactions: List[Transaction]):
        """Initialize with list of transactions"""
        self.transactions = transactions
    
    def get_total_income(self) -> float:
        """Calculate total income"""
        return sum(t.amount for t in self.transactions if t.trans_type == "Income")
    
    def get_total_expense(self) -> float:
        """Calculate total expenses"""
        return sum(t.amount for t in self.transactions if t.trans_type == "Expense")
    
    def get_balance(self) -> float:
        """Calculate balance (income - expenses)"""
        return self.get_total_income() - self.get_total_expense()
    
    def get_expenses_by_category(self) -> Dict[str, float]:
        """Get total expenses grouped by category"""
        expenses = defaultdict(float)
        for t in self.transactions:
            if t.trans_type == "Expense":
                expenses[t.category] += t.amount
        return dict(sorted(expenses.items(), key=lambda x: x[1], reverse=True))
    
    def get_income_by_category(self) -> Dict[str, float]:
        """Get total income grouped by category"""
        income = defaultdict(float)
        for t in self.transactions:
            if t.trans_type == "Income":
                income[t.category] += t.amount
        return dict(sorted(income.items(), key=lambda x: x[1], reverse=True))
    
    def get_monthly_summary(self) -> Dict[str, Dict[str, float]]:
        """Get monthly income and expenses breakdown"""
        monthly = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
        
        for t in self.transactions:
            # Extract YYYY-MM from date
            month = t.date[:7]
            if t.trans_type == "Income":
                monthly[month]["income"] += t.amount
            else:
                monthly[month]["expense"] += t.amount
        
        return dict(sorted(monthly.items()))
    
    def get_summary_report(self) -> str:
        """Generate a text summary report"""
        total_income = self.get_total_income()
        total_expense = self.get_total_expense()
        balance = self.get_balance()
        
        report = "\n" + "="*50 + "\n"
        report += "BUDGET SUMMARY REPORT\n"
        report += "="*50 + "\n\n"
        
        report += f"Total Income:       ${total_income:>10.2f}\n"
        report += f"Total Expenses:     ${total_expense:>10.2f}\n"
        report += f"Balance:            ${balance:>10.2f}\n"
        report += "\n" + "-"*50 + "\n"
        report += "EXPENSES BY CATEGORY\n"
        report += "-"*50 + "\n"
        
        expenses_by_cat = self.get_expenses_by_category()
        if expenses_by_cat:
            for category, amount in expenses_by_cat.items():
                percentage = (amount / total_expense * 100) if total_expense > 0 else 0
                report += f"{category:<25} ${amount:>10.2f} ({percentage:>5.1f}%)\n"
        else:
            report += "No expenses recorded.\n"
        
        report += "\n" + "-"*50 + "\n"
        report += "INCOME BY CATEGORY\n"
        report += "-"*50 + "\n"
        
        income_by_cat = self.get_income_by_category()
        if income_by_cat:
            for category, amount in income_by_cat.items():
                percentage = (amount / total_income * 100) if total_income > 0 else 0
                report += f"{category:<25} ${amount:>10.2f} ({percentage:>5.1f}%)\n"
        else:
            report += "No income recorded.\n"
        
        report += "\n" + "="*50 + "\n"
        return report
    
    def get_monthly_report(self) -> str:
        """Generate monthly breakdown report"""
        report = "\n" + "="*50 + "\n"
        report += "MONTHLY BREAKDOWN\n"
        report += "="*50 + "\n\n"
        
        monthly = self.get_monthly_summary()
        for month, data in monthly.items():
            balance = data["income"] - data["expense"]
            report += f"{month}:\n"
            report += f"  Income:   ${data['income']:>10.2f}\n"
            report += f"  Expenses: ${data['expense']:>10.2f}\n"
            report += f"  Balance:  ${balance:>10.2f}\n"
            report += "\n"
        
        report += "="*50 + "\n"
        return report
