"""
Professional Flask application for Budget Tracker.

This module sets up and configures the Flask application with:
- Configuration management
- Logging
- Error handling
- CORS security
- RESTful API endpoints
"""

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import io
from datetime import datetime
from functools import wraps
import logging

from config import get_config
from src.logger import LoggerFactory
from src.transaction import Transaction
from src.storage import BudgetStorage
from src.analytics import BudgetAnalytics
from src.visualization import BudgetVisualizer
from src.validators import TransactionValidator, QueryValidator, APIValidator
from src.exceptions import ValidationException, StorageException


def create_app(config_name: str = None) -> Flask:
    """
    Create and configure Flask application.
    
    Args:
        config_name: Environment name ('development', 'production', 'testing')
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Setup logging
    logger = LoggerFactory.get_logger(
        'budget_tracker',
        log_file=config.LOG_FILE,
        level=config.LOG_LEVEL
    )
    app.logger = logger
    
    # Setup CORS
    CORS(app, resources={r"/api/*": {"origins": config.CORS_ALLOWED_ORIGINS}})
    
    # Add security headers
    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    # Initialize storage
    storage = BudgetStorage()
    
    # ==================== DECORATORS ====================
    
    def log_request(f):
        """Decorator to log API requests."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            app.logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
            try:
                result = f(*args, **kwargs)
                return result
            except Exception as e:
                app.logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
                raise
        return decorated_function
    
    # ==================== TRANSACTION ENDPOINTS ====================
    
    @app.route('/api/transactions', methods=['GET'])
    @log_request
    def get_transactions():
        """
        GET /api/transactions
        
        Retrieve all transactions with optional filters.
        
        Query Parameters:
            type: Filter by transaction type ('Income' or 'Expense')
            category: Filter by category name
            
        Returns:
            JSON list of transactions
        """
        try:
            trans_type = request.args.get('type', '').strip()
            category = request.args.get('category', '').strip()
            
            # Validate filters
            is_valid, error_msg = QueryValidator.validate_filters({
                'type': trans_type,
                'category': category
            })
            if not is_valid:
                return jsonify({'error': error_msg}), 400
            
            transactions = storage.get_all_transactions()
            
            if trans_type:
                transactions = [t for t in transactions if t.trans_type == trans_type]
            if category:
                transactions = [t for t in transactions if t.category == category]
            
            app.logger.info(f"Retrieved {len(transactions)} transactions")
            return jsonify([t.to_dict() for t in transactions]), 200
        
        except Exception as e:
            app.logger.error(f"Error retrieving transactions: {str(e)}")
            return jsonify({'error': 'Failed to retrieve transactions'}), 500


    
    @app.route('/api/transactions', methods=['POST'])
    @log_request
    def add_transaction():
        """
        POST /api/transactions
        
        Add a new transaction.
        
        Request Body:
            {
                "type": "Income" | "Expense",
                "category": "Category name",
                "amount": 1000.00,
                "description": "Optional description",
                "date": "2024-12-15"  (optional, defaults to today)
            }
            
        Returns:
            Created transaction data with 201 status
        """
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Request body is required'}), 400
            
            # Sanitize input
            if 'description' in data:
                data['description'] = APIValidator.sanitize_string(data['description'])
            
            # Validate transaction data
            is_valid, error_msg = TransactionValidator.validate_transaction(data)
            if not is_valid:
                app.logger.warning(f"Validation failed: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            # Create transaction
            transaction = Transaction(
                amount=float(data['amount']),
                trans_type=data['type'],
                category=data['category'],
                description=data.get('description', ''),
                date=data.get('date')
            )
            
            # Save transaction
            storage.add_transaction(transaction)
            app.logger.info(f"Transaction created: {transaction.id}")
            
            return jsonify({
                'status': 'success',
                'message': 'Transaction created successfully',
                'transaction': transaction.to_dict()
            }), 201
        
        except ValueError as e:
            app.logger.warning(f"Invalid transaction data: {str(e)}")
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            app.logger.error(f"Error creating transaction: {str(e)}")
            return jsonify({'error': 'Failed to create transaction'}), 500


    
    @app.route('/api/transactions/<trans_id>', methods=['DELETE'])
    @log_request
    def delete_transaction(trans_id: str):
        """
        DELETE /api/transactions/<id>
        
        Delete a transaction by ID.
        
        URL Parameters:
            id: Transaction ID
            
        Returns:
            Success message or 404 if not found
        """
        try:
            success = storage.delete_transaction(trans_id)
            
            if success:
                app.logger.info(f"Transaction deleted: {trans_id}")
                return jsonify({
                    'status': 'success',
                    'message': 'Transaction deleted successfully'
                }), 200
            else:
                app.logger.warning(f"Transaction not found: {trans_id}")
                return jsonify({'error': 'Transaction not found'}), 404
        
        except Exception as e:
            app.logger.error(f"Error deleting transaction: {str(e)}")
            return jsonify({'error': 'Failed to delete transaction'}), 500

    
    # ==================== ANALYTICS ENDPOINTS ====================
    
    @app.route('/api/summary', methods=['GET'])
    @log_request
    def get_summary():
        """
        GET /api/summary
        
        Get complete budget summary and analytics.
        
        Returns:
            Summary data including totals, breakdown by category, and monthly data
        """
        try:
            transactions = storage.get_all_transactions()
            analytics = BudgetAnalytics(transactions)
            
            summary = {
                'total_income': analytics.get_total_income(),
                'total_expense': analytics.get_total_expense(),
                'balance': analytics.get_balance(),
                'expenses_by_category': analytics.get_expenses_by_category(),
                'income_by_category': analytics.get_income_by_category(),
                'monthly_summary': analytics.get_monthly_summary(),
                'transaction_count': len(transactions)
            }
            
            app.logger.info("Summary retrieved successfully")
            return jsonify(summary), 200
        
        except Exception as e:
            app.logger.error(f"Error retrieving summary: {str(e)}")
            return jsonify({'error': 'Failed to retrieve summary'}), 500


    
    @app.route('/api/stats', methods=['GET'])
    @log_request
    def get_stats():
        """
        GET /api/stats
        
        Get quick statistics snapshot.
        
        Returns:
            Quick statistics data
        """
        try:
            transactions = storage.get_all_transactions()
            analytics = BudgetAnalytics(transactions)
            
            expense_count = len([t for t in transactions if t.trans_type == 'Expense'])
            avg_expense = analytics.get_total_expense() / max(expense_count, 1)
            
            stats = {
                'total_transactions': len(transactions),
                'total_income': analytics.get_total_income(),
                'total_expense': analytics.get_total_expense(),
                'balance': analytics.get_balance(),
                'average_expense': round(avg_expense, 2),
                'categories_count': len(analytics.get_expenses_by_category())
            }
            
            return jsonify(stats), 200
        
        except Exception as e:
            app.logger.error(f"Error retrieving stats: {str(e)}")
            return jsonify({'error': 'Failed to retrieve stats'}), 500

    
    # ==================== CATEGORIES ENDPOINT ====================
    
    @app.route('/api/categories', methods=['GET'])
    @log_request
    def get_categories():
        """
        GET /api/categories
        
        Get all available transaction categories.
        
        Returns:
            Dictionary of categories grouped by type
        """
        return jsonify(Transaction.CATEGORIES), 200

    
    # ==================== CHART ENDPOINTS ====================
    
    @app.route('/api/charts/expenses-pie', methods=['GET'])
    @log_request
    def get_expense_pie_chart():
        """
        GET /api/charts/expenses-pie
        
        Get pie chart of expenses by category.
        
        Returns:
            PNG image of pie chart
        """
        try:
            transactions = storage.get_all_transactions()
            analytics = BudgetAnalytics(transactions)
            
            expenses = analytics.get_expenses_by_category()
            if not expenses:
                return jsonify({'error': 'No expense data available'}), 400
            
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.pie(expenses.values(), labels=expenses.keys(), autopct='%1.1f%%', startangle=90)
            ax.set_title("Expenses by Category", fontweight='bold')
            
            img = io.BytesIO()
            plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
            img.seek(0)
            plt.close()
            
            app.logger.info("Pie chart generated successfully")
            return send_file(img, mimetype='image/png', as_attachment=False)
        
        except Exception as e:
            app.logger.error(f"Error generating pie chart: {str(e)}")
            return jsonify({'error': 'Failed to generate chart'}), 500


    
    @app.route('/api/charts/monthly-bar', methods=['GET'])
    @log_request
    def get_monthly_bar_chart():
        """
        GET /api/charts/monthly-bar
        
        Get bar chart comparing monthly income vs expenses.
        
        Returns:
            PNG image of bar chart
        """
        try:
            transactions = storage.get_all_transactions()
            analytics = BudgetAnalytics(transactions)
            monthly = analytics.get_monthly_summary()
            
            if not monthly:
                return jsonify({'error': 'No monthly data available'}), 400
            
            import matplotlib.pyplot as plt
            months = list(monthly.keys())
            income = [monthly[m]['income'] for m in months]
            expenses = [monthly[m]['expense'] for m in months]
            
            fig, ax = plt.subplots(figsize=(12, 6))
            x = range(len(months))
            width = 0.35
            ax.bar([i - width/2 for i in x], income, width, label='Income', color='green', alpha=0.7)
            ax.bar([i + width/2 for i in x], expenses, width, label='Expenses', color='red', alpha=0.7)
            ax.set_xlabel('Month')
            ax.set_ylabel('Amount ($)')
            ax.set_title('Monthly Income vs Expenses', fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(months, rotation=45, ha='right')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            
            img = io.BytesIO()
            plt.savefig(img, format='png', bbox_inches='tight', dpi=100)
            img.seek(0)
            plt.close()
            
            app.logger.info("Monthly bar chart generated successfully")
            return send_file(img, mimetype='image/png', as_attachment=False)
        
        except Exception as e:
            app.logger.error(f"Error generating bar chart: {str(e)}")
            return jsonify({'error': 'Failed to generate chart'}), 500

    
    # ==================== WEB INTERFACE ====================
    
    @app.route('/')
    def index():
        """Serve the web dashboard."""
        return render_template('index.html')
    
    
    # ==================== ERROR HANDLERS ====================
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        app.logger.warning(f"Bad request: {error}")
        return jsonify({'error': 'Bad request'}), 400
    
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        app.logger.warning(f"Resource not found: {request.path}")
        return jsonify({'error': 'Resource not found'}), 404
    
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        app.logger.error(f"Internal server error: {error}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
    
    
    # ==================== HEALTH & INFO ====================
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """
        GET /health
        
        Health check endpoint.
        
        Returns:
            Status and timestamp
        """
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }), 200
    
    
    @app.route('/api/info', methods=['GET'])
    def app_info():
        """
        GET /api/info
        
        Get application information.
        
        Returns:
            Application metadata
        """
        return jsonify({
            'name': 'Budget Tracker',
            'version': '1.0.0',
            'environment': app.config.get('ENV', 'development'),
            'debug': app.config.get('DEBUG', False)
        }), 200
    
    
    return app


if __name__ == '__main__':
    app_instance = create_app()
    app_instance.run(host='0.0.0.0', port=5000, debug=True)
