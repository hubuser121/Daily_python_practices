"""Data visualization for budget tracking"""

import matplotlib.pyplot as plt
from typing import List, Dict
from .transaction import Transaction
from .analytics import BudgetAnalytics


class BudgetVisualizer:
    """Create charts and visualizations for budget data"""
    
    def __init__(self, transactions: List[Transaction]):
        """Initialize with list of transactions"""
        self.transactions = transactions
        self.analytics = BudgetAnalytics(transactions)
    
    def plot_expenses_by_category(self, save_path: str = None) -> None:
        """Create pie chart of expenses by category"""
        expenses = self.analytics.get_expenses_by_category()
        
        if not expenses:
            print("No expense data to visualize.")
            return
        
        categories = list(expenses.keys())
        amounts = list(expenses.values())
        
        plt.figure(figsize=(10, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        plt.title("Expenses by Category", fontsize=16, fontweight='bold')
        plt.axis('equal')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
        plt.close()
    
    def plot_income_vs_expenses(self, save_path: str = None) -> None:
        """Create bar chart comparing income and expenses"""
        monthly = self.analytics.get_monthly_summary()
        
        if not monthly:
            print("No data to visualize.")
            return
        
        months = list(monthly.keys())
        income_values = [monthly[m]["income"] for m in months]
        expense_values = [monthly[m]["expense"] for m in months]
        
        x = range(len(months))
        width = 0.35
        
        plt.figure(figsize=(12, 6))
        plt.bar([i - width/2 for i in x], income_values, width, label='Income', color='green', alpha=0.7)
        plt.bar([i + width/2 for i in x], expense_values, width, label='Expenses', color='red', alpha=0.7)
        
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Amount ($)', fontsize=12)
        plt.title('Monthly Income vs Expenses', fontsize=16, fontweight='bold')
        plt.xticks(x, months, rotation=45)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
        plt.close()
    
    def plot_monthly_expenses(self, save_path: str = None) -> None:
        """Create line chart of expenses over time"""
        monthly = self.analytics.get_monthly_summary()
        
        if not monthly:
            print("No data to visualize.")
            return
        
        months = list(monthly.keys())
        expenses = [monthly[m]["expense"] for m in months]
        
        plt.figure(figsize=(12, 6))
        plt.plot(months, expenses, marker='o', linewidth=2, markersize=8, color='red')
        plt.fill_between(range(len(months)), expenses, alpha=0.3, color='red')
        
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Expenses ($)', fontsize=12)
        plt.title('Monthly Expense Trend', fontsize=16, fontweight='bold')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
        plt.close()
    
    def plot_category_trends(self, save_path: str = None) -> None:
        """Create bar chart of top expense categories"""
        expenses = self.analytics.get_expenses_by_category()
        
        if not expenses:
            print("No expense data to visualize.")
            return
        
        # Get top 5 categories
        top_categories = dict(sorted(expenses.items(), key=lambda x: x[1], reverse=True)[:5])
        categories = list(top_categories.keys())
        amounts = list(top_categories.values())
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories, amounts, color='steelblue', alpha=0.7)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:.2f}',
                    ha='center', va='bottom', fontsize=10)
        
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Amount ($)', fontsize=12)
        plt.title('Top 5 Expense Categories', fontsize=16, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
        plt.close()
    
    def generate_all_charts(self, output_dir: str = "data") -> None:
        """Generate all charts and save to directory"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        self.plot_expenses_by_category(f"{output_dir}/expenses_by_category.png")
        self.plot_income_vs_expenses(f"{output_dir}/income_vs_expenses.png")
        self.plot_monthly_expenses(f"{output_dir}/monthly_expenses.png")
        self.plot_category_trends(f"{output_dir}/category_trends.png")
        print(f"\nAll charts generated in {output_dir}/")
