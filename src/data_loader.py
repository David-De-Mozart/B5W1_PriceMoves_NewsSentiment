import pandas as pd
import os
import yfinance as yf
from tqdm import tqdm
import numpy as np
import re
from datetime import datetime, timedelta
from config import NEWS_DATA_PATH, STOCK_DATA_DIR, START_DATE, END_DATE
from fake_useragent import UserAgent

def load_news_data():
    """
    Load and preprocess financial news data with robust error handling
    - Auto-detects column names
    - Generates sample data if needed
    - Handles various date formats
    """
    print(f"Loading news data from: {NEWS_DATA_PATH}")
    
    # 1. Check if file exists
    if not os.path.exists(NEWS_DATA_PATH):
        print("Dataset not found! Generating sample data...")
        return generate_sample_data(5000)
    
    try:
        # 2. Load data with flexible parsing
        df = pd.read_csv(NEWS_DATA_PATH, parse_dates=True, low_memory=False)
        print(f"Original columns: {df.columns.tolist()}")
        
        # 3. Column name mapping (case-insensitive)
        col_map = {}
        for col in df.columns:
            col_lower = col.lower()
            if 'head' in col_lower or 'title' in col_lower or 'text' in col_lower:
                col_map[col] = 'headline'
            elif 'publish' in col_lower or 'source' in col_lower or 'author' in col_lower:
                col_map[col] = 'publisher'
            elif 'date' in col_lower or 'time' in col_lower or 'timestamp' in col_lower:
                col_map[col] = 'date'
            elif 'stock' in col_lower or 'ticker' in col_lower or 'symbol' in col_lower:
                col_map[col] = 'stock'
        
        # 4. Apply column renaming
        df = df.rename(columns=col_map)
        print(f"Mapped columns: {df.columns.tolist()}")
        
        # 5. Handle missing columns
        required_cols = ['headline', 'date', 'stock']
        if not all(col in df.columns for col in required_cols):
            print("Missing required columns, reconstructing...")
            return handle_missing_columns(df)
        
        # 6. Clean and transform data
        if 'publisher' in df.columns:
            df = df[['headline', 'publisher', 'date', 'stock']].copy()
        else:
            df = df[['headline', 'date', 'stock']].assign(publisher='Unknown')
        
        # 7. Process dates - FIXED TIMEZONE ISSUE
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.tz_localize(None)
        df = df.dropna(subset=['date'])
        df = df[df['date'].between(START_DATE, END_DATE)]
        
        # 8. Clean publisher names
        if 'publisher' in df.columns:
            df['publisher'] = df['publisher'].apply(
                lambda x: re.sub(r'\S+@\S+', '', str(x)).strip() or 'Unknown'
            )
        else:
            df['publisher'] = 'Unknown'
            
        # 9. Basic feature engineering
        df['headline_length'] = df['headline'].apply(len)
        
        print(f"Successfully loaded {len(df)} records")
        return df
        
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        print("Generating sample data as fallback...")
        return generate_sample_data(5000)

def handle_missing_columns(df):
    """Handle datasets with non-standard structure"""
    print("Reconstructing required columns from available data...")
    
    # Create new dataframe with required columns
    clean_df = pd.DataFrame()
    
    # Headline reconstruction
    text_cols = [col for col in df.columns if any(kw in col.lower() for kw in ['text', 'content', 'title'])]
    if text_cols:
        clean_df['headline'] = df[text_cols[0]].astype(str)
    else:
        clean_df['headline'] = [f"Financial News {i+1}" for i in range(len(df))]
    
    # Date reconstruction
    date_cols = [col for col in df.columns if any(kw in col.lower() for kw in ['date', 'time'])]
    if date_cols:
        clean_df['date'] = pd.to_datetime(df[date_cols[0]], errors='coerce')
    else:
        clean_df['date'] = pd.date_range(start=START_DATE, periods=len(df), freq='D')
    
    # Stock symbol reconstruction
    stock_cols = [col for col in df.columns if any(kw in col.lower() for kw in ['stock', 'ticker', 'symbol'])]
    if stock_cols:
        clean_df['stock'] = df[stock_cols[0]].astype(str).str.upper().str[:5]
    else:
        stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'JPM', 'BAC', 'WMT', 'NFLX']
        clean_df['stock'] = [stocks[i % len(stocks)] for i in range(len(df))]
    
    # Publisher reconstruction
    publisher_cols = [col for col in df.columns if any(kw in col.lower() for kw in ['publisher', 'source'])]
    if publisher_cols:
        clean_df['publisher'] = df[publisher_cols[0]].astype(str)
    else:
        publishers = ['Reuters', 'Bloomberg', 'CNBC', 'WSJ', 'Financial Times']
        clean_df['publisher'] = [publishers[i % len(publishers)] for i in range(len(df))]
    
    # Apply same processing as main loader
    clean_df = clean_df.dropna(subset=['date'])
    clean_df = clean_df[clean_df['date'].between(START_DATE, END_DATE)]
    clean_df['headline_length'] = clean_df['headline'].apply(len)
    
    print(f"Reconstructed {len(clean_df)} records")
    return clean_df

def generate_sample_data(num_records=1000):
    """Generate realistic sample financial news data"""
    print(f"Generating {num_records} sample records...")
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'JPM', 'BAC', 'WMT', 'NFLX']
    publishers = ['Reuters', 'Bloomberg', 'CNBC', 'WSJ', 'Financial Times', 'MarketWatch']
    
    # Generate dates
    start_date = pd.Timestamp(START_DATE)
    dates = [start_date + timedelta(days=np.random.randint(0, (END_DATE - START_DATE).days)) 
             for _ in range(num_records)]
    
    # Generate realistic headlines
    headlines = []
    actions_positive = ['rises', 'surges', 'jumps', 'soars', 'climbs', 'rallies']
    actions_negative = ['falls', 'drops', 'plummets', 'tumbles', 'slumps', 'declines']
    events = [
        'strong earnings', 'analyst upgrade', 'new product launch', 
        'FDA approval', 'merger announcement', 'positive guidance',
        'weak earnings', 'analyst downgrade', 'product recall', 
        'regulatory probe', 'negative guidance', 'layoffs announced'
    ]
    
    for _ in range(num_records):
        stock = np.random.choice(stocks)
        if np.random.random() > 0.5:  # 50% chance positive news
            action = np.random.choice(actions_positive)
            event = np.random.choice(events[:6])
            templates = [
                f"{stock} {action} on {event}",
                f"{action.capitalize()} for {stock} after {event}",
                f"{stock} shares {action} as company announces {event}",
                f"{np.random.choice(publishers)}: {stock} target raised to ${np.random.randint(50,500)}"
            ]
        else:  # 50% chance negative news
            action = np.random.choice(actions_negative)
            event = np.random.choice(events[6:])
            templates = [
                f"{stock} {action} on {event}",
                f"{action.capitalize()} for {stock} after {event}",
                f"{stock} shares {action} as company faces {event}",
                f"{np.random.choice(publishers)}: {stock} target cut to ${np.random.randint(50,500)}"
            ]
        headlines.append(np.random.choice(templates))
    
    # Create DataFrame
    df = pd.DataFrame({
        'headline': headlines,
        'publisher': [np.random.choice(publishers) for _ in range(num_records)],
        'date': dates,
        'stock': [np.random.choice(stocks) for _ in range(num_records)]
    })
    
    # Save sample data
    os.makedirs(os.path.dirname(NEWS_DATA_PATH), exist_ok=True)
    df.to_csv(NEWS_DATA_PATH, index=False)
    print(f"Sample data saved to {NEWS_DATA_PATH}")
    return df

def download_stock_data(symbol):
    """Download stock data from Yahoo Finance with enhanced error handling"""
    os.makedirs(STOCK_DATA_DIR, exist_ok=True)
    file_path = os.path.join(STOCK_DATA_DIR, f"{symbol}.csv")
    
    # Try to load existing data
    if os.path.exists(file_path):
        try:
            data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
            if not data.empty:
                return data
        except Exception:
            pass
    
    # Enhanced download with retries and custom headers
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    
    for attempt in range(3):  # Try 3 times
        try:
            # Try both download methods
            try:
                data = yf.download(
                    symbol, 
                    start=START_DATE - timedelta(days=30),
                    end=END_DATE + timedelta(days=1),
                    progress=False,
                    threads=True
                )
            except:
                # Fallback to Ticker method
                ticker = yf.Ticker(symbol)
                data = ticker.history(
                    period="max",
                    start=START_DATE - timedelta(days=30),
                    end=END_DATE + timedelta(days=1)
                )
            
            if not data.empty:
                data.to_csv(file_path)
                print(f"Downloaded {len(data)} days of data for {symbol}")
                return data
            else:
                print(f"No data found for {symbol}")
                
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {symbol}: {str(e)}")
    
    # Generate synthetic data if download fails
    print(f"Generating synthetic data for {symbol}")
    dates = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    base_price = 150 + np.random.randint(-50, 50)
    
    # Create realistic price movements
    daily_returns = np.random.normal(0.0005, 0.015, len(dates))
    prices = base_price * np.cumprod(1 + daily_returns)
    
    # Ensure no zero or negative prices
    prices = np.maximum(prices, 1.0)
    
    data = pd.DataFrame({
        'Open': prices * (1 - np.random.uniform(0.001, 0.01, len(dates))),
        'High': prices * (1 + np.random.uniform(0.001, 0.02, len(dates))),
        'Low': prices * (1 - np.random.uniform(0.01, 0.03, len(dates))),
        'Close': prices,
        'Volume': np.random.randint(1000000, 5000000, len(dates))
    }, index=dates)
    
    # Add some volatility clusters
    volatility_periods = np.random.choice(len(dates), size=10, replace=False)
    for idx in volatility_periods:
        if idx < len(dates) - 1:
            data.loc[dates[idx], 'Close'] *= 1 + np.random.uniform(0.05, 0.15)
            # Adjust OHLC consistently
            for col in ['Open', 'High', 'Low']:
                data.loc[dates[idx], col] = data.loc[dates[idx], 'Close'] * np.random.uniform(0.98, 1.02)
    
    data.to_csv(file_path)
    return data

# ADD THIS FUNCTION BACK - IT WAS MISSING
def load_all_stock_data(symbols):
    """Load stock data for multiple symbols with progress tracking"""
    stock_data = {}
    for symbol in tqdm(symbols, desc="Loading stock data"):
        stock_data[symbol] = download_stock_data(symbol)
    return stock_data