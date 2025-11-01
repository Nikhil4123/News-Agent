# Running the Indian News Fetcher

## Files Created

1. **[news_fetcher.py](file://c:/Users/asus/Music/Temp/News%20Agent/news_fetcher.py)** - Main script to fetch Indian news and create YouTube content
2. **[better_news_fetcher.py](file://c:/Users/asus/Music/Temp/News%20Agent/better_news_fetcher.py)** - Improved version that tries multiple sources for better titles
3. **[requirements.txt](file://c:/Users/asus/Music/Temp/News%20Agent/requirements.txt)** - Python dependencies
4. **[config.txt](file://c:/Users/asus/Music/Temp/News%20Agent/config.txt)** - API key configuration
5. **[youtube_news_content.txt](file://c:/Users/asus/Music/Temp/News%20Agent/youtube_news_content.txt)** - Current news content for YouTube
6. **[news_dashboard.html](file://c:/Users/asus/Music/Temp/News%20Agent/news_dashboard.html)** - Web dashboard to view news
7. **Test scripts** - Various test files to verify functionality

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   - Get a free API key from [NewsAPI.org](https://newsapi.org/)
   - Add it to [config.txt](file://c:/Users/asus/Music/Temp/News%20Agent/config.txt):
     ```
     NEWS_API_KEY=your_actual_api_key_here
     ```

## Running the Scripts

### Main News Fetcher
```bash
python news_fetcher.py
```

This will:
- Fetch top Indian news
- Create [youtube_news_content.txt](file://c:/Users/asus/Music/Temp/News%20Agent/youtube_news_content.txt) with news for YouTube videos
- Generate [news_dashboard.html](file://c:/Users/asus/Music/Temp/News%20Agent/news_dashboard.html) for web viewing

### Better News Fetcher (Recommended)
```bash
python better_news_fetcher.py
```

This improved version:
- Tries multiple Indian news sources for better quality titles
- Filters out generic "Google News" articles
- Creates [better_youtube_news_content.txt](file://c:/Users/asus/Music/Temp/News%20Agent/better_youtube_news_content.txt)

## Output Files

1. **Text Files for YouTube**:
   - [youtube_news_content.txt](file://c:/Users/asus/Music/Temp/News%20Agent/youtube_news_content.txt) - Content from main fetcher
   - [better_youtube_news_content.txt](file://c:/Users/asus/Music/Temp/News%20Agent/better_youtube_news_content.txt) - Content from improved fetcher

2. **Web Dashboard**:
   - [news_dashboard.html](file://c:/Users/asus/Music/Temp/News%20Agent/news_dashboard.html) - Interactive news dashboard

## Viewing the Dashboard

1. Start a simple web server:
   ```bash
   python -m http.server 8000
   ```

2. Open your browser to:
   ```
   http://localhost:8000/news_dashboard.html
   ```

## Troubleshooting

1. **No articles found**: 
   - Check your API key in [config.txt](file://c:/Users/asus/Music/Temp/News%20Agent/config.txt)
   - Verify you have internet connectivity
   - Check if you've hit the NewsAPI rate limits

2. **Generic "Google News" titles**:
   - Use [better_news_fetcher.py](file://c:/Users/asus/Music/Temp/News%20Agent/better_news_fetcher.py) which filters these out
   - Try running the script at a different time of day when more specific articles may be available

3. **Empty output files**:
   - Run the debug scripts to see what's happening:
     ```bash
     python debug_news_fetcher.py
     python api_test.py
     ```

## Using for YouTube Videos

1. **For video scripts**: Copy titles and descriptions from the text files
2. **For video descriptions**: Use the complete formatted content
3. **For research**: Follow the links to read full articles

The content updates each time you run the script, ensuring fresh news for your videos.