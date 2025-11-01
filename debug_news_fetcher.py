#!/usr/bin/env python3
"""
Debug version of the Indian News Fetcher to troubleshoot issues
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
                        print(f"Found API key: {api_key[:5]}***")  # Show only first 5 chars
                        return api_key
    except FileNotFoundError:
        print("config.txt file not found.")
    except Exception as e:
        print(f"Error reading config file: {e}")
    return None

def get_indian_news(api_key):
    """Fetch top headlines from Indian news sources"""
    print("Fetching news from NewsAPI...")
    
    # Try country-specific first (better quality articles)
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': 'in',
        'apiKey': api_key,
        'pageSize': '10'
    }
    
    try:
        print(f"Making request to: {url}")
        print(f"Parameters: {params}")
        response = requests.get(url, params=params)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"API Response Status: {data.get('status')}")
            print(f"Total Results: {data.get('totalResults', 0)}")
            
            if data['status'] == 'ok' and data.get('articles'):
                articles = data['articles']
                print(f"Received {len(articles)} articles")
                
                # Print first few article titles to see what we're getting
                print("\nFirst 5 article titles:")
                for i, article in enumerate(articles[:5]):
                    title = article.get('title', 'No title')
                    source = article.get('source', {}).get('name', 'Unknown source')
                    print(f"  {i+1}. {title} (Source: {source})")
                
                # Filter out generic titles
                filtered_articles = [
                    article for article in articles 
                    if article.get('title') and not article['title'].startswith('Google News')
                ]
                print(f"\nAfter filtering: {len(filtered_articles)} articles")
                
                return filtered_articles
            else:
                print(f"API returned error: {data.get('message', 'Unknown error')}")
        else:
            print(f"HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error fetching news: {e}")
        import traceback
        traceback.print_exc()
    
    return []

def save_news_for_youtube(articles):
    """Save news data to a text file for YouTube video creation"""
    with open('debug_youtube_news_content.txt', 'w', encoding='utf-8') as f:
        f.write(f"TOP NEWS FROM INDIA - {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("=" * 50 + "\n\n")
        
        if not articles:
            f.write("No articles found.\n")
            return
            
        for i, article in enumerate(articles[:10], 1):
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
    
    print("News content saved to: debug_youtube_news_content.txt")

def main():
    print("🔍 Debug Indian News Fetcher")
    print("=" * 40)
    
    # Get API key
    api_key = get_api_key_from_config()
    if not api_key:
        print("❌ No API key found!")
        return
    
    # Fetch news
    articles = get_indian_news(api_key)
    
    # Save to file
    save_news_for_youtube(articles)
    
    print("\n✅ Debug complete!")

if __name__ == "__main__":
    main()