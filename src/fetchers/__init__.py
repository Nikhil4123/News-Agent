"""
News API Fetchers Module
"""

from .newsapi_fetcher import get_indian_news as get_newsapi_articles
from .newsdata_fetcher import NewsDataFetcher

__all__ = ['get_newsapi_articles', 'NewsDataFetcher']

