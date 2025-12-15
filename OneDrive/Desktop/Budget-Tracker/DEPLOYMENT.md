# Budget Tracker - Deployment Guide

## Quick Start

### Option 1: Run Locally (Development)

```bash
# Navigate to project directory
cd Budget_Tracker

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit http://localhost:5000 in your browser.

---

### Option 2: Docker (Recommended)

#### Prerequisites
- Docker installed ([Download here](https://www.docker.com/products/docker-desktop))

#### Run with Docker

```bash
# Build the image
docker build -t budget-tracker .

# Run the container
docker run -p 5000:5000 -v $(pwd)/data:/app/data budget-tracker
```

Or with Docker Compose:

```bash
docker-compose up --build
```

Visit http://localhost:5000

---

### Option 3: Deploy to Cloud

#### A. Heroku (Free tier available)

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **View logs**
   ```bash
   heroku logs --tail
   ```

#### B. Railway.app (Modern Alternative)

1. **Sign up** at https://railway.app

2. **Connect your GitHub repo**

3. **Set environment variables**
   - `FLASK_ENV=production`

4. **Deploy** - Railway auto-deploys on push

#### C. Render.com

1. **Sign up** at https://render.com

2. **Create new Web Service**

3. **Connect GitHub repository**

4. **Set start command**
   ```
   gunicorn --bind 0.0.0.0:5000 app:app
   ```

5. **Deploy**

#### D. AWS, Google Cloud, or Azure

Use their container services:
- AWS: Elastic Container Service (ECS)
- Google Cloud: Cloud Run
- Azure: App Service

Push Docker image to their registries and deploy.

---

## Environment Variables

Create a `.env` file (for production):

```
FLASK_ENV=production
FLASK_DEBUG=False
```

---

## Database Persistence

The app stores data in `data/transactions.csv`. 

For cloud deployment:
- Ensure the `/data` volume is persistent
- Or upgrade to PostgreSQL/MongoDB for scalability

---

## Monitoring & Maintenance

### Health Check
```bash
curl http://localhost:5000/health
```

### View Logs
```bash
# Docker
docker logs container_id

# Heroku
heroku logs --tail

# Railway
View in dashboard
```

### Backup Data
```bash
# Copy local data
cp data/transactions.csv backup/transactions_backup.csv

# Or from container
docker cp container_id:/app/data/transactions.csv ./backup/
```

---

## Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Disable `debug=True`
- [ ] Use Gunicorn (already configured)
- [ ] Set up SSL/HTTPS
- [ ] Enable CORS for your domain only
- [ ] Regular backups
- [ ] Monitor uptime
- [ ] Set resource limits

---

## Troubleshooting

### Port already in use
```bash
# Kill process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

### Permission denied (Docker)
```bash
sudo docker-compose up
```

### Module not found errors
```bash
pip install -r requirements.txt
```

---

## API Documentation

### GET /api/transactions
Returns all transactions

### POST /api/transactions
Add new transaction
```json
{
  "type": "Income",
  "category": "Salary",
  "amount": 5000,
  "description": "Monthly salary",
  "date": "2024-12-15"
}
```

### DELETE /api/transactions/<id>
Delete transaction

### GET /api/summary
Get summary statistics

### GET /api/categories
Get available categories

### GET /api/charts/expenses-pie
Get pie chart image

### GET /api/charts/monthly-bar
Get monthly bar chart

---

## Support

For issues or questions:
1. Check logs
2. Review error messages
3. Check Flask/Python documentation
4. Open GitHub issue

---

Last Updated: December 2024
