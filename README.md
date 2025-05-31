
📊 README: Predicting Price Moves with News Sentiment

🌟 Project Overview
This project analyzes how financial news sentiment impacts stock price movements. By combining Natural Language Processing (NLP) techniques with quantitative financial analysis, we develop a pipeline that:

1. Processes financial news headlines

2. Quantifies sentiment scores

3. Calculates technical indicators

4. Measures correlations between news sentiment and stock returns

5. Generates actionable trading insights

Business Value: Enables Nova Financial Solutions to enhance predictive analytics capabilities for improved financial forecasting.

📂 Project Structure

B5W1_PriceMoves_NewsSentiment/
├── data/                   # Raw and processed datasets
├── reports/                # Analysis outputs
│   ├── figures/            # Visualizations
│   └── analysis_report.txt # Final insights
├── src/                    # Source code
│   ├── data_loader.py      # Data ingestion/preprocessing
│   ├── text_analyzer.py    # Sentiment analysis
│   ├── technical_analyzer.py # Stock indicators
│   └── correlation_engine.py # Statistical analysis
├── main.py                 # Execution entry point
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

🚀 Installation

1. Clone repository:


git clone https://github.com/David-De-Mozart/B5W1_PriceMoves_NewsSentiment.git
cd B5W1_PriceMoves_NewsSentiment

2. Create virtual environment:


python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Install dependencies:


pip install -r requirements.txt


🧪 Usage

Run the complete analysis pipeline:

python main.py


Key Execution Steps:

1. Data Loading: Ingests financial news and stock data

2. Preprocessing: Cleans and transforms raw data

3. Exploratory Analysis: Generates insights about news patterns

4. Sentiment Analysis: Quantifies news tone using NLP

5. Technical Analysis: Calculates stock indicators (MA, RSI, MACD)

6. Correlation Analysis: Measures news sentiment vs. stock returns

7. Report Generation: Creates actionable insights in publication-ready format


📊 Key Outputs


After running the analysis, check these files:

1. Visualizations (reports/figures/):

        -publisher_distribution.png: Top news sources

        -hourly_distribution.png: News publication frequency

        -top_keywords.png: Most frequent financial terms

        -AAPL_technical_indicators.png: Sample technical analysis

        -AAPL_sentiment_correlation.png: Sentiment vs. returns

        -overall_correlations.png: Cross-stock comparison

2. Data Results:

        -correlation_results.csv: Statistical correlations

3. Final Report:

        -analysis_report.txt: Comprehensive insights and recommendations


📈 Key Insights (Sample)

The analysis revealed:

1. 65% of financial news is published between 2-4 PM UTC

2. "Earnings", "Target", and "Upgrade" are top keywords

3. AAPL shows 0.32 correlation between sentiment and same-day returns

4. Technical indicators provide strongest signals when combined with sentiment

5. Optimal trading strategy:

        -Enter long positions when sentiment > 0.2 & 50MA > 200MA

        -Exit when RSI > 70


🔧 Customization

To analyze different stocks:

1. Edit config.py:

SYMBOLS = ['TSLA', 'JPM', 'NVDA']  # Your target stocks
START_DATE = datetime(2022, 1, 1)   # New date range
END_DATE = datetime(2023, 12, 31)

2. Place your financial_news.csv in data/ folder

3. Run python main.py