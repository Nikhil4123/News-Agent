#!/usr/bin/env python3
"""
Setup Verification Script
Tests all components to ensure proper configuration
"""

import sys
import os
from datetime import datetime
import io

# Set stdout encoding to UTF-8 for Windows compatibility
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_test(test_name, status, message=""):
    """Print test result"""
    status_symbol = "[OK]" if status else "[FAIL]"
    print(f"{status_symbol} {test_name}", end="")
    if message:
        print(f": {message}")
    else:
        print()

def test_python_version():
    """Test Python version"""
    print_header("Testing Python Version")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 7:
        print_test("Python Version", True, f"v{version_str} (OK)")
        return True
    else:
        print_test("Python Version", False, f"v{version_str} (Need 3.7+)")
        return False

def test_dependencies():
    """Test required packages"""
    print_header("Testing Dependencies")
    
    packages = {
        'requests': 'requests',
        'schedule': 'schedule'
    }
    
    all_ok = True
    for package_name, import_name in packages.items():
        try:
            __import__(import_name)
            print_test(f"Package: {package_name}", True)
        except ImportError:
            print_test(f"Package: {package_name}", False, "Not installed")
            all_ok = False
    
    return all_ok

def load_config():
    """Load configuration from file or environment"""
    import pathlib
    config = {}
    
    # Try multiple config file locations
    project_root = pathlib.Path(__file__).parent.parent
    config_paths = [
        project_root / 'config' / 'config.txt',
        project_root / 'config.txt',
        pathlib.Path('config') / 'config.txt',
        pathlib.Path('config.txt'),
    ]
    
    config_path = None
    for path in config_paths:
        if path.exists():
            config_path = path
            break
    
    # Try loading from config file
    if config_path:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip().strip('"\'')
        except FileNotFoundError:
            pass
    
    # Override with environment variables
    env_keys = [
        'NEWS_API_KEY', 'NEWSDATA_API_KEY', 'API_PREFERENCE',
        'SMTP_SERVER', 'SMTP_PORT', 'SENDER_EMAIL', 
        'SENDER_PASSWORD', 'RECIPIENT_EMAILS', 'SCHEDULE_TIMES'
    ]
    
    for key in env_keys:
        env_value = os.environ.get(key)
        if env_value:
            config[key] = env_value
    
    return config

def test_config():
    """Test configuration"""
    print_header("Testing Configuration")
    
    config = load_config()
    all_ok = True
    
    # Test API keys
    has_newsapi = config.get('NEWS_API_KEY') and config['NEWS_API_KEY'] not in ['', 'your_newsapi_key_here', 'your_api_key_here']
    has_newsdata = config.get('NEWSDATA_API_KEY') and config['NEWSDATA_API_KEY'] not in ['', 'your_newsdata_io_api_key_here']
    
    if has_newsapi:
        print_test("NewsAPI.org Key", True, f"Found ({len(config['NEWS_API_KEY'])} chars)")
    else:
        print_test("NewsAPI.org Key", False, "Not configured")
    
    if has_newsdata:
        print_test("NewsData.io Key", True, f"Found ({len(config['NEWSDATA_API_KEY'])} chars)")
    else:
        print_test("NewsData.io Key", False, "Not configured")
    
    if not has_newsapi and not has_newsdata:
        print("  [WARNING] You need at least ONE API key configured!")
        all_ok = False
    
    # Test email configuration
    email_fields = {
        'SMTP_SERVER': 'SMTP Server',
        'SMTP_PORT': 'SMTP Port',
        'SENDER_EMAIL': 'Sender Email',
        'SENDER_PASSWORD': 'Email Password',
        'RECIPIENT_EMAILS': 'Recipient Emails'
    }
    
    for key, name in email_fields.items():
        value = config.get(key)
        if value and value not in ['your_email@gmail.com', 'your_app_password_here', 'recipient@example.com']:
            if key == 'SENDER_PASSWORD':
                print_test(name, True, f"Set ({len(value)} chars)")
            else:
                print_test(name, True, value)
        else:
            print_test(name, False, "Not configured")
            all_ok = False
    
    return all_ok, config

def test_newsapi(api_key):
    """Test NewsAPI.org connection"""
    print_header("Testing NewsAPI.org")
    
    if not api_key:
        print_test("API Connection", False, "No API key")
        return False
    
    try:
        import requests
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            'country': 'in',
            'apiKey': api_key,
            'pageSize': '1'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                total_results = data.get('totalResults', 0)
                print_test("API Connection", True, f"{total_results} articles available")
                return True
            else:
                print_test("API Connection", False, data.get('message', 'Unknown error'))
                return False
        elif response.status_code == 401:
            print_test("API Connection", False, "Invalid API key")
            return False
        elif response.status_code == 429:
            print_test("API Connection", False, "Rate limit exceeded")
            return False
        else:
            print_test("API Connection", False, f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_test("API Connection", False, str(e))
        return False

def test_newsdata(api_key):
    """Test NewsData.io connection"""
    print_header("Testing NewsData.io")
    
    if not api_key:
        print_test("API Connection", False, "No API key")
        return False
    
    try:
        import requests
        url = "https://newsdata.io/api/1/news"
        params = {
            'apikey': api_key,
            'country': 'in',
            'language': 'en',
            'size': '1'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                total_results = data.get('totalResults', len(data.get('results', [])))
                print_test("API Connection", True, f"{total_results} articles available")
                return True
            else:
                print_test("API Connection", False, data.get('message', 'Unknown error'))
                return False
        elif response.status_code == 401:
            print_test("API Connection", False, "Invalid API key")
            return False
        elif response.status_code == 429:
            print_test("API Connection", False, "Rate limit exceeded")
            return False
        else:
            print_test("API Connection", False, f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_test("API Connection", False, str(e))
        return False

def test_email_connection(config):
    """Test email SMTP connection"""
    print_header("Testing Email Connection")
    
    smtp_server = config.get('SMTP_SERVER')
    smtp_port = int(config.get('SMTP_PORT', 587))
    sender_email = config.get('SENDER_EMAIL')
    sender_password = config.get('SENDER_PASSWORD')
    
    if not all([smtp_server, sender_email, sender_password]):
        print_test("Email Configuration", False, "Incomplete configuration")
        return False
    
    try:
        import smtplib
        
        print(f"  Connecting to {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()
            print("  Attempting login...")
            server.login(sender_email, sender_password)
        
        print_test("SMTP Connection", True, "Successfully authenticated")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print_test("SMTP Connection", False, "Authentication failed - check email/password")
        print("  💡 For Gmail: Use App Password, not regular password!")
        return False
    except Exception as e:
        print_test("SMTP Connection", False, str(e))
        return False

def print_summary(results):
    """Print test summary"""
    print_header("Test Summary")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed
    
    print(f"\n  Total Tests: {total}")
    print(f"  [OK] Passed: {passed}")
    print(f"  [FAIL] Failed: {failed}")
    
    if failed == 0:
        print("\n  [SUCCESS] All tests passed! You're ready to run the scheduler!")
        print("\n  Next steps:")
        print("    1. Run test email: python scheduler_app.py --test")
        print("    2. Start scheduler: python scheduler_app.py")
    else:
        print("\n  [WARNING] Some tests failed. Please fix the issues above.")
        print("\n  Common fixes:")
        print("    • API keys: Check config.txt or environment variables")
        print("    • Email: Use App Password for Gmail (not regular password)")
        print("    • Dependencies: Run 'pip install -r requirements.txt'")
    
    print("\n" + "=" * 70 + "\n")

def main():
    """Main test function"""
    print("\n" + "=" * 70)
    print("  Indian News Fetcher - Setup Test")
    print("=" * 70)
    
    results = {}
    
    # Test 1: Python version
    results['python'] = test_python_version()
    
    # Test 2: Dependencies
    results['dependencies'] = test_dependencies()
    
    if not results['dependencies']:
        print("\n[WARNING] Install dependencies first: pip install -r requirements.txt")
        print_summary(results)
        return
    
    # Test 3: Configuration
    config_ok, config = test_config()
    results['config'] = config_ok
    
    if not config_ok:
        print("\n[WARNING] Please configure config.txt or environment variables")
        print_summary(results)
        return
    
    # Test 4: NewsAPI.org (if configured)
    newsapi_key = config.get('NEWS_API_KEY')
    if newsapi_key and newsapi_key not in ['', 'your_newsapi_key_here', 'your_api_key_here']:
        results['newsapi'] = test_newsapi(newsapi_key)
    
    # Test 5: NewsData.io (if configured)
    newsdata_key = config.get('NEWSDATA_API_KEY')
    if newsdata_key and newsdata_key not in ['', 'your_newsdata_io_api_key_here']:
        results['newsdata'] = test_newsdata(newsdata_key)
    
    # Test 6: Email connection
    results['email'] = test_email_connection(config)
    
    # Print summary
    print_summary(results)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

