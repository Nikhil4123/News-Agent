#!/usr/bin/env python3
"""
Better news fetcher that tries multiple sources to get quality titles
"""

import requests
import os
from datetime import datetime

def get_api_key_from_config():
    """Read API key from config.txt file"""
    try:
        with open('config.txt', 'r') as f:
            for line in f:
                if line.startswith('NEWS_API_KEY='):
                    api_key = line.strip().split('=', 1)[1]
                    api_key = api_key.strip('"\'')
                    if api_key:
                        return api_key
    except FileNotFoundError:
        print("config.txt file not found.")
    except Exception as e:
        print(f"Error reading config file: {e}")
    return None

def get_top_indian_news_sources(api_key):
    """Get a list of Indian news sources"""
    url = "https://newsapi.org/v2/sources"
    params = {
        'category': 'general',
        'country': 'in',
        'apiKey': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'ok':
                sources = [source['id'] for source in data['sources']]
                print(f"Found {len(sources)} Indian news sources: {sources}")
                return sources
    except Exception as e:
        print(f"Error fetching sources: {e}")
    
    # Fallback to known Indian news sources
    return ['the-times-of-india', 'the-hindu', 'google-news-in']

def get_articles_from_sources(api_key, sources):
    """Fetch articles from specific sources"""
    all_articles = []
    
    for source in sources[:3]:  # Limit to first 3 sources
        print(f"Fetching from source: {source}")
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            'sources': source,
            'apiKey': api_key,
            'pageSize': '5'
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'ok' and data.get('articles'):
                    # Add source info to articles
                    for article in data['articles']:
                        if article.get('title') and not article['title'].startswith('Google News'):
                            all_articles.append(article)
                            if len(all_articles) >= 15:  # Limit total articles
                                return all_articles
        except Exception as e:
            print(f"Error fetching from {source}: {e}")
    
    return all_articles

def get_country_news(api_key):
    """Fetch news using country parameter"""
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': 'in',
        'apiKey': api_key,
        'pageSize': '15'
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'ok' and data.get('articles'):
                # Filter out generic titles
                filtered_articles = [
                    article for article in data['articles'] 
                    if article.get('title') and not article['title'].startswith('Google News')
                ]
                return filtered_articles
    except Exception as e:
        print(f"Error fetching country news: {e}")
    
    return []

def save_better_news(articles):
    """Save improved news data to file"""
    with open('better_youtube_news_content.txt', 'w', encoding='utf-8') as f:
        f.write(f"TOP NEWS FROM INDIA - {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("=" * 50 + "\n\n")
        
        if not articles:
            f.write("No articles found.\n")
            return
            
        for i, article in enumerate(articles[:15], 1):
            title = article.get('title', 'No title')
            source = article['source']['name'] if article.get('source') else 'Unknown source'
            published_at = article.get('publishedAt', '')[:19].replace('T', ' ') if article.get('publishedAt') else 'Unknown date'
            description = article.get('description', 'No description available.')
            url = article.get('url', 'No URL available')
            
            f.write(f"{i}. {title}\n")
            f.write(f"   Source: {source}\n")
            f.write(f"   Published: {published_at}\n")
            f.write(f"   Description: {description}\n")
            f.write(f"   Link: {url}\n\n")
    
    print("Better news content saved to: better_youtube_news_content.txt")

def main():
    print("🌟 Better Indian News Fetcher")
    print("=" * 40)
    
    # Get API key
    api_key = get_api_key_from_config()
    if not api_key:
        print("❌ No API key found!")
        return
    
    print("✅ API key found")
    
    # Method 1: Try specific sources
    print("\n1. Trying specific Indian news sources...")
    sources = get_top_indian_news_sources(api_key)
    articles = get_articles_from_sources(api_key, sources)
    
    # Method 2: If not enough articles, try country method
    if len(articles) < 5:
        print("\n2. Trying country-based search...")
        country_articles = get_country_news(api_key)
        articles.extend(country_articles)
    
    # Remove duplicates
    seen_titles = set()
    unique_articles = []
    for article in articles:
        title = article.get('title', '').strip()
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append(article)
    
    print(f"\n📊 Total unique articles: {len(unique_articles)}")
    
    # Display sample
    print("\n📰 Sample articles:")
    for i, article in enumerate(unique_articles[:5], 1):
        print(f"  {i}. {article.get('title', 'No title')}")
    
    # Save to file
    save_better_news(unique_articles)

if __name__ == "__main__":
    main()