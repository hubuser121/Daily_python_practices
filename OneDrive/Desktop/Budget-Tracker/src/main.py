"""Main application with CLI interface for budget tracking"""

import os
from typing import Optional
from .transaction import Transaction, TransactionType
from .storage import BudgetStorage
from .analytics import BudgetAnalytics
from .visualization import BudgetVisualizer


class BudgetTracker:
    """Main budget tracking application"""
    
    def __init__(self, data_path: str = "data/transactions.csv"):
        """Initialize the budget tracker"""
        self.storage = BudgetStorage(data_path)
        self.data_path = data_path
    
    def clear_screen(self) -> None:
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str) -> None:
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f"  {title.center(56)}")
        print("="*60 + "\n")
    
    def print_menu(self) -> None:
        """Display main menu"""
        self.print_header("BUDGET TRACKER")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. View Summary Report")
        print("4. View Monthly Report")
        print("5. View Charts")
        print("6. Delete Transaction")
        print("7. Exit")
        print("\n" + "-"*60)
    
    def add_transaction(self) -> None:
        """Add a new transaction"""
        self.print_header("ADD TRANSACTION")
        
        # Choose transaction type
        print("Transaction Type:")
        print("1. Income")
        print("2. Expense")
        type_choice = input("\nSelect (1 or 2): ").strip()
        
        trans_type = "Income" if type_choice == "1" else "Expense"
        
        # Show available categories
        categories = Transaction.CATEGORIES[trans_type]
        print(f"\n{trans_type} Categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        cat_choice = input("\nSelect category: ").strip()
        try:
            category = categories[int(cat_choice) - 1]
        except (ValueError, IndexError):
            print("❌ Invalid category selection.")
            return
        
        # Get amount
        try:
            amount = float(input("Enter amount: $"))
            if amount <= 0:
                print("❌ Amount must be greater than 0.")
                return
        except ValueError:
            print("❌ Invalid amount.")
            return
        
        # Get description
        description = input("Enter description (optional): ").strip()
        
        # Create and save transaction
        transaction = Transaction(
            amount=amount,
            trans_type=trans_type,
            category=category,
            description=description
        )
        
        self.storage.add_transaction(transaction)
        print(f"\n✅ Transaction added successfully!")
        print(f"   {transaction}")
        input("\nPress Enter to continue...")
    
    def view_transactions(self) -> None:
        """View all transactions"""
        self.print_header("VIEW TRANSACTIONS")
        
        transactions = self.storage.get_all_transactions()
        
        if not transactions:
            print("No transactions recorded yet.")
            input("\nPress Enter to continue...")
            return
        
        # Filter options
        print("Filter by:")
        print("1. All transactions")
        print("2. Income only")
        print("3. Expense only")
        print("4. Specific category")
        
        choice = input("\nSelect (1-4): ").strip()
        
        if choice == "2":
            transactions = [t for t in transactions if t.trans_type == "Income"]
        elif choice == "3":
            transactions = [t for t in transactions if t.trans_type == "Expense"]
        elif choice == "4":
            category = input("Enter category name: ").strip()
            transactions = [t for t in transactions if t.category == category]
        
        if not transactions:
            print("No transactions found.")
            input("\nPress Enter to continue...")
            return
        
        # Display transactions
        print(f"{'Date':<12} {'Type':<10} {'Category':<15} {'Amount':<12} {'Description':<20}")
        print("-"*69)
        
        for t in transactions:
            symbol = "+" if t.trans_type == "Income" else "-"
            print(f"{t.date:<12} {t.trans_type:<10} {t.category:<15} {symbol}${t.amount:<10.2f} {t.description[:19]:<20}")
        
        print(f"\nTotal: {len(transactions)} transaction(s)")
        input("\nPress Enter to continue...")
    
    def view_summary(self) -> None:
        """View budget summary"""
        transactions = self.storage.get_all_transactions()
        analytics = BudgetAnalytics(transactions)
        print(analytics.get_summary_report())
        input("Press Enter to continue...")
    
    def view_monthly_report(self) -> None:
        """View monthly breakdown"""
        transactions = self.storage.get_all_transactions()
        analytics = BudgetAnalytics(transactions)
        print(analytics.get_monthly_report())
        input("Press Enter to continue...")
    
    def view_charts(self) -> None:
        """View data visualizations"""
        self.print_header("DATA VISUALIZATION")
        
        transactions = self.storage.get_all_transactions()
        
        if not transactions:
            print("No data to visualize. Add some transactions first.")
            input("\nPress Enter to continue...")
            return
        
        visualizer = BudgetVisualizer(transactions)
        
        print("Select chart type:")
        print("1. Expenses by Category (Pie Chart)")
        print("2. Income vs Expenses (Monthly)")
        print("3. Expense Trend (Line Chart)")
        print("4. Top Categories (Bar Chart)")
        print("5. Generate All Charts")
        print("6. Back to menu")
        
        choice = input("\nSelect (1-6): ").strip()
        
        if choice == "1":
            visualizer.plot_expenses_by_category()
        elif choice == "2":
            visualizer.plot_income_vs_expenses()
        elif choice == "3":
            visualizer.plot_monthly_expenses()
        elif choice == "4":
            visualizer.plot_category_trends()
        elif choice == "5":
            visualizer.generate_all_charts()
            print("\n✅ All charts saved to 'data/' directory")
        
        input("\nPress Enter to continue...")
    
    def delete_transaction(self) -> None:
        """Delete a transaction"""
        self.print_header("DELETE TRANSACTION")
        
        transactions = self.storage.get_all_transactions()
        
        if not transactions:
            print("No transactions to delete.")
            input("\nPress Enter to continue...")
            return
        
        # Show recent transactions
        print("Recent transactions:")
        print(f"{'#':<4} {'Date':<12} {'Type':<10} {'Category':<15} {'Amount':<12}")
        print("-"*53)
        
        for i, t in enumerate(transactions[-10:], 1):
            symbol = "+" if t.trans_type == "Income" else "-"
            print(f"{i:<4} {t.date:<12} {t.trans_type:<10} {t.category:<15} {symbol}${t.amount:<10.2f}")
        
        try:
            idx = int(input("\nEnter transaction number to delete: ").strip())
            if 1 <= idx <= len(transactions[-10:]):
                trans_to_delete = transactions[-10:][idx - 1]
                confirm = input(f"Delete '{trans_to_delete.description}' for ${trans_to_delete.amount}? (y/n): ").strip().lower()
                
                if confirm == 'y':
                    if self.storage.delete_transaction(trans_to_delete.id):
                        print("✅ Transaction deleted successfully!")
                    else:
                        print("❌ Failed to delete transaction.")
                else:
                    print("❌ Deletion cancelled.")
        except ValueError:
            print("❌ Invalid input.")
        
        input("\nPress Enter to continue...")
    
    def run(self) -> None:
        """Run the application main loop"""
        while True:
            self.clear_screen()
            self.print_menu()
            
            choice = input("Select option (1-7): ").strip()
            
            if choice == "1":
                self.add_transaction()
            elif choice == "2":
                self.view_transactions()
            elif choice == "3":
                self.view_summary()
            elif choice == "4":
                self.view_monthly_report()
            elif choice == "5":
                self.view_charts()
            elif choice == "6":
                self.delete_transaction()
            elif choice == "7":
                print("\n👋 Thank you for using Budget Tracker!")
                break
            else:
                print("❌ Invalid option. Please try again.")
                input("Press Enter to continue...")


def main():
    """Entry point"""
    tracker = BudgetTracker()
    tracker.run()


if __name__ == "__main__":
    main()
