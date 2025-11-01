# GitHub Setup Checklist

## ✅ Before Pushing to GitHub

### 1. Verify .gitignore is working
```bash
# Check what will be committed
git status

# Verify config/config.txt is NOT listed (it's in .gitignore)
```

### 2. Ensure no secrets are in code
- [ ] No API keys in any files
- [ ] No passwords in any files
- [ ] `config/config.txt` is in .gitignore
- [ ] Only `config/config.example.txt` will be committed

### 3. Create your config file locally
```bash
# This file is gitignored - never commit it!
cp config/config.example.txt config/config.txt
# Edit config/config.txt with your real credentials
```

### 4. Test the structure
```bash
# Test that everything works with new structure
python scripts/test_setup.py
python scripts/test_email_now.py
python run.py --test
```

### 5. Format code (optional but recommended)
```bash
# Install black if you want
pip install black

# Format all Python files
black src/ scripts/ *.py
```

### 6. Commit and push
```bash
# Initialize git (if not done)
git init

# Add all files (except gitignored ones)
git add .

# Commit
git commit -m "Initial commit: Restructured codebase for GitHub"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/indian-news-fetcher.git

# Push
git push -u origin main
```

## 📁 What Will Be Committed

✅ **Safe to commit:**
- `src/` - All source code (no secrets)
- `config/config.example.txt` - Template only (no real keys)
- `scripts/` - Test scripts
- `docs/` - Documentation
- `requirements.txt` - Dependencies
- `.gitignore` - Ignore rules
- `README.md`, `LICENSE`, etc.

❌ **NOT committed (in .gitignore):**
- `config/config.txt` - Your real config with secrets
- `logs/` - Log files
- `__pycache__/` - Python cache
- `*.log` - Any log files
- `.env` - Environment files
- `venv/` - Virtual environment

## 🔒 Security Checklist

- [ ] `.gitignore` includes `config/config.txt`
- [ ] `.gitignore` includes `*.env`
- [ ] `.gitignore` includes `logs/`
- [ ] No API keys in code
- [ ] No passwords in code
- [ ] `config/config.example.txt` has placeholder values only
- [ ] Test that `git status` doesn't show sensitive files

## 📝 Recommended Repository Structure

```
indian-news-fetcher/
├── .gitignore              ✅ Committed
├── LICENSE                 ✅ Committed
├── README.md               ✅ Committed
├── CONTRIBUTING.md         ✅ Committed
├── SETUP.md                ✅ Committed
├── requirements.txt        ✅ Committed
├── run.py                  ✅ Committed
├── scheduler_app.py        ✅ Committed
├── src/                    ✅ Committed (all code)
├── config/
│   └── config.example.txt  ✅ Committed (template only)
├── scripts/                ✅ Committed
├── docs/                   ✅ Committed
└── tests/                  ✅ Committed
```

## 🚀 After First Push

1. **Add repository description** on GitHub
2. **Add topics** (e.g., python, news, email, automation)
3. **Add badges** to README (optional):
   ```markdown
   ![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
   ![License](https://img.shields.io/badge/license-MIT-green.svg)
   ```
4. **Enable Issues** for bug reports and feature requests
5. **Create releases** when ready

## 📋 Optional: GitHub Actions

Consider adding `.github/workflows/tests.yml` for CI/CD:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python scripts/test_setup.py
```

---

**Ready to push!** Make sure all secrets are in `.gitignore`! 🔒

