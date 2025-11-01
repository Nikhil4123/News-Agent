# 🚨 SECURITY BREACH: Secrets Exposed on GitHub

## ⚠️ CRITICAL: Secrets Were Committed

GitGuardian detected that your `config.txt` with real secrets was committed to GitHub in commit `c2ed93d`.

**Exposed Secrets:**
- ❌ NewsAPI.org API Key: `71777e8c885643adaada0f2a3288fe9f`
- ❌ NewsData.io API Key: `pub_4df1799350014b899e79e9d7c3e8f890`
- ❌ Gmail App Password: `yhxq pffk sfmf elxu`
- ❌ Email Addresses: Multiple recipients

## 🔒 IMMEDIATE ACTION REQUIRED

### Step 1: Rotate ALL Compromised Credentials (DO THIS FIRST!)

**1. Rotate NewsAPI.org Key:**
1. Go to https://newsapi.org/account
2. Revoke the old key: `71777e8c885643adaada0f2a3288fe9f`
3. Generate a new API key
4. Update your `config/config.txt` with the new key

**2. Rotate NewsData.io Key:**
1. Go to https://newsdata.io/dashboard
2. Revoke the old key: `pub_4df1799350014b899e79e9d7c3e8f890`
3. Generate a new API key
4. Update your `config/config.txt` with the new key

**3. Rotate Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Delete the compromised app password
3. Generate a new app password
4. Update your `config/config.txt` with the new password

**4. Consider Email Security:**
- Change your Gmail password if you think it might be compromised
- Review recent account activity
- Enable 2-factor authentication if not already enabled

### Step 2: Remove Secrets from Git History

You need to remove the secrets from GitHub history. Choose one method:

#### Method A: BFG Repo Cleaner (Recommended - Easier)

```bash
# 1. Download BFG from https://rtyley.github.io/bfg-repo-cleaner/

# 2. Clone a fresh copy of your repo
git clone --mirror https://github.com/Nikhil4123/News-Agent.git
cd News-Agent.git

# 3. Remove config.txt from history
java -jar bfg.jar --delete-files config.txt

# 4. Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 5. Force push (WARNING: This rewrites history!)
git push --force
```

#### Method B: git-filter-repo (Alternative)

```bash
# Install git-filter-repo first
pip install git-filter-repo

# Remove config.txt from entire history
git filter-repo --path config.txt --invert-paths

# Force push to GitHub
git push origin --force --all
```

#### Method C: Manual Git Commands (If above don't work)

```bash
# Remove from latest commit
git rm --cached config.txt
git commit --amend -m "Remove config.txt from repository"

# Remove from history (if it was in previous commits)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config.txt" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all
```

### Step 3: Verify Removal

After cleaning history:
```bash
# Check that config.txt is not in any commit
git log --all --full-history -- config.txt
# Should return nothing

# Verify .gitignore is working
git check-ignore -v config.txt
# Should show: .gitignore:39:config.txt  config.txt
```

### Step 4: Update All Credentials Locally

Update your local `config/config.txt` with the NEW rotated credentials:
```ini
# Use NEW keys (not the old ones!)
NEWS_API_KEY=your_NEW_newsapi_key_here
NEWSDATA_API_KEY=your_NEW_newsdata_key_here
SENDER_PASSWORD=your_NEW_app_password_here
```

### Step 5: Verify Security

```bash
# Run security check
python scripts/check_git_status.py

# Should show:
# [OK] No sensitive files detected!
```

## ⚠️ Important Notes

1. **Force Push Warning**: Force pushing rewrites history. Anyone who cloned the repo will need to re-clone.

2. **GitHub Secrets Scanner**: After removing secrets, GitHub may still show them in their security alerts. This is normal - it takes time to update.

3. **Backup First**: Make a backup before force pushing:
   ```bash
   git clone https://github.com/Nikhil4123/News-Agent.git backup-repo
   ```

4. **After Force Push**: Tell collaborators to re-clone:
   ```bash
   git fetch origin
   git reset --hard origin/main
   ```

## 🔒 Prevention for Future

1. **Always check before committing:**
   ```bash
   git status
   git diff
   ```

2. **Use pre-commit hooks** (optional):
   ```bash
   pip install pre-commit
   # Install git-secrets or similar
   ```

3. **Never commit**:
   - `config.txt`
   - `config/config.txt`
   - Any file with `.env`
   - Any file with real passwords

4. **Use environment variables** in production:
   ```bash
   export NEWS_API_KEY="your_key"
   export SENDER_PASSWORD="your_password"
   ```

## 📋 Quick Reference

**Exposed Secrets:**
- NewsAPI Key: `71777e8c885643adaada0f2a3288fe9f` → **REVOKE NOW**
- NewsData Key: `pub_4df1799350014b899e79e9d7c3e8f890` → **REVOKE NOW**
- Gmail Password: `yhxq pffk sfmf elxu` → **REVOKE NOW**

**Action Items:**
1. ✅ Rotate all API keys
2. ✅ Rotate Gmail app password
3. ✅ Remove from git history
4. ✅ Force push cleaned history
5. ✅ Update local config with new keys
6. ✅ Verify security

---

**SECURITY PRIORITY: Rotate credentials IMMEDIATELY before removing from git history!**

Once secrets are exposed, assume they're compromised. Always rotate first, then clean history.

