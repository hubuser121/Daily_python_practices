# Budget Tracker

A **production-ready** full-stack budget tracking application built with Python and Flask. Track your income and expenses with real-time analytics and visualization.

**Status**: ✅ Production Ready | **Version**: 1.0.0 Professional | **Tests**: 18/18 Passing

---

## ✨ Features

### Core Functionality
- ✅ **Add/Edit/Delete Transactions** - Manage income and expenses
- ✅ **Real-time Analytics** - Track spending by category and month
- ✅ **Data Visualization** - Interactive charts (pie, bar, line)
- ✅ **Category Management** - Pre-configured income and expense categories
- ✅ **Data Persistence** - CSV-based storage with backup support
- ✅ **Web Dashboard** - Beautiful, responsive user interface
- ✅ **REST API** - 12+ professional endpoints

### Professional Features
- ✅ **Configuration Management** - Environment-specific settings
- ✅ **Professional Logging** - Rotating file logs with console output
- ✅ **Input Validation** - Comprehensive data validation & sanitization
- ✅ **Security Headers** - XSS, clickjacking, and MIME type protection
- ✅ **Type Hints** - Full static type checking support
- ✅ **Custom Exceptions** - Meaningful error handling
- ✅ **API Documentation** - Complete endpoint documentation
- ✅ **Unit Tests** - 18 comprehensive tests with 100% pass rate

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

**Option 1: Automatic (Windows)**
```bash
run.bat
```

**Option 2: Automatic (Mac/Linux)**
```bash
bash run.sh
```

**Option 3: Manual**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Run application
python app.py
```

**Visit**: http://localhost:5000

---

## 📚 Documentation

### Main Documentation
- **[README.md](README.md)** - Project overview (this file)
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference
- **[PROFESSIONAL_UPGRADE.md](PROFESSIONAL_UPGRADE.md)** - Code quality improvements
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guides

---

## 🏗️ Project Structure

```
Budget_Tracker/
├── config.py                 # Configuration management
├── app.py                    # Flask application factory
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── API_DOCUMENTATION.md     # API reference
├── PROFESSIONAL_UPGRADE.md  # Code improvements guide
├── README.md                # This file
├── src/
│   ├── main.py              # CLI application
│   ├── transaction.py       # Data model (UUID-based)
│   ├── storage.py           # Data persistence
│   ├── analytics.py         # Analytics engine
│   ├── visualization.py     # Chart generation
│   ├── logger.py            # Logging system
│   ├── validators.py        # Input validation
│   └── exceptions.py        # Custom exceptions
├── templates/
│   └── index.html           # Web dashboard
├── static/
│   ├── style.css            # Styling (900+ lines)
│   └── script.js            # Frontend logic
├── tests/
│   └── test_budget.py       # Unit tests (18 tests)
└── data/
    ├── transactions.csv     # Database
    └── app.log             # Application logs
```

---

## 🔌 API Endpoints

### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/transactions` | Get all transactions |
| POST | `/api/transactions` | Create transaction |
| DELETE | `/api/transactions/<id>` | Delete transaction |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/summary` | Complete budget summary |
| GET | `/api/stats` | Quick statistics |

### Categories & Charts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories` | Available categories |
| GET | `/api/charts/expenses-pie` | Pie chart (PNG) |
| GET | `/api/charts/monthly-bar` | Monthly bar chart (PNG) |

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/info` | App info |

**[Full API Documentation →](API_DOCUMENTATION.md)**

---

## 🧪 Testing

Run unit tests:
```bash
pytest tests/test_budget.py -v
```

Expected output:
```
18 passed in 0.31s
```

**Test Coverage:**
- ✅ Transaction model (4 tests)
- ✅ Data storage (7 tests)
- ✅ Analytics (7 tests)
- ✅ Edge cases & empty data

---

## 🎯 Use Cases

### Personal Finance Management
Track your daily spending and income patterns.

```json
GET /api/summary
{
  "total_income": 5000.00,
  "total_expense": 1200.00,
  "balance": 3800.00,
  "expenses_by_category": {
    "Food": 400,
    "Transport": 150,
    "Entertainment": 200,
    "Bills": 450
  }
}
```

### Business Expense Tracking
Monitor team or project-specific expenses.

### Monthly Budget Analysis
Visualize spending patterns over time.

---

## 🔐 Security

The application includes:
- ✅ **Input Validation** - All user input validated and sanitized
- ✅ **Security Headers** - Protection against XSS, clickjacking, MIME sniffing
- ✅ **CORS Protection** - Configurable allowed origins
- ✅ **Session Security** - Secure, HTTP-only cookies
- ✅ **Type Checking** - Static type validation

**[Security Details →](PROFESSIONAL_UPGRADE.md#-security-improvements)**

---

## 📊 Configuration

Create `.env` file from template:
```bash
cp .env.example .env
```

**Key Settings:**
- `FLASK_ENV` - Environment (development/production)
- `LOG_LEVEL` - Logging level (DEBUG/INFO/WARNING)
- `SECRET_KEY` - Flask session key
- `CORS_ALLOWED_ORIGINS` - Allowed API origins

---

## 📦 Dependencies

### Core
- **Flask** (3.0.0) - Web framework
- **Flask-CORS** (4.0.0) - CORS handling
- **Gunicorn** (21.2.0) - Production server

### Data & Analytics
- **Pandas** (2.1.3) - Data processing
- **Matplotlib** (3.8.2) - Chart generation

### Development
- **pytest** (7.4.3) - Testing framework
- **python-dotenv** (1.0.0) - Environment variables

[See requirements.txt for all dependencies]

---

## 🚢 Deployment

### Local Development
```bash
python app.py
```

### Docker
```bash
docker-compose up --build
```

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Railway, Render, or Cloud Providers
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 📈 Architecture

### Clean Architecture Pattern
```
API Layer (Flask)
    ↓
Validation Layer (validators.py)
    ↓
Business Logic (analytics.py, visualization.py)
    ↓
Data Access Layer (storage.py)
    ↓
File System (transactions.csv)
```

### Key Design Patterns
- **Factory Pattern** - Flask app creation
- **Repository Pattern** - Data access abstraction
- **Validator Pattern** - Input validation
- **Logging Decorator** - Request logging

---

## 🎓 Learning Resources

This project demonstrates professional Python development:

1. **Configuration Management** - Environment-specific settings
2. **Logging** - Production-ready logging with rotation
3. **Input Validation** - Security-first validation
4. **Type Hints** - Modern Python type checking
5. **Exception Handling** - Custom exception hierarchy
6. **Testing** - Comprehensive unit tests
7. **API Design** - RESTful endpoint design
8. **Security** - OWASP best practices
9. **Documentation** - Professional API documentation
10. **Code Organization** - Clean architecture

**[Detailed Explanation →](PROFESSIONAL_UPGRADE.md)**

---

## 🐛 Troubleshooting

### Port 5000 Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### Tests Failing
```bash
# Check logs
cat data/app.log

# Run with verbose output
pytest tests/test_budget.py -vv
```

---

## 🤝 Contributing

To extend this project:

1. **Add New Features**
   - Update models in `src/`
   - Add API endpoints in `app.py`
   - Add tests in `tests/`
   - Update documentation

2. **Code Quality**
   - Follow PEP 8 style guide
   - Add type hints to all functions
   - Write comprehensive docstrings
   - Maintain test coverage

3. **Example: Add Budget Limits Feature**
   ```python
   # src/models.py (new)
   class BudgetLimit(BaseModel):
       category: str
       monthly_limit: float
   
   # src/storage.py
   def add_budget_limit(self, limit: BudgetLimit): ...
   
   # app.py
   @app.route('/api/budget-limits', methods=['POST'])
   def add_budget_limit(): ...
   
   # tests/test_budget.py
   def test_budget_limit(): ...
   ```

---

## 📝 License

This project is open source. Use it for personal projects and learning.

---

## 🎉 What's New in v1.0.0 Professional

### Code Quality
- ✅ Full type hints (100% coverage)
- ✅ Comprehensive docstrings
- ✅ Professional logging system
- ✅ Input validation layer
- ✅ Custom exception hierarchy

### Security
- ✅ Security headers
- ✅ Input sanitization
- ✅ CORS configuration
- ✅ Session security
- ✅ Validation rules

### Documentation
- ✅ Complete API documentation
- ✅ Configuration guide
- ✅ Deployment guide
- ✅ Upgrade guide
- ✅ Professional examples

### Production Ready
- ✅ Configuration management
- ✅ Rotating file logging
- ✅ Health check endpoints
- ✅ Error handling
- ✅ All tests passing

---

## 🎯 Next Steps

### For Learning
1. Read [PROFESSIONAL_UPGRADE.md](PROFESSIONAL_UPGRADE.md)
2. Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
3. Study the source code in `src/`
4. Run tests: `pytest tests/`

### For Deployment
1. Read [DEPLOYMENT.md](DEPLOYMENT.md)
2. Configure `.env` file
3. Choose deployment platform
4. Deploy and monitor

### For Enhancement
1. Add database (PostgreSQL)
2. Implement authentication
3. Add recurring transactions
4. Build mobile app
5. Implement budgets & alerts

---

## 📞 Support

- **API Issues**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Code Quality**: See [PROFESSIONAL_UPGRADE.md](PROFESSIONAL_UPGRADE.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Logs**: Check `data/app.log`

---

**Version**: 1.0.0 Professional  
**Status**: ✅ Production Ready  
**Last Updated**: December 15, 2024  
**Test Coverage**: 18/18 passing ✅
