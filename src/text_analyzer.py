import pandas as pd
from textblob import TextBlob
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from config import REPORTS_DIR
import matplotlib.pyplot as plt

nltk.download('stopwords')

def analyze_text(df):
    """Perform text analysis on headlines"""
    # Sentiment analysis
    df['sentiment'] = df['headline'].apply(
        lambda x: TextBlob(str(x)).sentiment.polarity
    )
    
    # Keyword extraction
    stop_words = set(stopwords.words('english'))
    custom_stopwords = {'said', 'new', 'us', 'will', 'says', 'company', 'stock'}
    all_words = []
    
    for headline in df['headline']:
        words = re.findall(r'\b\w+\b', str(headline).lower())
        filtered = [word for word in words if (
            word not in stop_words and 
            word not in custom_stopwords and 
            len(word) > 2 and
            not word.isdigit()
        )]
        all_words.extend(filtered)
    
    # Get top 20 keywords
    keyword_counts = Counter(all_words).most_common(20)
    keywords_df = pd.DataFrame(keyword_counts, columns=['Keyword', 'Count'])
    
    # Save keyword plot
    plt.figure(figsize=(10, 6))
    keywords_df.set_index('Keyword')['Count'].plot(kind='barh', color='skyblue')
    plt.title('Top 20 Keywords in Financial Headlines')
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/top_keywords.png")
    plt.close()
    
    return df, keywords_df