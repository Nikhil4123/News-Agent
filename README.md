# Indian News Fetcher

A Python application to fetch and deliver Indian news updates automatically via email 3 times daily.

## Features

- **Dual API Support**: Fetches top headlines from Indian news sources using:
  - NewsAPI.org (100 requests/day free)
  - NewsData.io (200 requests/day free)
- **Automated Email Delivery**: Beautiful HTML emails with news updates
- **Scheduled Updates**: Automatically sends news 3 times daily (every 8 hours)
- **Smart Fallback**: Automatically switches between APIs if one fails
- **Multiple Viewing Options**: 
  - Email notifications (HTML + plain text)
  - Console output
  - HTML dashboard
  - Text file export
- **Flexible Configuration**: Config file or environment variables

## Requirements

- Python 3.7 or higher
- At least one API key (NewsAPI.org or NewsData.io)
- Email account with SMTP access (Gmail, Outlook, etc.)

## Installation

1. Clone or download this repository
   ```bash
   git clone https://github.com/yourusername/indian-news-fetcher.git
   cd indian-news-fetcher
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application:
   ```bash
   # Copy example config
   cp config/config.example.txt config/config.txt
   
   # Edit config/config.txt with your API keys and email settings
   # See config/config.example.txt for all options
   ```

## Quick Start

### 1. Get API Keys (Free)

**Option A: NewsAPI.org** (Recommended for comprehensive coverage)
- Register at [NewsAPI.org](https://newsapi.org/)
- Free tier: 100 requests/day

**Option B: NewsData.io** (Alternative/Backup)
- Register at [NewsData.io](https://newsdata.io/)
- Free tier: 200 requests/day

**Best Practice**: Configure both for automatic fallback!

### 2. Configure Email (Gmail Example)

For Gmail, you need to create an **App Password**:
1. Go to your Google Account settings
2. Enable 2-Step Verification
3. Go to Security → App Passwords
4. Generate a new app password for "Mail"
5. Use this app password (not your regular password)

### 3. Update Configuration

Edit `config/config.txt` with your credentials:

```ini
# API Configuration
NEWS_API_KEY=your_newsapi_key_here
NEWSDATA_API_KEY=your_newsdata_key_here
API_PREFERENCE=newsapi

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password_here
RECIPIENT_EMAILS=recipient1@example.com,recipient2@example.com

# Schedule (times in 24-hour format)
SCHEDULE_TIMES=06:00,14:00,22:00
```

**For Outlook/Hotmail**:
- SMTP_SERVER=smtp-mail.outlook.com
- SMTP_PORT=587

### 4. Alternative: Environment Variables

For cloud deployment, use environment variables instead:

```bash
# Windows PowerShell
$env:NEWS_API_KEY="your_key"
$env:SENDER_EMAIL="your_email@gmail.com"
$env:SENDER_PASSWORD="your_app_password"
$env:RECIPIENT_EMAILS="recipient@example.com"

# Linux/Mac
export NEWS_API_KEY="your_key"
export SENDER_EMAIL="your_email@gmail.com"
export SENDER_PASSWORD="your_app_password"
export RECIPIENT_EMAILS="recipient@example.com"
```

## Usage

### Option 1: Automated Scheduler (Recommended for Deployment)

Run the automated scheduler that sends news 3 times daily:

```bash
python run.py
# or
python scheduler_app.py
```

This will:
- Send news at scheduled times (default: 6 AM, 2 PM, 10 PM)
- Run continuously in the background
- Automatically retry with backup API if primary fails
- Log all activities to `logs/news_scheduler.log`

**Test immediately without waiting**:
```bash
python scheduler_app.py --test
```

### Option 2: Manual News Fetch (Legacy)

Fetch and display news in console:
```bash
python news_fetcher.py
```

### Option 3: Test Individual Components

**Test NewsData.io API**:
```bash
python newsdata_fetcher.py
```

**Test Email Sender**:
```bash
python email_sender.py
```

**Test Unified Service**:
```bash
python news_service.py
```

## Deployment

### Cloud Deployment (AWS, Azure, Google Cloud, etc.)

1. **Upload your code** to the cloud server

2. **Set environment variables** (recommended for security):
   ```bash
   export NEWS_API_KEY="your_key"
   export NEWSDATA_API_KEY="your_key"
   export SMTP_SERVER="smtp.gmail.com"
   export SMTP_PORT="587"
   export SENDER_EMAIL="your_email@gmail.com"
   export SENDER_PASSWORD="your_app_password"
   export RECIPIENT_EMAILS="recipient1@email.com,recipient2@email.com"
   export SCHEDULE_TIMES="06:00,14:00,22:00"
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run as background service**:
   ```bash
   nohup python scheduler_app.py > output.log 2>&1 &
   ```

### Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "scheduler_app.py"]
```

Run with:
```bash
docker build -t indian-news-fetcher .
docker run -d --env-file .env indian-news-fetcher
```

### Heroku Deployment

1. Create `Procfile`:
   ```
   worker: python scheduler_app.py
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set NEWS_API_KEY=your_key
   heroku config:set SENDER_EMAIL=your_email
   # ... set other variables
   git push heroku main
   ```

### PythonAnywhere / Other Platforms

Similar approach: Set environment variables and run `scheduler_app.py` as a long-running process.

## Project Structure

```
indian-news-fetcher/
├── src/                       # Source code
│   ├── __init__.py
│   ├── fetchers/              # News API fetchers
│   │   ├── __init__.py
│   │   ├── newsapi_fetcher.py
│   │   └── newsdata_fetcher.py
│   └── services/              # Core services
│       ├── __init__.py
│       ├── news_service.py
│       └── email_sender.py
├── config/                    # Configuration files
│   ├── config.example.txt     # Template (safe to commit)
│   └── config.txt            # Your config (gitignored)
├── scripts/                   # Utility scripts
│   ├── test_setup.py
│   ├── test_email_now.py
│   └── ...
├── docs/                      # Documentation
├── tests/                     # Test files
├── logs/                      # Log files (gitignored)
├── run.py                     # Main entry point
├── scheduler_app.py            # Scheduler application
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore rules
├── README.md                   # Main documentation
├── CONTRIBUTING.md            # Contributing guidelines
└── SETUP.md                   # Setup guide
```

## How It Works

1. **Scheduler** runs continuously and triggers news fetch at scheduled times
2. **News Service** tries primary API (based on API_PREFERENCE setting)
3. If primary fails, automatically switches to backup API
4. **Email Sender** formats articles into beautiful HTML email
5. Email is sent to all configured recipients
6. Process repeats 3 times daily

## Troubleshooting

### Email Issues

**Gmail Authentication Failed**:
- Use App Password, not regular password
- Enable 2-Step Verification first
- Check SMTP settings: smtp.gmail.com:587

**Outlook/Hotmail Issues**:
- Use smtp-mail.outlook.com:587
- Enable "Let apps use SMTP" in settings

### API Issues

**No articles fetched**:
- Check API key is valid and not expired
- Verify API quota (100/day for NewsAPI, 200/day for NewsData.io)
- Check internet connection
- Try switching API_PREFERENCE in config.txt

**Rate Limit Exceeded**:
- Use both APIs for higher limits
- Reduce SCHEDULE_TIMES to 2 times daily
- Consider paid API plans

### Scheduler Issues

**Scheduler not running**:
- Check Python version (3.7+)
- Verify all dependencies installed
- Check news_scheduler.log for errors

## API Limits & Best Practices

### NewsAPI.org (Free Tier)
- 100 requests/day
- 1,000 requests/month
- Good for: Broad news coverage

### NewsData.io (Free Tier)
- 200 requests/day
- Good for: Real-time Indian news

### Recommended Setup for 3x Daily Schedule
- Configure both APIs
- Set API_PREFERENCE to your primary choice
- System will auto-fallback if primary fails
- Total: ~6 requests/day (well within limits)

## Advanced Configuration

### Custom Schedule Times

Edit `SCHEDULE_TIMES` in config.txt for different intervals:

```ini
# Every 6 hours (4 times/day)
SCHEDULE_TIMES=00:00,06:00,12:00,18:00

# Business hours only (2 times/day)
SCHEDULE_TIMES=09:00,18:00

# Every 8 hours (3 times/day) - Default
SCHEDULE_TIMES=06:00,14:00,22:00
```

### Multiple Recipients

Add multiple email addresses (comma-separated):
```ini
RECIPIENT_EMAILS=user1@email.com,user2@email.com,team@company.com
```

## Logging

All activities are logged to `news_scheduler.log`:
- Scheduled runs
- API calls and responses
- Email send status
- Errors and warnings

Check logs for troubleshooting:
```bash
tail -f news_scheduler.log
```

## Contributing

Feel free to contribute improvements:
- Additional news sources
- Better email templates
- Enhanced error handling
- More deployment guides

## License

MIT License - Feel free to use and modify!