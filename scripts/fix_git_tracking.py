#!/usr/bin/env python3
"""
Fix Git Tracking - Untrack files that should be gitignored
This removes files from git tracking but keeps them on disk
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return f"Error: {e}", 1

def untrack_files():
    """Untrack files that should be gitignored"""
    print("=" * 70)
    print("Untracking Sensitive/Old Files from Git")
    print("=" * 70)
    print()
    
    # Files that should NOT be tracked (already in .gitignore)
    files_to_untrack = [
        'config.txt',                    # Old config with secrets
        'config/config.txt',             # New config with secrets
        'news_fetcher.py',               # Old file (use src/fetchers/)
        'newsdata_fetcher.py',           # Old file (use src/fetchers/)
        'email_sender.py',               # Old file (use src/services/)
        'news_service.py',               # Old file (use src/services/)
        'simple_news_fetcher.py',        # Old file
        'better_news_fetcher.py',        # Old file
        'debug_news_fetcher.py',         # Old file
        'api_test.py',                   # Old test file
        'simple_test.py',                # Old test file
        'test_news_fetcher.py',          # Old test file
        'verify_improvements.py',        # Old file
        'news_scheduler.log',            # Log file
        'news_dashboard.html',           # Generated file
        'youtube_news_content.txt',      # Generated file
        'better_youtube_news_content.txt', # Generated file
        'test_results.txt',              # Generated file
    ]
    
    # Check if git is initialized
    output, code = run_command("git status")
    if code != 0 and "not a git repository" in output:
        print("[INFO] Git not initialized. Nothing to untrack.")
        return True
    
    # Get list of tracked files
    output, code = run_command("git ls-files")
    if code != 0:
        print(f"[ERROR] Could not list git files: {output}")
        return False
    
    tracked_files = output.split('\n')
    
    files_to_remove = []
    for file_path in files_to_untrack:
        if file_path in tracked_files:
            files_to_remove.append(file_path)
    
    if not files_to_remove:
        print("[OK] No tracked files need to be untracked!")
        print()
        return True
    
    print(f"[INFO] Found {len(files_to_remove)} tracked files that should be untracked:")
    for file_path in files_to_remove:
        print(f"  - {file_path}")
    print()
    
    # Ask for confirmation (in non-interactive mode, just proceed)
    print("[INFO] Untracking files (keeping on disk)...")
    print()
    
    success = True
    for file_path in files_to_remove:
        # Check if file exists
        if not Path(file_path).exists():
            print(f"[SKIP] {file_path} (not found on disk)")
            continue
        
        # Remove from git index but keep on disk
        output, code = run_command(f'git rm --cached "{file_path}"')
        if code == 0:
            print(f"[OK] Untracked: {file_path}")
        else:
            print(f"[FAIL] Could not untrack {file_path}: {output}")
            success = False
    
    print()
    if success:
        print("[SUCCESS] All files untracked successfully!")
        print()
        print("Next steps:")
        print("  1. Verify with: git status")
        print("  2. Review .gitignore to ensure these files are excluded")
        print("  3. Commit changes: git commit -m 'Untrack sensitive files'")
    else:
        print("[WARNING] Some files could not be untracked.")
        print("          Check manually and remove from git if needed.")
    
    print()
    return success

def main():
    """Main function"""
    try:
        success = untrack_files()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

