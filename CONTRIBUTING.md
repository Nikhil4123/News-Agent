# Contributing to Indian News Fetcher

Thank you for your interest in contributing!

## Project Structure

```
News Agent/
├── src/
│   ├── fetchers/          # News API fetchers
│   │   ├── newsapi_fetcher.py
│   │   └── newsdata_fetcher.py
│   └── services/          # Core services
│       ├── news_service.py
│       └── email_sender.py
├── config/
│   └── config.example.txt  # Template (copy to config.txt)
├── scripts/               # Utility scripts
├── docs/                  # Documentation
├── tests/                 # Test files
├── logs/                  # Log files (gitignored)
├── run.py                 # Main entry point
├── scheduler_app.py       # Scheduler application
├── requirements.txt       # Dependencies
└── README.md             # Main documentation
```

## Setup for Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/indian-news-fetcher.git
   cd indian-news-fetcher
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure**
   ```bash
   cp config/config.example.txt config/config.txt
   # Edit config/config.txt with your API keys
   ```

## Code Style

- Use Python 3.7+
- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to all functions/classes
- Keep functions focused and small

## Making Changes

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Update documentation if needed
5. Submit a pull request

## Testing

Run tests before submitting:
```bash
python -m pytest tests/
```

## Security

- **NEVER commit config/config.txt** (it's in .gitignore)
- **NEVER commit API keys or passwords**
- Use `config/config.example.txt` as template only

## Questions?

Open an issue or start a discussion!

