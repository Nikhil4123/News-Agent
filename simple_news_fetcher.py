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

def get_indian_news(api_key):
    """Fetch top headlines from Indian news sources"""
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'sources': 'google-news-in',
        'apiKey': api_key,
        'pageSize': '10'
    }
    
    try:
        print("Making request to NewsAPI...")
        response = requests.get(url, params=params)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'ok' and data.get('articles'):
                print(f"Found {len(data['articles'])} articles")
                return data['articles']
            else:
                print("API returned no articles")
        else:
            print(f"API request failed with status {response.status_code}")
            
    except Exception as e:
        print(f"Error fetching news: {e}")
    
    return []

def save_news_for_youtube(articles):
    """Save news data to a text file for YouTube video creation"""
    with open('youtube_news_content.txt', 'w', encoding='utf-8') as f:
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
    
    print("News content saved to: youtube_news_content.txt")

def main():
    print("Starting Indian News Fetcher...")
    
    # Get API key
    api_key = get_api_key_from_config()
    if not api_key:
        print("No API key found!")
        return
    
    print("API key found, fetching news...")
    articles = get_indian_news(api_key)
    save_news_for_youtube(articles)
    print("Done!")

if __name__ == "__main__":
    main()