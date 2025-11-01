# Running the Indian News Fetcher

## 🆕 NEW: Automated Email Scheduler

**The project now includes automated email delivery!** Get Indian news delivered to your inbox 3 times daily.

### Quick Start (Email Mode)
1. Configure `config.txt` with your API keys and email settings
2. Run: `python test_setup.py` to verify configuration
3. Run: `python scheduler_app.py --test` for immediate test
4. Run: `python scheduler_app.py` for continuous operation

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

---

## Files Overview

### **Core Application Files (NEW)**
1. **scheduler_app.py** - Main scheduler for automated email delivery
2. **news_service.py** - Unified news service with dual API support
3. **newsdata_fetcher.py** - NewsData.io API integration
4. **email_sender.py** - Email notification system
5. **test_setup.py** - Setup verification script

### **Legacy/Manual Files**
6. **news_fetcher.py** - Original manual news fetcher
7. **better_news_fetcher.py** - Enhanced manual fetcher
8. **simple_news_fetcher.py** - Simplified version

### **Configuration & Data**
9. **config.txt** - Main configuration file
10. **requirements.txt** - Python dependencies
11. **youtube_news_content.txt** - Generated news content
12. **news_dashboard.html** - Web dashboard

### **Documentation**
13. **README.md** - Complete documentation
14. **QUICKSTART.md** - 5-minute setup guide
15. **DEPLOYMENT_GUIDE.md** - Cloud deployment guide
16. **PROJECT_OVERVIEW.md** - Project structure

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

### Option 1: Automated Email Scheduler (NEW - Recommended)

**For continuous automated delivery via email:**

```bash
# 1. First, verify your setup
python test_setup.py

# 2. Test immediately (sends one email now)
python scheduler_app.py --test

# 3. Run continuously (sends at scheduled times)
python scheduler_app.py
```

**What it does:**
- Fetches news from NewsAPI.org or NewsData.io (with auto-fallback)
- Sends beautiful HTML emails to configured recipients
- Runs 3 times daily at scheduled times (default: 6 AM, 2 PM, 10 PM)
- Logs all activity to `news_scheduler.log`
- Perfect for deployment on cloud servers

**Configuration**: Edit `config.txt` with your:
- API keys (NewsAPI.org and/or NewsData.io)
- Email SMTP settings
- Recipient email addresses
- Schedule times

---

### Option 2: Manual News Fetcher (Original)

**For on-demand viewing in console/browser:**

```bash
python news_fetcher.py
```

This will:
- Fetch top Indian news
- Create [youtube_news_content.txt](file://c:/Users/asus/Music/Temp/News%20Agent/youtube_news_content.txt) with news for YouTube videos
- Generate [news_dashboard.html](file://c:/Users/asus/Music/Temp/News%20Agent/news_dashboard.html) for web viewing

---

### Option 3: Better News Fetcher (Enhanced Manual)

```bash
python better_news_fetcher.py
```

This improved version:
- Tries multiple Indian news sources for better quality titles
- Filters out generic "Google News" articles
- Creates [better_youtube_news_content.txt](file://c:/Users/asus/Music/Temp/News%20Agent/better_youtube_news_content.txt)

---

### Option 4: Test Individual Components

```bash
# Test NewsData.io API
python newsdata_fetcher.py

# Test email sending
python email_sender.py

# Test unified news service
python news_service.py

# Test complete setup
python test_setup.py
```

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