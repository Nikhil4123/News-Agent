#!/usr/bin/env python3
"""
NewsAPI.org Fetcher
Fetches Indian news from NewsAPI.org
"""

import requests
from typing import List, Dict


def get_indian_news(api_key: str) -> List[Dict]:
    """
    Fetch top headlines from Indian news sources using NewsAPI.org
    
    Args:
        api_key: NewsAPI.org API key
    
    Returns:
        List of news articles
    """
    # Try different sources to get better quality articles
    sources = [
        {'country': 'in'},  # India (broader search)
        {'sources': 'google-news-in'},  # Google News India
        {'q': 'India'},  # Search for India
    ]
    
    all_articles = []
    
    for source_params in sources:
        url = "https://newsapi.org/v2/top-headlines"
        params = source_params.copy()
        params['apiKey'] = api_key
        params['pageSize'] = '20'
        
        try:
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'ok' and data.get('articles'):
                    # Filter out generic "Google News" titles
                    filtered_articles = [
                        article for article in data['articles']
                        if article.get('title') and not article['title'].startswith('Google News')
                    ]
                    all_articles.extend(filtered_articles)
                    
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news from NewsAPI.org: {e}")
    
    # Remove duplicates based on title
    seen_titles = set()
    unique_articles = []
    for article in all_articles:
        title = article.get('title', '').strip()
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append(article)
    
    # Return top 10 unique articles
    return unique_articles[:10] if unique_articles else []

