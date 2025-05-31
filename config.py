import os
from datetime import datetime

# Project directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports', 'figures')
SRC_DIR = os.path.join(BASE_DIR, 'src')

# Create directories if needed
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(SRC_DIR, exist_ok=True)

# Dataset paths
NEWS_DATA_PATH = os.path.join(DATA_DIR, 'financial_news.csv')
STOCK_DATA_DIR = os.path.join(DATA_DIR, 'stock_data')
os.makedirs(STOCK_DATA_DIR, exist_ok=True)

# Analysis parameters
START_DATE = datetime(2020, 1, 1)
END_DATE = datetime(2023, 12, 31)
SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']  # Example stocks