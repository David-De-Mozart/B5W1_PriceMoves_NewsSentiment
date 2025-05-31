import pytest
from src.data_loader import load_news_data, generate_sample_data
import os
from config import NEWS_DATA_PATH

def test_sample_data_generation():
    """Test synthetic data generation"""
    df = generate_sample_data(100)
    assert len(df) == 100
    assert set(df.columns) == {'headline', 'publisher', 'date', 'stock'}
    assert os.path.exists(NEWS_DATA_PATH)

def test_data_loading(tmp_path):
    """Test data loading with mock file"""
    # Create temporary test data
    test_data = """headline,publisher,date,stock
    'Apple hits record high','Bloomberg','2023-01-01','AAPL'
    'Microsoft earnings beat estimates','Reuters','2023-01-02','MSFT'"""
    
    test_file = tmp_path / "test_financial_news.csv"
    test_file.write_text(test_data)
    
    # Test loading
    df = load_news_data()
    assert len(df) > 0
    assert 'headline' in df.columns