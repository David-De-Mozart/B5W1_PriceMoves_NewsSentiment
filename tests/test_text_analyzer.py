from src.text_analyzer import extract_keywords
import pandas as pd

def test_keyword_extraction():
    """Test keyword extraction from headlines"""
    headlines = pd.Series([
        'Apple stock rises on strong earnings',
        'Microsoft falls after weak guidance',
        'FDA approves new diabetes drug'
    ])
    keywords = extract_keywords(headlines)
    assert len(keywords) > 0
    assert 'apple' in keywords.index
    assert 'fda' in keywords.index