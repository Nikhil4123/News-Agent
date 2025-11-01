# ⚡ Quick Fix: Remove Secrets from GitHub

## 🚨 Secrets Were Committed - Fix Now!

Your `config.txt` with secrets was committed. Follow these steps IMMEDIATELY:

## Step-by-Step Fix

### 1. Rotate Credentials First (CRITICAL!)

**NewsAPI.org:**
1. Visit: https://newsapi.org/account
2. Find key: `71777e8c885643adaada0f2a3288fe9f`
3. Click "Revoke" or "Delete"
4. Generate NEW key
5. Copy new key

**NewsData.io:**
1. Visit: https://newsdata.io/dashboard
2. Find key: `pub_4df1799350014b899e79e9d7c3e8f890`
3. Delete/Revoke it
4. Generate NEW key
5. Copy new key

**Gmail App Password:**
1. Visit: https://myaccount.google.com/apppasswords
2. Delete password: `yhxq pffk sfmf elxu`
3. Generate NEW app password
4. Copy new password

### 2. Remove from Git History

**Windows PowerShell:**
```powershell
# Remove from tracking
git rm --cached config.txt

# Remove from all commits
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch config.txt" --prune-empty --tag-name-filter cat -- --all

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

**Or use script:**
```powershell
powershell -ExecutionPolicy Bypass -File scripts/remove_secrets_from_history.ps1
```

### 3. Force Push to GitHub

```bash
git push origin --force --all
```

**⚠️ WARNING:** This rewrites history! Anyone who cloned needs to re-clone.

### 4. Update Local Config

Edit `config/config.txt` with NEW credentials:
```ini
NEWS_API_KEY=your_NEW_newsapi_key_from_step_1
NEWSDATA_API_KEY=your_NEW_newsdata_key_from_step_1
SENDER_PASSWORD=your_NEW_app_password_from_step_1
```

### 5. Verify Fix

```bash
# Check config.txt is not in history
git log --all --full-history -- config.txt
# Should return: (nothing)

# Verify .gitignore works
git check-ignore -v config.txt
# Should show: .gitignore:39:config.txt  config.txt

# Check what will be committed
git status
# Should NOT show config.txt
```

## ✅ Done!

Your secrets are now:
1. ✅ Rotated (old keys revoked)
2. ✅ Removed from git history
3. ✅ Removed from GitHub
4. ✅ Protected by .gitignore

## 📋 Reminder

- ✅ `.gitignore` already excludes `config.txt` and `config/config.txt`
- ✅ Never commit config files with real secrets
- ✅ Always use `config/config.example.txt` as template
- ✅ Use environment variables in production

---

**All secrets have been handled!** 🔒

