# PowerShell script to remove config.txt from git history
# WARNING: This rewrites git history!

Write-Host "==========================================" -ForegroundColor Red
Write-Host "REMOVE SECRETS FROM GIT HISTORY" -ForegroundColor Red
Write-Host "==========================================" -ForegroundColor Red
Write-Host ""
Write-Host "WARNING: This will rewrite git history!" -ForegroundColor Yellow
Write-Host "Make sure you've rotated all exposed credentials first!" -ForegroundColor Yellow
Write-Host ""

$rotated = Read-Host "Have you rotated all API keys and passwords? (yes/no)"

if ($rotated -ne "yes") {
    Write-Host ""
    Write-Host "ERROR: Please rotate all credentials FIRST!" -ForegroundColor Red
    Write-Host "See SECURITY_BREACH_FIX.md for instructions"
    exit 1
}

Write-Host ""
Write-Host "Removing config.txt from git history..." -ForegroundColor Yellow

# Remove from git index
git rm --cached config.txt 2>$null

# Remove from all commits in history using filter-branch
Write-Host "Removing from all commits..." -ForegroundColor Yellow
git filter-branch --force --index-filter `
  "git rm --cached --ignore-unmatch config.txt" `
  --prune-empty --tag-name-filter cat -- --all

# Clean up
Write-Host "Cleaning up..." -ForegroundColor Yellow
git reflog expire --expire=now --all
git gc --prune=now --aggressive

Write-Host ""
Write-Host "Done! Now force push to GitHub:" -ForegroundColor Green
Write-Host "  git push origin --force --all" -ForegroundColor Cyan
Write-Host ""
Write-Host "WARNING: This will rewrite history on GitHub!" -ForegroundColor Red
Write-Host "Tell collaborators to re-clone the repository." -ForegroundColor Yellow

