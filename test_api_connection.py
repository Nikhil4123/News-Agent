import requests
import os

# Function to write results to file
def write_result(message):
    with open('test_results.txt', 'a', encoding='utf-8') as f:
        f.write(message + '\n')
    print(message)

# Read API key
api_key = None
try:
    with open('config.txt', 'r') as f:
        for line in f:
            if line.startswith('NEWS_API_KEY='):
                api_key = line.strip().split('=', 1)[1].strip()
                break
except Exception as e:
    write_result(f"Error reading config: {e}")

if not api_key:
    write_result("No API key found")
else:
    write_result(f"API key found: {api_key[:5]}...")
    
    # Test API call
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': 'in',
        'apiKey': api_key,
        'pageSize': '2'
    }
    
    try:
        write_result("Making test API call...")
        response = requests.get(url, params=params, timeout=10)
        write_result(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            write_result(f"Status: {data.get('status')}")
            write_result(f"Total results: {data.get('totalResults')}")
            if data.get('articles'):
                write_result(f"Articles received: {len(data['articles'])}")
                for i, article in enumerate(data['articles']):
                    title = article.get('title', 'No title')
                    write_result(f"  {i+1}. {title}")
            else:
                write_result("No articles in response")
        else:
            write_result(f"Error: {response.text}")
    except Exception as e:
        write_result(f"Request failed: {e}")

write_result("\nTest completed.")