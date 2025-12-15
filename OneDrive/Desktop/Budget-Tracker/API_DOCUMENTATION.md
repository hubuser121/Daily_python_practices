# Budget Tracker - API Documentation

## Overview

The Budget Tracker API provides RESTful endpoints for managing personal finances including transactions, analytics, and data visualization.

**Base URL**: `http://localhost:5000/api`  
**Version**: `1.0.0`  
**Authentication**: None (add as needed)

---

## Authentication

Currently, no authentication is required. For production, implement:
- API Key authentication
- JWT tokens
- OAuth2

---

## Response Format

All responses are JSON with the following structure:

### Success Response (2xx)
```json
{
  "status": "success",
  "data": {},
  "message": "Operation completed"
}
```

### Error Response (4xx, 5xx)
```json
{
  "error": "Error message description"
}
```

---

## Transaction Endpoints

### GET /transactions
Retrieve all transactions with optional filtering.

**Query Parameters:**
- `type` (optional): Filter by type - "Income" or "Expense"
- `category` (optional): Filter by category name

**Example Request:**
```bash
GET /api/transactions?type=Expense&category=Food
```

**Response (200 OK):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2024-12-15",
    "type": "Expense",
    "category": "Food",
    "amount": 50.00,
    "description": "Lunch"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "date": "2024-12-14",
    "type": "Expense",
    "category": "Food",
    "amount": 35.50,
    "description": "Dinner"
  }
]
```

**Status Codes:**
- `200 OK` - Transactions retrieved successfully
- `400 Bad Request` - Invalid filter parameters
- `500 Internal Server Error` - Server error

---

### POST /transactions
Create a new transaction.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "type": "Income",
  "category": "Salary",
  "amount": 5000.00,
  "description": "Monthly salary",
  "date": "2024-12-15"
}
```

**Fields:**
- `type` (required): "Income" or "Expense"
- `category` (required): Category name (from /categories endpoint)
- `amount` (required): Positive decimal number
- `description` (optional): Max 500 characters
- `date` (optional): YYYY-MM-DD format, defaults to today

**Example cURL:**
```bash
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Expense",
    "category": "Food",
    "amount": 45.99,
    "description": "Groceries",
    "date": "2024-12-15"
  }'
```

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "Transaction created successfully",
  "transaction": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2024-12-15",
    "type": "Expense",
    "category": "Food",
    "amount": 45.99,
    "description": "Groceries"
  }
}
```

**Status Codes:**
- `201 Created` - Transaction created successfully
- `400 Bad Request` - Invalid input data
- `500 Internal Server Error` - Server error

---

### DELETE /transactions/{id}
Delete a transaction by ID.

**Path Parameters:**
- `id` (required): Transaction ID (UUID)

**Example Request:**
```bash
DELETE /api/transactions/550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Transaction deleted successfully"
}
```

**Status Codes:**
- `200 OK` - Transaction deleted
- `404 Not Found` - Transaction not found
- `500 Internal Server Error` - Server error

---

## Analytics Endpoints

### GET /summary
Get complete budget summary with all analytics.

**Example Request:**
```bash
GET /api/summary
```

**Response (200 OK):**
```json
{
  "total_income": 10000.00,
  "total_expense": 2500.00,
  "balance": 7500.00,
  "transaction_count": 35,
  "expenses_by_category": {
    "Food": 500.00,
    "Transport": 200.00,
    "Entertainment": 300.00,
    "Bills": 1500.00
  },
  "income_by_category": {
    "Salary": 10000.00
  },
  "monthly_summary": {
    "2024-12": {
      "income": 10000.00,
      "expense": 2500.00
    }
  }
}
```

**Status Codes:**
- `200 OK` - Summary retrieved
- `500 Internal Server Error` - Server error

---

### GET /stats
Get quick statistics snapshot.

**Example Request:**
```bash
GET /api/stats
```

**Response (200 OK):**
```json
{
  "total_transactions": 35,
  "total_income": 10000.00,
  "total_expense": 2500.00,
  "balance": 7500.00,
  "average_expense": 71.43,
  "categories_count": 4
}
```

---

## Category Endpoints

### GET /categories
Get all available transaction categories.

**Example Request:**
```bash
GET /api/categories
```

**Response (200 OK):**
```json
{
  "Income": [
    "Salary",
    "Bonus",
    "Investment",
    "Other Income"
  ],
  "Expense": [
    "Food",
    "Transport",
    "Entertainment",
    "Bills",
    "Shopping",
    "Health",
    "Other Expense"
  ]
}
```

---

## Chart Endpoints

### GET /charts/expenses-pie
Get pie chart of expenses by category.

**Example Request:**
```bash
GET /api/charts/expenses-pie
```

**Response:** PNG image (image/png)

**Query Parameters:**
- None

**Status Codes:**
- `200 OK` - Chart generated
- `400 Bad Request` - No data available
- `500 Internal Server Error` - Server error

---

### GET /charts/monthly-bar
Get bar chart comparing monthly income vs expenses.

**Example Request:**
```bash
GET /api/charts/monthly-bar
```

**Response:** PNG image (image/png)

**Status Codes:**
- `200 OK` - Chart generated
- `400 Bad Request` - No data available
- `500 Internal Server Error` - Server error

---

## Health & Info Endpoints

### GET /health
Health check endpoint.

**Example Request:**
```bash
GET /health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-15T10:30:45.123456",
  "version": "1.0.0"
}
```

---

### GET /api/info
Get application information.

**Example Request:**
```bash
GET /api/info
```

**Response (200 OK):**
```json
{
  "name": "Budget Tracker",
  "version": "1.0.0",
  "environment": "development",
  "debug": true
}
```

---

## Error Handling

The API uses standard HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

**Error Response Format:**
```json
{
  "error": "Description of what went wrong"
}
```

---

## Validation Rules

### Transaction Validation
- **amount**: Minimum $0.01, Maximum $1,000,000
- **type**: Must be "Income" or "Expense"
- **category**: Must not be empty
- **description**: Maximum 500 characters
- **date**: YYYY-MM-DD format

---

## Rate Limiting

Currently, no rate limiting is implemented. For production:
- Implement 1000 requests/hour limit per IP
- Return 429 Too Many Requests when exceeded

---

## CORS

CORS is enabled for specified origins. Configure in `.env`:
```
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5000
```

---

## Security

### Headers
The API adds security headers to all responses:
- `X-Content-Type-Options: nosniff` - Prevent MIME type sniffing
- `X-Frame-Options: SAMEORIGIN` - Prevent clickjacking
- `X-XSS-Protection: 1; mode=block` - XSS protection

### Input Sanitization
All user input is sanitized to prevent XSS attacks.

---

## Examples

### Complete Workflow

**1. Check system health:**
```bash
curl http://localhost:5000/health
```

**2. Get available categories:**
```bash
curl http://localhost:5000/api/categories
```

**3. Add a transaction:**
```bash
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Expense",
    "category": "Food",
    "amount": 50.00,
    "description": "Lunch at cafe"
  }'
```

**4. View all expenses:**
```bash
curl "http://localhost:5000/api/transactions?type=Expense"
```

**5. Get summary:**
```bash
curl http://localhost:5000/api/summary
```

**6. Download chart:**
```bash
curl http://localhost:5000/api/charts/expenses-pie -o expenses.png
```

---

## Testing

### Using Python Requests
```python
import requests

# Get summary
response = requests.get('http://localhost:5000/api/summary')
summary = response.json()
print(summary)

# Add transaction
data = {
    'type': 'Income',
    'category': 'Salary',
    'amount': 5000.00,
    'description': 'Monthly salary'
}
response = requests.post('http://localhost:5000/api/transactions', json=data)
transaction = response.json()['transaction']
print(f"Created: {transaction['id']}")
```

### Using curl
See examples above.

---

## Logging

All API requests and errors are logged. View logs in:
- Console: Real-time output
- File: `data/app.log` (rotating, max 10MB)

---

## Support & Troubleshooting

### Common Issues

**404 Not Found**
- Verify correct API endpoint
- Check URL spelling

**400 Bad Request**
- Validate request JSON format
- Check required fields
- Verify data types and constraints

**500 Internal Server Error**
- Check application logs
- Verify data directory permissions
- Ensure dependencies are installed

---

## Changelog

### Version 1.0.0 (December 2024)
- Initial release
- Transaction CRUD operations
- Analytics & reporting
- Chart generation
- RESTful API design
- Professional error handling
- Comprehensive logging

---

**Last Updated:** December 15, 2024
