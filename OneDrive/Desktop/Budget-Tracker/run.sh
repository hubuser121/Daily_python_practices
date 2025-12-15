#!/bin/bash
# Budget Tracker - Quick Start Script

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Budget Tracker - Quick Start${NC}"
echo -e "${BLUE}================================${NC}\n"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3.8+"
    exit 1
fi

echo -e "${GREEN}✓ Python found${NC}\n"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}\n"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}\n"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q
echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Run the application
echo -e "${BLUE}Starting Budget Tracker...${NC}"
echo "Open your browser and go to: http://localhost:5000"
echo ""

python app.py
