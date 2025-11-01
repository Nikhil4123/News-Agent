#!/usr/bin/env python3
"""
Quick Email Test - Send news email immediately
"""

import sys
import io
from pathlib import Path

# Set stdout encoding to UTF-8 for Windows compatibility
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.services.news_service import NewsService, load_config
from src.services.email_sender import EmailSender

def main():
    print("=" * 70)
    print("Testing Email Sending - Sending News Email Now")
    print("=" * 70)
    
    try:
        # Load configuration
        print("\n1. Loading configuration...")
        config = load_config()
        
        # Check required settings
        required = ['SMTP_SERVER', 'SMTP_PORT', 'SENDER_EMAIL', 'SENDER_PASSWORD', 'RECIPIENT_EMAILS']
        missing = [key for key in required if not config.get(key)]
        
        if missing:
            print(f"[FAIL] Missing configuration: {', '.join(missing)}")
            return
        
        # Strip spaces from password (Gmail app passwords sometimes copied with spaces)
        password = config['SENDER_PASSWORD'].replace(' ', '')
        config['SENDER_PASSWORD'] = password
        print(f"[OK] Configuration loaded")
        print(f"   SMTP Server: {config['SMTP_SERVER']}:{config['SMTP_PORT']}")
        print(f"   Sender: {config['SENDER_EMAIL']}")
        print(f"   Recipients: {config['RECIPIENT_EMAILS']}")
        
        # Initialize news service
        print("\n2. Initializing news service...")
        news_service = NewsService(config)
        print("[OK] News service initialized")
        
        # Fetch news
        print("\n3. Fetching news...")
        articles, api_source = news_service.fetch_news(max_articles=10)
        
        if not articles:
            print("[FAIL] No articles fetched!")
            print("   This might be due to:")
            print("   - Invalid API keys")
            print("   - API rate limits")
            print("   - Network issues")
            return
        
        print(f"[OK] Fetched {len(articles)} articles from {api_source}")
        print(f"   Sample titles:")
        for i, article in enumerate(articles[:3], 1):
            print(f"   {i}. {article.get('title', 'No title')[:60]}...")
        
        # Initialize email sender
        print("\n4. Initializing email sender...")
        smtp_server = config['SMTP_SERVER']
        smtp_port = int(config['SMTP_PORT'])
        sender_email = config['SENDER_EMAIL']
        sender_password = config['SENDER_PASSWORD']
        recipient_emails = [email.strip() for email in config['RECIPIENT_EMAILS'].split(',') if email.strip()]
        
        email_sender = EmailSender(
            smtp_server, smtp_port, sender_email,
            sender_password, recipient_emails
        )
        print(f"[OK] Email sender initialized for {len(recipient_emails)} recipient(s)")
        
        # Send email
        print("\n5. Sending email...")
        print("   This may take 10-30 seconds...")
        success = email_sender.send_news_email(articles, api_source)
        
        if success:
            print("\n" + "=" * 70)
            print("[SUCCESS] Email sent successfully!")
            print("=" * 70)
            print(f"\n[INFO] Check your inbox: {', '.join(recipient_emails)}")
            print("   - Check your spam/junk folder if not in inbox")
            print("   - It may take 1-2 minutes to arrive")
        else:
            print("\n" + "=" * 70)
            print("[FAIL] Email was not sent.")
            print("=" * 70)
            print("\nTroubleshooting:")
            print("1. Check SENDER_PASSWORD in config.txt:")
            print("   - Gmail app passwords are 16 characters WITHOUT spaces")
            print("   - Make sure you're using App Password, not regular password")
            print("   - Enable 2-Step Verification first in Google Account")
            print("\n2. Verify SMTP settings:")
            print("   - Gmail: smtp.gmail.com, port 587")
            print("   - Make sure 'Less secure app access' is enabled OR use App Password")
            print("\n3. Check your internet connection")
            print("\n4. Try running: python email_sender.py")
            
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nTroubleshooting:")
        print("1. Make sure config.txt has all required fields")
        print("2. Check that API keys are valid")
        print("3. Verify email SMTP settings")
        print("4. Run: python test_setup.py to check configuration")

if __name__ == "__main__":
    main()

