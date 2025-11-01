import requests
from datetime import datetime
import os
import html
import json
import re

def get_api_key_from_config():
    """
    Read API key from config.txt file
    """
    try:
        with open('config.txt', 'r') as f:
            for line in f:
                if line.startswith('NEWS_API_KEY='):
                    api_key = line.strip().split('=', 1)[1]
                    # Remove any quotes around the API key
                    api_key = api_key.strip('"\'')
                    if api_key:
                        return api_key
    except FileNotFoundError:
        print("config.txt file not found.")
    except Exception as e:
        print(f"Error reading config file: {e}")
    return None

def get_indian_news(api_key):
    """
    Fetch top headlines from Indian news sources
    """
    # Try different sources to get better quality articles
    sources = [
        {'country': 'in'},  # India (broader search)
        {'sources': 'google-news-in'},  # Google News India
        {'q': 'India'},  # Search for India
    ]
    
    all_articles = []
    
    for i, source_params in enumerate(sources):
        # URL for top headlines
        url = f"https://newsapi.org/v2/top-headlines"
        
        # Parameters for the API request
        params = source_params.copy()
        params['apiKey'] = api_key
        params['pageSize'] = '20'  # Get more articles to filter through
        
        try:
            # Make the API request
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()
                
                # Check if the request was successful
                if data['status'] == 'ok' and data.get('articles'):
                    # Filter out generic "Google News" titles
                    filtered_articles = [
                        article for article in data['articles'] 
                        if article.get('title') and not article['title'].startswith('Google News')
                    ]
                    all_articles.extend(filtered_articles)
                    
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
    
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

def clean_html(text):
    """
    Remove HTML tags and decode HTML entities
    """
    if not text:
        return ""
    # Decode HTML entities
    text = html.unescape(text)
    # Remove common HTML tags (basic cleaning)
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()

def save_news_for_youtube(articles):
    """
    Save news data to a text file for YouTube video creation
    """
    with open('youtube_news_content.txt', 'w', encoding='utf-8') as f:
        f.write(f"TOP NEWS FROM INDIA - {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("=" * 50 + "\n\n")
        
        if not articles:
            f.write("No articles found.\n")
            return
            
        for i, article in enumerate(articles[:15], 1):  # Increase to 15 articles
            title = article.get('title', 'No title')
            source = article['source']['name'] if article.get('source') else 'Unknown source'
            published_at = article.get('publishedAt', '')[:19].replace('T', ' ') if article.get('publishedAt') else 'Unknown date'
            
            # Clean and display description
            description = clean_html(article.get('description', ''))
            if not description:
                description = "No description available."
            
            # URL
            url = article.get('url', 'No URL available')
            
            # Write to file
            f.write(f"{i}. {title}\n")
            f.write(f"   Source: {source}\n")
            f.write(f"   Published: {published_at}\n")
            f.write(f"   Description: {description}\n")
            f.write(f"   Link: {url}\n\n")
    
    print("News content saved to: youtube_news_content.txt")

def generate_html_dashboard(articles):
    """
    Generate an HTML dashboard with the news articles
    """
    if not articles:
        articles_html = "<p>No articles found.</p>"
    else:
        articles_html = ""
        for i, article in enumerate(articles[:15], 1):  # Increase to 15 articles
            # Clean and prepare article data
            title = article.get('title', 'No title')
            source = article['source']['name'] if article.get('source') else 'Unknown source'
            published_at = article.get('publishedAt', '')[:19].replace('T', ' ') if article.get('publishedAt') else 'Unknown date'
            
            # Clean and display description
            description = clean_html(article.get('description', ''))
            if not description:
                description = "No description available."
            elif len(description) > 300:
                description = description[:297] + "..."
            
            # Display URL if available and seems valid
            url = article.get('url', '#')
            if not url or not url.startswith('http'):
                url = '#'
            
            # Add article to HTML
            articles_html += f'''
            <div class="article">
                <h3>{i}. {title}</h3>
                <p class="meta">Source: {source} | Published: {published_at}</p>
                <p class="description">{description}</p>
                <div class="url-container">
                    <span class="url-label">Link:</span>
                    <a href="{url}" target="_blank" class="url-link">{url}</a>
                    <button class="copy-btn" onclick="copyToClipboard('{url.replace("'", "\\'")}', this)">Copy Link</button>
                </div>
                <button class="copy-content-btn" onclick="copyArticleContent({i}, '{title.replace("'", "\\'")}', '{source.replace("'", "\\'")}', '{published_at}', '{description.replace("'", "\\'")}')">Copy Article Content</button>
            </div>
            '''
    
    # Create complete HTML document
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Indian News Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .header {{
                background-color: #2c3e50;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            .articles {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
                gap: 20px;
            }}
            .article {{
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .article h3 {{
                margin-top: 0;
                color: #2c3e50;
            }}
            .meta {{
                color: #7f8c8d;
                font-size: 0.9em;
                margin: 10px 0;
            }}
            .description {{
                line-height: 1.6;
                margin: 15px 0;
            }}
            .url-container {{
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 3px;
                margin: 10px 0;
                display: flex;
                align-items: center;
                flex-wrap: wrap;
            }}
            .url-label {{
                font-weight: bold;
                margin-right: 10px;
            }}
            .url-link {{
                flex: 1;
                color: #3498db;
                text-decoration: none;
                word-break: break-all;
                margin-right: 10px;
            }}
            .url-link:hover {{
                text-decoration: underline;
            }}
            .copy-btn, .copy-content-btn {{
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 3px;
                cursor: pointer;
                font-size: 0.9em;
                white-space: nowrap;
            }}
            .copy-btn:hover, .copy-content-btn:hover {{
                background-color: #2980b9;
            }}
            .notification {{
                position: fixed;
                top: 20px;
                right: 20px;
                background-color: #27ae60;
                color: white;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                display: none;
                z-index: 1000;
            }}
            @media (max-width: 600px) {{
                .articles {{
                    grid-template-columns: 1fr;
                }}
                body {{
                    padding: 10px;
                }}
                .url-container {{
                    flex-direction: column;
                    align-items: flex-start;
                }}
                .url-link {{
                    margin: 10px 0;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🇮🇳 Indian News Dashboard</h1>
            <p>Top headlines from Indian news sources - {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        <div class="articles">
            {articles_html}
        </div>
        <div id="notification" class="notification">Copied to clipboard!</div>
        
        <script>
            function copyToClipboard(text, button) {{
                navigator.clipboard.writeText(text).then(() => {{
                    const originalText = button.textContent;
                    button.textContent = 'Copied!';
                    setTimeout(() => {{
                        button.textContent = originalText;
                    }}, 2000);
                }}).catch(err => {{
                    console.error('Failed to copy: ', err);
                    showNotification('Failed to copy to clipboard');
                }});
            }}
            
            function copyArticleContent(index, title, source, published, description) {{
                const content = `${{index}}. ${{title}}
Source: ${{source}}
Published: ${{published}}
Description: ${{description}}`;
                
                navigator.clipboard.writeText(content).then(() => {{
                    showNotification('Article content copied to clipboard!');
                }}).catch(err => {{
                    console.error('Failed to copy: ', err);
                    showNotification('Failed to copy to clipboard');
                }});
            }}
            
            function showNotification(message) {{
                const notification = document.getElementById('notification');
                notification.textContent = message;
                notification.style.display = 'block';
                setTimeout(() => {{
                    notification.style.display = 'none';
                }}, 3000);
            }}
        </script>
    </body>
    </html>
    '''
    
    # Write HTML to file
    with open('news_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML dashboard generated: news_dashboard.html")

def display_news(articles):
    """
    Display news articles in a formatted way (console output)
    """
    if not articles:
        print("No articles found.")
        return
    
    print(f"\n{'='*100}")
    print(f"TOP NEWS FROM INDIA - {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*100}")
    
    for i, article in enumerate(articles[:15], 1):  # Increase to 15 articles
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source']['name']}")
        print(f"   Published: {article['publishedAt'][:19].replace('T', ' ')}")
        
        # Clean and display description
        description = clean_html(article.get('description', ''))
        if description:
            # Limit description length for better readability
            if len(description) > 200:
                description = description[:197] + "..."
            print(f"   Description: {description}")
        
        # Display URL if available and seems valid
        url = article.get('url', '')
        if url and url.startswith('http'):
            print(f"   Link: {url}")
        print("-" * 100)

def main():
    # Get API key from environment variable, config file, or user input
    api_key = os.environ.get('NEWS_API_KEY')
    
    if not api_key:
        api_key = get_api_key_from_config()
    
    if not api_key:
        print("NewsAPI.org API key not found in environment variables or config file.")
        print("Please get a free API key from https://newsapi.org/")
        api_key = input("Enter your NewsAPI key: ").strip()
    
    if not api_key:
        print("API key is required to fetch news.")
        return
    
    print("Fetching today's top news from India...")
    articles = get_indian_news(api_key)
    
    # Display news in console
    display_news(articles)
    
    # Save news content for YouTube
    save_news_for_youtube(articles)
    
    # Generate HTML dashboard
    generate_html_dashboard(articles)
    print("Open 'news_dashboard.html' in your browser to view the web dashboard.")
    print("Check 'youtube_news_content.txt' for news content to use in your YouTube videos.")

if __name__ == "__main__":
    main()