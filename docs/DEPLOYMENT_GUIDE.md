# Indian News Fetcher - Deployment Guide

This guide provides detailed instructions for deploying the Indian News Fetcher with automated email delivery.

## Prerequisites

Before deployment, ensure you have:

1. ✅ Python 3.7 or higher installed
2. ✅ At least one API key (NewsAPI.org or NewsData.io)
3. ✅ Email account with SMTP access
4. ✅ Server or cloud platform (for 24/7 operation)

## Step-by-Step Setup

### Step 1: Get Your API Keys

#### NewsAPI.org (Recommended Primary)
1. Visit https://newsapi.org/
2. Click "Get API Key"
3. Sign up with your email
4. Verify your email
5. Copy your API key
6. **Free Tier**: 100 requests/day, 1000/month

#### NewsData.io (Recommended Backup)
1. Visit https://newsdata.io/
2. Click "Get API Key" or "Sign Up"
3. Complete registration
4. Copy your API key from dashboard
5. **Free Tier**: 200 requests/day

**Pro Tip**: Configure both APIs for maximum reliability!

### Step 2: Configure Email Access

#### For Gmail Users

**Important**: Gmail requires "App Passwords" for security.

1. Go to https://myaccount.google.com/
2. Click **Security** in the left sidebar
3. Enable **2-Step Verification** (if not already enabled)
4. After enabling 2-Step, scroll to "App passwords"
5. Select:
   - App: **Mail**
   - Device: **Other (Custom name)**
   - Enter: "Indian News Fetcher"
6. Click **Generate**
7. Copy the 16-character password (spaces can be ignored)
8. **Use this password**, not your Gmail password!

#### For Outlook/Hotmail Users

1. Go to https://account.microsoft.com/security
2. Enable **Two-step verification** if not enabled
3. Go to **App passwords**
4. Generate a new app password
5. Copy and save it
6. SMTP settings:
   - Server: `smtp-mail.outlook.com`
   - Port: `587`

#### For Other Email Providers

Check your provider's documentation for:
- SMTP server address
- SMTP port (usually 587 for TLS)
- Whether app passwords are required

### Step 3: Configure the Application

#### Option A: Using config.txt (Simple)

1. Open `config.txt` in a text editor
2. Fill in your details:

```ini
# API Configuration
NEWS_API_KEY=your_actual_newsapi_key_here
NEWSDATA_API_KEY=your_actual_newsdata_key_here
API_PREFERENCE=newsapi

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=youremail@gmail.com
SENDER_PASSWORD=your_16_char_app_password
RECIPIENT_EMAILS=recipient1@example.com,recipient2@example.com

# Schedule Configuration
SCHEDULE_TIMES=06:00,14:00,22:00
```

3. Save the file

#### Option B: Using Environment Variables (Cloud Deployment)

Set these environment variables on your server:

```bash
export NEWS_API_KEY="your_newsapi_key"
export NEWSDATA_API_KEY="your_newsdata_key"
export API_PREFERENCE="newsapi"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SENDER_EMAIL="youremail@gmail.com"
export SENDER_PASSWORD="your_app_password"
export RECIPIENT_EMAILS="recipient1@example.com,recipient2@example.com"
export SCHEDULE_TIMES="06:00,14:00,22:00"
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter issues, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Step 5: Test Your Setup

Before deploying, test each component:

#### Test 1: NewsData.io Connection
```bash
python newsdata_fetcher.py
```
Expected: Should fetch and display sample news

#### Test 2: Email Sending
```bash
python email_sender.py
```
Expected: Should send a test email

#### Test 3: Unified Service
```bash
python news_service.py
```
Expected: Should fetch news using configured API

#### Test 4: Full Scheduler (Immediate)
```bash
python scheduler_app.py --test
```
Expected: Should fetch news and send email immediately

### Step 6: Deploy

Choose your deployment platform:

---

## Deployment Options

### Option 1: Linux Server (VPS, AWS EC2, DigitalOcean, etc.)

#### Upload Your Code
```bash
# On your local machine
scp -r "News Agent" user@yourserver.com:~/indian-news-fetcher

# Or use git
git clone your-repo-url
cd indian-news-fetcher
```

#### Set Up Environment
```bash
# Install Python if needed
sudo apt update
sudo apt install python3 python3-pip -y

# Install dependencies
cd ~/indian-news-fetcher
pip3 install -r requirements.txt
```

#### Configure Environment Variables
```bash
# Edit your shell profile
nano ~/.bashrc

# Add these lines at the end
export NEWS_API_KEY="your_key"
export NEWSDATA_API_KEY="your_key"
export SENDER_EMAIL="your_email@gmail.com"
export SENDER_PASSWORD="your_app_password"
export RECIPIENT_EMAILS="recipient@example.com"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"

# Save and reload
source ~/.bashrc
```

#### Run as Background Service (Method 1: nohup)
```bash
nohup python3 scheduler_app.py > output.log 2>&1 &
```

Check if running:
```bash
ps aux | grep scheduler_app.py
```

#### Run as Systemd Service (Method 2: Recommended)

Create service file:
```bash
sudo nano /etc/systemd/system/indian-news.service
```

Add this content:
```ini
[Unit]
Description=Indian News Fetcher Service
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/home/yourusername/indian-news-fetcher
Environment="NEWS_API_KEY=your_key"
Environment="SENDER_EMAIL=your_email@gmail.com"
Environment="SENDER_PASSWORD=your_app_password"
Environment="RECIPIENT_EMAILS=recipient@example.com"
ExecStart=/usr/bin/python3 /home/yourusername/indian-news-fetcher/scheduler_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable indian-news.service
sudo systemctl start indian-news.service

# Check status
sudo systemctl status indian-news.service

# View logs
sudo journalctl -u indian-news.service -f
```

---

### Option 2: Windows Server

#### Run as Background Process
```powershell
# PowerShell
Start-Process python -ArgumentList "scheduler_app.py" -WindowStyle Hidden
```

#### Run as Windows Service (using NSSM)

1. Download NSSM from https://nssm.cc/download
2. Open Command Prompt as Administrator:
```cmd
nssm install IndianNewsFetcher
```
3. In the GUI:
   - Path: `C:\Python39\python.exe`
   - Startup directory: `C:\path\to\News Agent`
   - Arguments: `scheduler_app.py`
4. Go to Environment tab, add variables
5. Click "Install service"

Start the service:
```cmd
nssm start IndianNewsFetcher
```

---

### Option 3: Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Run the scheduler
CMD ["python", "scheduler_app.py"]
```

#### Create .dockerignore
```
__pycache__
*.pyc
*.pyo
*.log
.git
.env
news_scheduler.log
youtube_news_content.txt
news_dashboard.html
```

#### Build and Run
```bash
# Build image
docker build -t indian-news-fetcher .

# Run with environment variables
docker run -d \
  --name news-fetcher \
  --restart unless-stopped \
  -e NEWS_API_KEY="your_key" \
  -e NEWSDATA_API_KEY="your_key" \
  -e SENDER_EMAIL="your_email@gmail.com" \
  -e SENDER_PASSWORD="your_app_password" \
  -e RECIPIENT_EMAILS="recipient@example.com" \
  -e SMTP_SERVER="smtp.gmail.com" \
  -e SMTP_PORT="587" \
  indian-news-fetcher

# View logs
docker logs -f news-fetcher

# Stop
docker stop news-fetcher

# Remove
docker rm news-fetcher
```

---

### Option 4: Heroku

#### Prepare Files

1. Create `Procfile`:
```
worker: python scheduler_app.py
```

2. Create `runtime.txt`:
```
python-3.9.16
```

#### Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-indian-news-app

# Set environment variables
heroku config:set NEWS_API_KEY=your_key
heroku config:set NEWSDATA_API_KEY=your_key
heroku config:set SENDER_EMAIL=your_email@gmail.com
heroku config:set SENDER_PASSWORD=your_app_password
heroku config:set RECIPIENT_EMAILS=recipient@example.com
heroku config:set SMTP_SERVER=smtp.gmail.com
heroku config:set SMTP_PORT=587
heroku config:set SCHEDULE_TIMES=06:00,14:00,22:00

# Deploy
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a your-indian-news-app
git push heroku main

# Scale worker
heroku ps:scale worker=1

# View logs
heroku logs --tail
```

---

### Option 5: Python Anywhere

1. Upload files via Files tab
2. Go to Tasks tab
3. Create scheduled tasks at your desired times
4. For each schedule time, add:
   ```bash
   cd ~/indian-news-fetcher && python3 scheduler_app.py --test
   ```
5. Set up tasks for 06:00, 14:00, and 22:00 UTC

---

### Option 6: AWS Lambda (Serverless)

For a serverless approach using AWS Lambda + EventBridge:

1. Package your code with dependencies
2. Create Lambda function
3. Set environment variables
4. Create EventBridge rules for scheduled execution
5. Use SES for email sending instead of SMTP

(Detailed Lambda setup requires AWS knowledge)

---

## Post-Deployment

### Verify It's Working

1. **Check logs**:
   ```bash
   tail -f news_scheduler.log
   ```

2. **Check email**: You should receive a test email if you used `--test`

3. **Wait for scheduled time**: First email will arrive at next scheduled time

### Monitor the Application

- Check `news_scheduler.log` regularly
- Set up email alerts for errors
- Monitor API usage in your API dashboards

### Troubleshooting

#### Application Not Starting
```bash
# Check if dependencies installed
pip list | grep schedule

# Check Python version
python --version  # Should be 3.7+

# Run with verbose output
python scheduler_app.py --test
```

#### Emails Not Sending
- Verify SMTP settings
- Check app password is correct
- Check sender email can send via SMTP
- Check firewall allows outbound port 587

#### No News Fetched
- Verify API keys are valid
- Check API quotas
- Try switching API_PREFERENCE
- Check internet connectivity

## Maintenance

### Update API Keys
```bash
# Edit config.txt or update environment variables
nano config.txt

# Restart service
sudo systemctl restart indian-news.service
```

### Change Schedule Times
```bash
# Edit SCHEDULE_TIMES in config.txt
SCHEDULE_TIMES=08:00,16:00,23:00

# Restart the service
```

### Update Code
```bash
git pull origin main
pip install -r requirements.txt --upgrade
sudo systemctl restart indian-news.service
```

## Security Best Practices

1. ✅ Never commit `config.txt` with real credentials
2. ✅ Use environment variables in production
3. ✅ Use app passwords, not real passwords
4. ✅ Restrict file permissions: `chmod 600 config.txt`
5. ✅ Use HTTPS/TLS for SMTP (port 587)
6. ✅ Regularly rotate API keys and passwords
7. ✅ Keep dependencies updated

## Cost Considerations

### Free Tier (Recommended for Personal Use)
- NewsAPI.org: Free (100 req/day)
- NewsData.io: Free (200 req/day)
- Gmail: Free
- Server: $5-10/month (DigitalOcean, Linode, etc.)

### Total Cost: $5-10/month

### Alternative: Free Options
- Heroku Free Tier (limited hours)
- Oracle Cloud Free Tier
- Google Cloud Free Tier
- Run on existing home server

## Support

For issues or questions:
1. Check logs: `news_scheduler.log`
2. Review troubleshooting section
3. Check API status pages
4. Verify email provider SMTP access

## Next Steps

After successful deployment:
1. ✅ Monitor first few email deliveries
2. ✅ Adjust schedule times if needed
3. ✅ Add more recipients
4. ✅ Customize email templates
5. ✅ Set up monitoring/alerts

---

**Congratulations! Your Indian News Fetcher is now deployed and running 24/7!** 🎉

You'll receive Indian news updates via email 3 times daily at your scheduled times.

