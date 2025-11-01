# Quick Start Guide - Indian News Fetcher

Get Indian news delivered to your email in 3 times daily in under 10 minutes!

## ⚡ 5-Minute Setup

### Step 1: Get API Key (2 minutes)

Choose **ONE** or **BOTH**:

**Option A - NewsAPI.org** (Recommended)
1. Go to https://newsapi.org/register
2. Enter email and create password
3. Verify email
4. Copy your API key

**Option B - NewsData.io** (Backup/Alternative)
1. Go to https://newsdata.io/register
2. Sign up
3. Copy your API key from dashboard

### Step 2: Setup Gmail App Password (3 minutes)

1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification**
3. Scroll to **App passwords**
4. Select **Mail** → **Other**
5. Name it "News Fetcher"
6. Copy the 16-character password

### Step 3: Configure (1 minute)

Edit `config.txt`:

```ini
NEWS_API_KEY=paste_your_newsapi_key_here
NEWSDATA_API_KEY=paste_your_newsdata_key_here  # optional but recommended

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=paste_16_char_app_password_here
RECIPIENT_EMAILS=your_email@gmail.com

SCHEDULE_TIMES=06:00,14:00,22:00
```

### Step 4: Install & Test (1 minute)

```bash
# Install dependencies
pip install -r requirements.txt

# Test immediately
python scheduler_app.py --test
```

✅ Check your email! You should receive a news update.

### Step 5: Run Continuously

```bash
# Windows
python scheduler_app.py

# Linux/Mac (background)
nohup python scheduler_app.py &
```

## 🎯 That's It!

You'll now receive Indian news updates at:
- 6:00 AM
- 2:00 PM  
- 10:00 PM

(or your custom times)

## 🔧 Common Issues

### "Authentication failed"
→ Use **App Password**, not your regular Gmail password!

### "No API key"
→ Make sure you copied the key correctly in `config.txt`

### "No articles found"
→ Check your internet connection and API key validity

## 📚 Need More Help?

- Detailed setup: See `README.md`
- Deployment: See `DEPLOYMENT_GUIDE.md`
- Logs: Check `news_scheduler.log`

## 🚀 Pro Tips

1. **Use both APIs** for better reliability
2. **Set API_PREFERENCE** to your primary choice
3. **Add multiple recipients** (comma-separated)
4. **Check logs** for troubleshooting
5. **Deploy to cloud** for 24/7 operation

## 📧 Email Not Arriving?

1. Check spam folder
2. Verify sender email can send via SMTP
3. Try sending test: `python email_sender.py`
4. Check `news_scheduler.log` for errors

## ⏰ Customize Schedule

Want different times? Edit `SCHEDULE_TIMES` in `config.txt`:

```ini
# Business hours only
SCHEDULE_TIMES=09:00,18:00

# Every 6 hours
SCHEDULE_TIMES=00:00,06:00,12:00,18:00

# Morning and evening
SCHEDULE_TIMES=07:00,19:00
```

## 🌟 Next Steps

**For Local Use:**
- Just keep the script running on your computer

**For 24/7 Operation:**
- Deploy to a cloud server (see `DEPLOYMENT_GUIDE.md`)
- Options: AWS, DigitalOcean, Heroku, etc.
- Cost: $5-10/month or free tier

---

**Enjoy your automated Indian news updates!** 📰🇮🇳

Questions? Check the full documentation in `README.md`

