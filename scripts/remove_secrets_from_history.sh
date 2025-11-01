#!/bin/bash
# Script to remove config.txt from git history
# WARNING: This rewrites git history!

echo "=========================================="
echo "REMOVE SECRETS FROM GIT HISTORY"
echo "=========================================="
echo ""
echo "WARNING: This will rewrite git history!"
echo "Make sure you've rotated all exposed credentials first!"
echo ""
read -p "Have you rotated all API keys and passwords? (yes/no): " rotated

if [ "$rotated" != "yes" ]; then
    echo ""
    echo "ERROR: Please rotate all credentials FIRST!"
    echo "See SECURITY_BREACH_FIX.md for instructions"
    exit 1
fi

echo ""
echo "Removing config.txt from git history..."

# Remove from git index
git rm --cached config.txt 2>/dev/null

# Remove from all commits in history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config.txt" \
  --prune-empty --tag-name-filter cat -- --all

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo ""
echo "Done! Now force push to GitHub:"
echo "  git push origin --force --all"
echo ""
echo "WARNING: This will rewrite history on GitHub!"
echo "Tell collaborators to re-clone the repository."

