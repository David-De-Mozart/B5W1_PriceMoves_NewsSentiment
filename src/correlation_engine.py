import pandas as pd
import numpy as np
from config import REPORTS_DIR
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def calculate_correlations(news_df, stock_data):
    """Calculate correlations between sentiment and stock returns with robust error handling"""
    results = []
    
    # Return empty DataFrame if no stock data
    if not stock_data:
        print("No stock data available for correlation analysis")
        return pd.DataFrame()
    
    for symbol, data in stock_data.items():
        # Skip if no stock data
        if data.empty:
            print(f"Skipping {symbol} - no stock data available")
            continue
            
        # Get relevant news
        stock_news = news_df[news_df['stock'] == symbol].copy()
        if stock_news.empty:
            print(f"No news found for {symbol}")
            continue
            
        try:
            # Prepare stock data
            data.index = pd.to_datetime(data.index).normalize()
            
            # Aggregate sentiment by day
            stock_news['date'] = pd.to_datetime(stock_news['date']).dt.normalize()
            daily_sentiment = stock_news.groupby('date')['sentiment'].agg(['mean', 'count'])
            daily_sentiment.columns = ['avg_sentiment', 'article_count']
            
            # Merge with stock data
            merged = data.merge(daily_sentiment, left_index=True, right_index=True, how='left')
            
            # Fill missing sentiment with 0 (neutral)
            merged['avg_sentiment'].fillna(0, inplace=True)
            
            # Calculate returns with NaN handling
            merged['daily_return'] = merged['Close'].pct_change()
            merged.replace([np.inf, -np.inf], np.nan, inplace=True)
            merged.dropna(subset=['daily_return', 'avg_sentiment'], inplace=True)
            
            # Skip if insufficient data
            if len(merged) < 2:
                print(f"Not enough data for {symbol} to compute correlation")
                continue
            
            # Calculate correlations
            valid_data = merged.dropna(subset=['avg_sentiment', 'daily_return'])
            if len(valid_data) < 2:
                print(f"Insufficient valid data for {symbol}")
                continue
                
            same_day_corr, _ = pearsonr(valid_data['avg_sentiment'], valid_data['daily_return'])
            
            # Next-day correlation
            next_returns = merged['daily_return'].shift(-1).fillna(0)
            next_valid_data = merged.dropna(subset=['avg_sentiment'])
            if len(next_valid_data) > 1:
                next_day_corr, _ = pearsonr(next_valid_data['avg_sentiment'], 
                                           next_returns.loc[next_valid_data.index])
            else:
                next_day_corr = np.nan

            results.append({
                'symbol': symbol,
                'same_day_corr': same_day_corr,
                'next_day_corr': next_day_corr,
                'avg_sentiment': merged['avg_sentiment'].mean(),
                'articles': len(stock_news)
            })
            
            # Plot for one stock
            if symbol == 'AAPL' and not merged.empty:
                plt.figure(figsize=(12, 6))
                sns.regplot(x='avg_sentiment', y='daily_return', data=merged, 
                            scatter_kws={'alpha':0.3}, line_kws={'color':'red'})
                plt.title(f'{symbol} Sentiment vs Daily Returns (r={same_day_corr:.2f})')
                plt.xlabel('Average Daily Sentiment')
                plt.ylabel('Daily Return')
                plt.savefig(f"{REPORTS_DIR}/{symbol}_sentiment_correlation.png")
                plt.close()
        
        except Exception as e:
            print(f"Error processing {symbol}: {str(e)}")
    
    # Return results if any, otherwise empty DataFrame
    if results:
        return pd.DataFrame(results)
    else:
        print("No valid correlation results generated")
        return pd.DataFrame()