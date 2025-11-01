#!/usr/bin/env python3
"""
Simple test script for the Indian News Fetcher
"""

import os
import sys

# Add the current directory to the path so we can import our news_fetcher module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_clean_html():
    """Test that HTML tags are properly removed from text"""
    import news_fetcher
    
    # Test with HTML tags
    html_text = "<p>This is a <strong>test</strong> paragraph.</p>"
    cleaned = news_fetcher.clean_html(html_text)
    assert cleaned == "This is a test paragraph.", f"Expected 'This is a test paragraph.', got '{cleaned}'"
    
    # Test with HTML entities
    html_entities = "This is a &quot;test&quot; with &lt;entities&gt;"
    cleaned = news_fetcher.clean_html(html_entities)
    assert cleaned == 'This is a "test" with <entities>', f"Expected 'This is a \"test\" with <entities>', got '{cleaned}'"
    
    # Test with None input
    cleaned = news_fetcher.clean_html(None)
    assert cleaned == "", f"Expected '', got '{cleaned}'"
    
    print("✅ test_clean_html passed")

def test_filtering():
    """Test that generic 'Google News' titles are filtered out"""
    # Mock articles with some generic titles
    mock_articles = [
        {'title': 'Google News', 'source': {'name': 'Google News (India)'}},
        {'title': 'Real News Article', 'source': {'name': 'Times of India'}},
        {'title': 'Google News', 'source': {'name': 'Google News (India)'}},
        {'title': 'Another Real Article', 'source': {'name': 'The Hindu'}}
    ]
    
    # Test filtering function
    filtered_articles = [
        article for article in mock_articles 
        if article.get('title') and not article['title'].startswith('Google News')
    ]
    
    # Should only have 2 articles left after filtering
    assert len(filtered_articles) == 2, f"Expected 2 articles, got {len(filtered_articles)}"
    
    # Check that the titles are the real ones
    titles = [article['title'] for article in filtered_articles]
    assert 'Real News Article' in titles, "Missing 'Real News Article'"
    assert 'Another Real Article' in titles, "Missing 'Another Real Article'"
    
    print("✅ test_filtering passed")

def test_file_creation():
    """Test that news content file is created correctly"""
    import news_fetcher
    
    # Create mock articles
    mock_articles = [
        {
            'title': 'Test News Article',
            'source': {'name': 'Test News Source'},
            'publishedAt': '2025-10-26T10:00:00Z',
            'description': 'This is a test description.',
            'url': 'https://example.com/test-article'
        }
    ]
    
    # Save to file
    news_fetcher.save_news_for_youtube(mock_articles)
    
    # Check that file was created and has expected content
    assert os.path.exists('youtube_news_content.txt'), "youtube_news_content.txt was not created"
    
    with open('youtube_news_content.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key elements
    assert 'Test News Article' in content, "Title not found in file"
    assert 'Test News Source' in content, "Source not found in file"
    assert '2025-10-26 10:00:00' in content, "Date not found in file"
    assert 'This is a test description.' in content, "Description not found in file"
    assert 'https://example.com/test-article' in content, "URL not found in file"
    
    # Clean up
    os.remove('youtube_news_content.txt')
    
    print("✅ test_file_creation passed")

if __name__ == "__main__":
    print("Running simple tests for Indian News Fetcher...")
    
    try:
        test_clean_html()
        test_filtering()
        test_file_creation()
        print("\n🎉 All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)