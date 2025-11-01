# Setup Guide - Indian News Fetcher

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/indian-news-fetcher.git
   cd indian-news-fetcher
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure**
   ```bash
   # Copy example config
   cp config/config.example.txt config/config.txt
   
   # Edit config/config.txt with your API keys and email settings
   # NEVER commit config.txt to git!
   ```

4. **Test**
   ```bash
   python scripts/test_setup.py
   ```

5. **Run**
   ```bash
   python run.py
   ```

## Configuration

Edit `config/config.txt` with:

- **API Keys**:
  - NewsAPI.org: https://newsapi.org/register
  - NewsData.io: https://newsdata.io/register

- **Email Settings**:
  - Gmail: Use App Password (not regular password)
  - SMTP server and port
  - Recipient email addresses

See `config/config.example.txt` for template.

## Project Structure

```
indian-news-fetcher/
├── src/                  # Source code
│   ├── fetchers/         # API fetchers
│   └── services/         # Core services
├── config/              # Configuration files
├── scripts/             # Utility scripts
├── docs/                # Documentation
├── tests/               # Test files
├── logs/                # Log files (gitignored)
├── run.py               # Main entry point
└── scheduler_app.py      # Scheduler application
```

## Environment Variables (Alternative)

Instead of `config/config.txt`, you can use environment variables:

```bash
export NEWS_API_KEY="your_key"
export NEWSDATA_API_KEY="your_key"
export SENDER_EMAIL="your_email@gmail.com"
export SENDER_PASSWORD="your_app_password"
export RECIPIENT_EMAILS="recipient@example.com"
```

## Deployment

See `docs/DEPLOYMENT_GUIDE.md` for deployment instructions.

