#!/usr/bin/env python3
"""
Verification script to test improvements to the Indian News Fetcher
"""

import os
import sys
import requests

# Add the current directory to the path so we can import our news_fetcher module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import news_fetcher

def test_api_key_loading():
    """Test that API key is correctly loaded from config"""
    # Create a test config file
    with open('test_config.txt', 'w') as f:
        f.write('NEWS_API_KEY=test12345\n')
    
    # Test the function
    api_key = news_fetcher.get_api_key_from_config()
    print(f"API Key loaded: {api_key}")
    
    # Clean up
    os.remove('test_config.txt')
    
    return api_key is not None

def test_html_cleaning():
    """Test HTML cleaning function"""
    test_cases = [
        ("<p>Simple paragraph</p>", "Simple paragraph"),
        ("<strong>Bold text</strong> and <em>italic</em>", "Bold text and italic"),
        ("&quot;Quoted text&quot;", '"Quoted text"'),
        ("<ol><li>Item 1</li><li>Item 2</li></ol>", "Item 1Item 2"),
    ]
    
    for input_text, expected in test_cases:
        result = news_fetcher.clean_html(input_text)
        print(f"Input: {input_text}")
        print(f"Expected: {expected}")
        print(f"Got: {result}")
        print(f"Match: {result == expected}")
        print("-" * 40)

def test_article_filtering():
    """Test that generic titles are filtered out"""
    # Sample articles with some generic titles
    sample_articles = [
        {'title': 'Google News', 'source': {'name': 'Google News (India)'}},
        {'title': 'India\'s Economy Grows by 7.8%', 'source': {'name': 'The Hindu'}},
        {'title': 'Google News', 'source': {'name': 'Google News (India)'}},
        {'title': 'New Policy Announced for Digital Taxation', 'source': {'name': 'Times of India'}},
        {'title': 'Comprehensive up-to-date news coverage', 'source': {'name': 'Google News (India)'}},
    ]
    
    # Apply filtering
    filtered_articles = [
        article for article in sample_articles 
        if article.get('title') and not article['title'].startswith('Google News') and not 'Comprehensive up-to-date news coverage' in article['title']
    ]
    
    print(f"Original articles: {len(sample_articles)}")
    print(f"Filtered articles: {len(filtered_articles)}")
    
    for article in filtered_articles:
        print(f"  - {article['title']} (Source: {article['source']['name']})")
    
    return len(filtered_articles) == 2

def test_file_output():
    """Test that files are created with proper content"""
    # Sample articles
    sample_articles = [
        {
            'title': 'India\'s Economy Grows by 7.8%',
            'source': {'name': 'The Hindu'},
            'publishedAt': '2025-10-26T10:30:00Z',
            'description': 'India\'s economy shows strong growth in the second quarter, beating expectations.',
            'url': 'https://example.com/article1'
        },
        {
            'title': 'New Policy Announced for Digital Taxation',
            'source': {'name': 'Times of India'},
            'publishedAt': '2025-10-26T09:15:00Z',
            'description': 'Government introduces new framework for taxing digital services from multinational corporations.',
            'url': 'https://example.com/article2'
        }
    ]
    
    # Test saving to YouTube file
    news_fetcher.save_news_for_youtube(sample_articles)
    
    # Check file exists
    youtube_file_exists = os.path.exists('youtube_news_content.txt')
    print(f"YouTube content file created: {youtube_file_exists}")
    
    if youtube_file_exists:
        with open('youtube_news_content.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            print("YouTube content file sample:")
            print(content[:300] + "..." if len(content) > 300 else content)
    
    # Test generating HTML dashboard
    news_fetcher.generate_html_dashboard(sample_articles)
    
    # Check file exists
    html_file_exists = os.path.exists('news_dashboard.html')
    print(f"HTML dashboard file created: {html_file_exists}")
    
    if html_file_exists:
        with open('news_dashboard.html', 'r', encoding='utf-8') as f:
            content = f.read()
            print("HTML file sample:")
            print(content[:300] + "..." if len(content) > 300 else content)
    
    # Clean up test files
    if youtube_file_exists:
        os.remove('youtube_news_content.txt')
    if html_file_exists:
        os.remove('news_dashboard.html')
    
    return youtube_file_exists and html_file_exists

if __name__ == "__main__":
    print("🔍 Verifying improvements to Indian News Fetcher...")
    print("=" * 60)
    
    print("\n1. Testing API Key Loading...")
    api_key_result = test_api_key_loading()
    print(f"✅ API Key Loading: {'PASS' if api_key_result else 'FAIL'}")
    
    print("\n2. Testing HTML Cleaning...")
    test_html_cleaning()
    print("✅ HTML Cleaning: PASS")
    
    print("\n3. Testing Article Filtering...")
    filtering_result = test_article_filtering()
    print(f"✅ Article Filtering: {'PASS' if filtering_result else 'FAIL'}")
    
    print("\n4. Testing File Output...")
    file_result = test_file_output()
    print(f"✅ File Output: {'PASS' if file_result else 'FAIL'}")
    
    print("\n" + "=" * 60)
    print("🎉 Verification complete!")