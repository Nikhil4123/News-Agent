# 🚨 URGENT: Secrets Exposed on GitHub - Fix Immediately

## 🔴 CRITICAL SECURITY BREACH

Your secrets were committed to GitHub in commit `c2ed93d`:
- API Keys exposed
- Email passwords exposed
- Email addresses exposed

**Repository**: `Nikhil4123/News-Agent`

## ⚡ IMMEDIATE ACTION (Do This NOW!)

### STEP 1: Rotate All Credentials (MOST IMPORTANT!)

**⏰ Do this FIRST - before removing from git!**

1. **Rotate NewsAPI.org Key:**
   - Go to: https://newsapi.org/account
   - Revoke: `71777e8c885643adaada0f2a3288fe9f`
   - Generate NEW key

2. **Rotate NewsData.io Key:**
   - Go to: https://newsdata.io/dashboard
   - Revoke: `pub_4df1799350014b899e79e9d7c3e8f890`
   - Generate NEW key

3. **Rotate Gmail App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Delete password: `yhxq pffk sfmf elxu`
   - Generate NEW app password

### STEP 2: Remove from Git History

After rotating credentials, clean git history:

```bash
# Option 1: Use PowerShell script (Windows)
powershell -ExecutionPolicy Bypass -File scripts/remove_secrets_from_history.ps1

# Option 2: Manual commands
git rm --cached config.txt
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch config.txt" --prune-empty --tag-name-filter cat -- --all
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### STEP 3: Force Push to GitHub

```bash
# This removes secrets from GitHub
git push origin --force --all

# WARNING: This rewrites history!
# Anyone who cloned needs to re-clone
```

### STEP 4: Update Local Config

Update `config/config.txt` with NEW credentials (from Step 1):
```ini
NEWS_API_KEY=your_NEW_newsapi_key
NEWSDATA_API_KEY=your_NEW_newsdata_key
SENDER_PASSWORD=your_NEW_app_password
```

## ✅ Verification

```bash
# Verify config.txt is not in history
git log --all --full-history -- config.txt
# Should return nothing

# Verify it's gitignored
git check-ignore -v config.txt
# Should show: .gitignore:39:config.txt

# Check what will be committed
python scripts/check_git_status.py
```

## 📋 Quick Checklist

- [ ] Rotate NewsAPI.org key
- [ ] Rotate NewsData.io key  
- [ ] Rotate Gmail app password
- [ ] Remove config.txt from git history
- [ ] Force push to GitHub
- [ ] Update local config with new keys
- [ ] Verify secrets are removed
- [ ] Test application with new keys

## ⚠️ Important Notes

1. **History Rewriting**: Force pushing rewrites history. If others have cloned, they need to re-clone.

2. **GitHub Alerts**: GitHub may still show alerts for a few days - that's normal.

3. **Backup First**: Make a backup before force pushing:
   ```bash
   git clone https://github.com/Nikhil4123/News-Agent.git backup
   ```

4. **Public Repository**: If repo is public, assume keys are compromised. Always rotate.

---

**PRIORITY ORDER:**
1. 🔴 Rotate credentials (MOST IMPORTANT)
2. 🟡 Remove from git history
3. 🟢 Update local config
4. ✅ Verify security

**See `SECURITY_BREACH_FIX.md` for detailed instructions.**

