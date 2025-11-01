#!/usr/bin/env python3
"""
Simple API test for NewsAPI
"""

import requests
import os

def test_api_key():
    """Test if we can read the API key"""
    try:
        with open('config.txt', 'r') as f:
            content = f.read()
            print(f"Config file content: {repr(content)}")
            
            if content.startswith('NEWS_API_KEY='):
                api_key = content.strip().split('=', 1)[1].strip()
                print(f"API Key: {api_key}")
                return api_key
    except FileNotFoundError:
        print("config.txt not found")
    except Exception as e:
        print(f"Error: {e}")
    return None

def test_api_call(api_key):
    """Test a simple API call"""
    if not api_key:
        print("No API key provided")
        return
        
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': 'in',
        'apiKey': api_key,
        'pageSize': '5'
    }
    
    print(f"Testing API call to: {url}")
    print(f"Parameters: {params}")
    
    try:
        response = requests.get(url, params=params)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Total Results: {data.get('totalResults')}")
            
            if data.get('articles'):
                print(f"Number of articles: {len(data['articles'])}")
                print("\nFirst article:")
                if data['articles']:
                    article = data['articles'][0]
                    print(f"  Title: {article.get('title')}")
                    print(f"  Source: {article.get('source', {}).get('name')}")
                    print(f"  Published: {article.get('publishedAt')}")
            else:
                print("No articles found")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Testing NewsAPI Connection")
    print("=" * 40)
    
    api_key = test_api_key()
    test_api_call(api_key)