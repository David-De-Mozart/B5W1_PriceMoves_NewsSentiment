import pandas as pd
from config import SYMBOLS
from src.data_loader import load_news_data, load_all_stock_data
from src.text_analyzer import analyze_text
from src.technical_analyzer import calculate_technical_indicators
from src.correlation_engine import calculate_correlations
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def run_analysis():
    print("Starting Task 1: Loading and preprocessing data...")
    news_df = load_news_data()
    
    # Task 1: Basic EDA
    print("\nPerforming EDA...")
    # Publisher analysis
    publisher_counts = news_df['publisher'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    publisher_counts.plot(kind='bar', color='teal')
    plt.title('Top 10 Publishers by Article Count')
    plt.ylabel('Number of Articles')
    plt.tight_layout()
    plt.savefig("reports/figures/publisher_distribution.png")
    plt.close()
    
    # Temporal analysis
    news_df['hour'] = news_df['date'].dt.hour
    news_df['day_of_week'] = news_df['date'].dt.day_name()
    
    plt.figure(figsize=(12, 6))
    news_df['hour'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title('Article Publication by Hour of Day')
    plt.xlabel('Hour of Day (UTC)')
    plt.ylabel('Number of Articles')
    plt.tight_layout()
    plt.savefig("reports/figures/hourly_distribution.png")
    plt.close()
    
    # Task 2: Text analysis
    print("\nPerforming sentiment analysis...")
    news_df, keywords_df = analyze_text(news_df)
    
    # Task 3: Stock analysis
    print("\nLoading stock data...")
    stock_data = load_all_stock_data(SYMBOLS)
    
    print("\nCalculating technical indicators...")
    stock_data = calculate_technical_indicators(stock_data)
    
    # Task 4: Correlation analysis
    print("\nAnalyzing correlations...")
    correlation_results = calculate_correlations(news_df, stock_data)
    
    # Save final results
    correlation_results.to_csv("reports/figures/correlation_results.csv", index=False)
    
    # Generate summary report
    print("\nGenerating final report...")
    generate_report(news_df, correlation_results)
    
    print("\nAnalysis complete! Results saved to reports/figures/")

def generate_report(news_df, correlation_results):
    """Generate a text summary report"""
    with open("reports/analysis_report.txt", "w") as f:
        f.write("Financial News Sentiment Analysis Report\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        f.write("1. Dataset Overview\n")
        f.write(f"- Time period: {news_df['date'].min().date()} to {news_df['date'].max().date()}\n")
        f.write(f"- Total articles: {len(news_df):,}\n")
        f.write(f"- Unique stocks covered: {news_df['stock'].nunique()}\n")
        f.write(f"- Unique publishers: {news_df['publisher'].nunique()}\n\n")
        
        f.write("2. Key Findings\n")
        f.write(f"- Average sentiment score: {news_df['sentiment'].mean():.3f}\n")
        f.write("- Sentiment distribution:\n")
        f.write(f"  - Positive (>0.1): {(news_df['sentiment'] > 0.1).sum() / len(news_df):.1%}\n")
        f.write(f"  - Neutral (-0.1 to 0.1): {(news_df['sentiment'].between(-0.1, 0.1)).sum() / len(news_df):.1%}\n")
        f.write(f"  - Negative (<-0.1): {(news_df['sentiment'] < -0.1).sum() / len(news_df):.1%}\n\n")
        
        f.write("3. Correlation Insights\n")
        f.write("- Correlation between sentiment and stock returns:\n")
        for _, row in correlation_results.iterrows():
            f.write(f"  - {row['symbol']}: Same-day: {row['same_day_corr']:.3f}, Next-day: {row['next_day_corr']:.3f}\n")
        
        f.write("\n4. Trading Strategy Recommendations\n")
        f.write("- For stocks with high sentiment-return correlation (>0.2):\n")
        f.write("  - Consider sentiment as a confirming indicator for trades\n")
        f.write("  - Enter long positions when sentiment is strongly positive\n")
        f.write("  - Consider short positions when sentiment is strongly negative\n")
        f.write("- For stocks with low correlation (<0.1):\n")
        f.write("  - Sentiment may not be a reliable predictor\n")
        f.write("  - Focus on technical indicators instead\n\n")
        
        f.write("5. Limitations and Future Work\n")
        f.write("- Current analysis uses only headlines; full article analysis may improve results\n")
        f.write("- No sector-specific analysis performed\n")
        f.write("- Sentiment analysis doesn't account for sarcasm or complex financial language\n")

if __name__ == "__main__":
    run_analysis()