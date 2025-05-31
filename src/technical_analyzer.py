import numpy as np  # ADD THIS IMPORT
import pandas as pd
from ta import add_all_ta_features
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator
from ta.volatility import BollingerBands
from config import REPORTS_DIR
import matplotlib.pyplot as plt

def calculate_technical_indicators(stock_data):
    """Calculate technical indicators for stock data with robust return calculation"""
    indicators_data = {}
    
    for symbol, data in stock_data.items():
        # Skip if no data
        if data.empty:
            print(f"Skipping {symbol} - no stock data available")
            continue
            
        # Ensure we have required columns
        if 'Close' not in data.columns:
            print(f"Skipping {symbol} - missing 'Close' column")
            continue
            
        # Calculate returns with NaN handling
        data['daily_return'] = data['Close'].pct_change()
        data['daily_return'] = data['daily_return'].replace([np.inf, -np.inf], np.nan)
        
        # Only proceed if we have at least 50 data points
        if len(data) < 50:
            print(f"Insufficient data for {symbol} ({len(data)} rows)")
            continue
            
        # Moving averages
        data['MA50'] = SMAIndicator(data['Close'], window=50).sma_indicator()
        data['MA200'] = SMAIndicator(data['Close'], window=200).sma_indicator()
        
        # RSI
        data['RSI'] = RSIIndicator(data['Close'], window=14).rsi()
        
        # MACD
        macd = MACD(data['Close'])
        data['MACD'] = macd.macd()
        data['Signal'] = macd.macd_signal()
        
        # Bollinger Bands
        bb = BollingerBands(data['Close'])
        data['BB_upper'] = bb.bollinger_hband()
        data['BB_lower'] = bb.bollinger_lband()
        
        indicators_data[symbol] = data
        
        # Save sample visualization for each stock
        if symbol == 'AAPL':  # Just for one stock to avoid too many files
            plt.figure(figsize=(14, 10))
            
            # Price and MAs
            plt.subplot(3, 1, 1)
            plt.plot(data.index, data['Close'], label='Close Price', alpha=0.7)
            plt.plot(data.index, data['MA50'], label='50-day MA', linestyle='--')
            plt.plot(data.index, data['MA200'], label='200-day MA', linestyle='-.')
            plt.title(f'{symbol} Price and Moving Averages')
            plt.legend()
            
            # RSI
            plt.subplot(3, 1, 2)
            plt.plot(data.index, data['RSI'], label='RSI', color='purple')
            plt.axhline(70, color='r', linestyle='--')
            plt.axhline(30, color='g', linestyle='--')
            plt.title('Relative Strength Index (RSI)')
            
            # MACD
            plt.subplot(3, 1, 3)
            plt.plot(data.index, data['MACD'], label='MACD', color='blue')
            plt.plot(data.index, data['Signal'], label='Signal', color='orange')
            plt.title('MACD')
            
            plt.tight_layout()
            plt.savefig(f"{REPORTS_DIR}/{symbol}_technical_indicators.png")
            plt.close()
    
    return indicators_data