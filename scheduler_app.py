#!/usr/bin/env python3
"""
News Scheduler Application
Automatically sends Indian news updates 3 times daily via email
"""

import time
import signal
import sys
from datetime import datetime, time as datetime_time
from typing import List
import schedule
import logging
from pathlib import Path

from src.services.news_service import NewsService, load_config
from src.services.email_sender import EmailSender


# Ensure logs directory exists
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

# Setup logging with UTF-8 encoding for Windows compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'news_scheduler.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Set stdout encoding to UTF-8 for Windows
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


class NewsScheduler:
    """Automated news scheduler with email notifications"""
    
    def __init__(self, config: dict):
        """
        Initialize news scheduler
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.news_service = None
        self.email_sender = None
        self.running = True
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Initialize services
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize news and email services"""
        try:
            # Initialize news service
            self.news_service = NewsService(self.config)
            logger.info("News service initialized")
            
            # Initialize email sender
            smtp_server = self.config.get('SMTP_SERVER')
            smtp_port = int(self.config.get('SMTP_PORT', 587))
            sender_email = self.config.get('SENDER_EMAIL')
            sender_password = self.config.get('SENDER_PASSWORD', '').replace(' ', '')  # Strip spaces (Gmail app passwords)
            recipient_emails_str = self.config.get('RECIPIENT_EMAILS', '')
            
            if not all([smtp_server, sender_email, sender_password, recipient_emails_str]):
                raise ValueError("Email configuration incomplete")
            
            recipient_emails = [email.strip() for email in recipient_emails_str.split(',') if email.strip()]
            
            self.email_sender = EmailSender(
                smtp_server, smtp_port, sender_email, 
                sender_password, recipient_emails
            )
            logger.info(f"Email sender initialized for {len(recipient_emails)} recipient(s)")
            
        except Exception as e:
            logger.error(f"Failed to initialize services: {e}")
            raise
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info("Shutdown signal received, stopping scheduler...")
        self.running = False
        sys.exit(0)
    
    def fetch_and_send_news(self):
        """Fetch news and send via email"""
        try:
            logger.info("=" * 70)
            logger.info("Starting scheduled news fetch...")
            
            # Fetch hottest/most interesting news articles
            # NewsData.io will fetch from multiple categories and filter for viral content
            articles, api_source = self.news_service.fetch_news(max_articles=25)
            
            if not articles:
                error_msg = "No articles fetched from any API"
                logger.error(error_msg)
                self.email_sender.send_error_notification(error_msg)
                return
            
            logger.info(f"Fetched {len(articles)} articles from {api_source}")
            
            # Send email
            success = self.email_sender.send_news_email(articles, api_source)
            
            if success:
                logger.info("✅ News email sent successfully")
            else:
                logger.error("❌ Failed to send news email")
            
            logger.info("=" * 70)
            
        except Exception as e:
            error_msg = f"Error in fetch_and_send_news: {e}"
            logger.error(error_msg)
            try:
                self.email_sender.send_error_notification(error_msg)
            except Exception as notify_error:
                logger.error(f"Failed to send error notification: {notify_error}")
    
    def setup_schedule(self, schedule_times: List[str]):
        """
        Setup scheduled times for news updates
        
        Args:
            schedule_times: List of times in HH:MM format (e.g., ["06:00", "14:00", "22:00"])
        """
        schedule.clear()
        
        for time_str in schedule_times:
            try:
                schedule.every().day.at(time_str).do(self.fetch_and_send_news)
                logger.info(f"Scheduled news update at {time_str}")
            except Exception as e:
                logger.error(f"Failed to schedule time {time_str}: {e}")
        
        if not schedule.get_jobs():
            raise ValueError("No valid schedule times configured")
    
    def run(self):
        """Run the scheduler"""
        logger.info("=" * 70)
        logger.info("🚀 Indian News Scheduler Started")
        logger.info("=" * 70)
        
        # Get schedule times from config
        schedule_times_str = self.config.get('SCHEDULE_TIMES', '06:00,14:00,22:00')
        schedule_times = [t.strip() for t in schedule_times_str.split(',') if t.strip()]
        
        logger.info(f"Schedule times: {', '.join(schedule_times)}")
        
        # Setup schedule
        self.setup_schedule(schedule_times)
        
        # Display next run times
        jobs = schedule.get_jobs()
        logger.info(f"Total scheduled jobs: {len(jobs)}")
        for job in jobs:
            logger.info(f"  Next run: {job.next_run}")
        
        logger.info("=" * 70)
        
        # Optional: Send immediate test notification
        if '--test' in sys.argv or '--immediate' in sys.argv:
            logger.info("Running immediate test...")
            self.fetch_and_send_news()
        
        # Main scheduler loop
        logger.info("Scheduler is running. Press Ctrl+C to stop.")
        
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)
        
        logger.info("Scheduler stopped")


def validate_config(config: dict) -> bool:
    """
    Validate configuration
    
    Args:
        config: Configuration dictionary
    
    Returns:
        True if valid, False otherwise
    """
    required_keys = [
        'SMTP_SERVER', 'SMTP_PORT', 'SENDER_EMAIL', 
        'SENDER_PASSWORD', 'RECIPIENT_EMAILS'
    ]
    
    # Check if at least one API key is configured
    has_news_api = config.get('NEWS_API_KEY') and config.get('NEWS_API_KEY') != 'your_api_key_here'
    has_newsdata_api = config.get('NEWSDATA_API_KEY') and config.get('NEWSDATA_API_KEY') != 'your_newsdata_io_api_key_here'
    
    if not has_news_api and not has_newsdata_api:
        logger.error("No API key configured! Please set NEWS_API_KEY or NEWSDATA_API_KEY")
        return False
    
    # Check email configuration
    for key in required_keys:
        if not config.get(key):
            logger.error(f"Missing required configuration: {key}")
            return False
    
    return True


def main():
    """Main entry point"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║         Indian News Scheduler - Email Edition                ║
║         Sends news updates 3 times daily                     ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Load configuration
        logger.info("Loading configuration...")
        config = load_config()
        
        # Validate configuration
        if not validate_config(config):
            logger.error("Configuration validation failed!")
            logger.error("Please check config.txt or environment variables")
            sys.exit(1)
        
        logger.info("✅ Configuration loaded and validated")
        
        # Create and run scheduler
        scheduler = NewsScheduler(config)
        scheduler.run()
        
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

