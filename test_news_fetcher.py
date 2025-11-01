#!/usr/bin/env python3
"""
Test script for the Indian News Fetcher
"""

import unittest
import os
import sys
from unittest.mock import patch, Mock
import json
import builtins

# Add the current directory to the path so we can import our news_fetcher module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import news_fetcher

class TestNewsFetcher(unittest.TestCase):
    
    def test_get_api_key_from_config(self):
        """Test that API key is correctly read from config file"""
        # Create a temporary config file for testing
        test_config_content = "NEWS_API_KEY=test_api_key_12345\n"
        with open('test_config.txt', 'w') as f:
            f.write(test_config_content)
        
        # Temporarily replace the config file name in the function
        original_open = builtins.open
        def mock_open(file, mode='r'):
            if file == 'config.txt':
                file = 'test_config.txt'
            return original_open(file, mode)
        
        with patch('builtins.open', side_effect=mock_open):
            api_key = news_fetcher.get_api_key_from_config()
            self.assertEqual(api_key, 'test_api_key_12345')
        
        # Clean up
        os.remove('test_config.txt')
    
    def test_clean_html(self):
        """Test that HTML tags are properly removed from text"""
        # Test with HTML tags
        html_text = "<p>This is a <strong>test</strong> paragraph.</p>"
        cleaned = news_fetcher.clean_html(html_text)
        self.assertEqual(cleaned, "This is a test paragraph.")
        
        # Test with HTML entities
        html_entities = "This is a &quot;test&quot; with &lt;entities&gt;"
        cleaned = news_fetcher.clean_html(html_entities)
        self.assertEqual(cleaned, 'This is a "test" with <entities>')
        
        # Test with None input
        cleaned = news_fetcher.clean_html(None)
        self.assertEqual(cleaned, "")
    
    def test_get_indian_news_filtering(self):
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
        self.assertEqual(len(filtered_articles), 2)
        
        # Check that the titles are the real ones
        titles = [article['title'] for article in filtered_articles]
        self.assertIn('Real News Article', titles)
        self.assertIn('Another Real Article', titles)
    
    def test_save_news_for_youtube(self):
        """Test that news content is saved correctly to file"""
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
        self.assertTrue(os.path.exists('youtube_news_content.txt'))
        
        with open('youtube_news_content.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key elements
        self.assertIn('Test News Article', content)
        self.assertIn('Test News Source', content)
        self.assertIn('2025-10-26 10:00:00', content)
        self.assertIn('This is a test description.', content)
        self.assertIn('https://example.com/test-article', content)
        
        # Clean up
        os.remove('youtube_news_content.txt')
    
    def test_display_news_output(self):
        """Test that news display function produces expected output structure"""
        # Capture print output
        import io
        from contextlib import redirect_stdout
        
        mock_articles = [
            {
                'title': 'Test Article',
                'source': {'name': 'Test Source'},
                'publishedAt': '2025-10-26T10:00:00Z',
                'description': 'Test description.',
                'url': 'https://example.com'
            }
        ]
        
        # Capture output
        f = io.StringIO()
        with redirect_stdout(f):
            news_fetcher.display_news(mock_articles)
        output = f.getvalue()
        
        # Check for key elements in output
        self.assertIn('Test Article', output)
        self.assertIn('Test Source', output)
        self.assertIn('2025-10-26 10:00:00', output)
        self.assertIn('Test description.', output)
        self.assertIn('https://example.com', output)

def run_tests():
    """Run all tests"""
    print("Running tests for Indian News Fetcher...")
    
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNewsFetcher)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success/failure
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)