#!/usr/bin/env python3
"""
Git Status Checker - Verifies what will be committed to GitHub
Checks that sensitive files are properly gitignored
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

def check_git_status():
    """Check git status to see what would be committed"""
    print("=" * 70)
    print("Git Status Check - Verifying what will be committed")
    print("=" * 70)
    print()
    
    # Check if git is initialized
    output, code = run_command("git status")
    if code != 0 and "not a git repository" in output:
        print("[WARNING] Git not initialized. Run 'git init' first.")
        return False
    
    # Get list of files that would be staged
    output, code = run_command("git status --short")
    
    if not output:
        print("[INFO] No changes to commit (working tree clean)")
        return True
    
    # Check for sensitive files
    sensitive_patterns = [
        'config.txt',
        'config/config.txt',
        '.env',
        '*.log',
        '*.key',
        '*.pem',
        '__pycache__',
        'logs/',
    ]
    
    lines = output.split('\n')
    sensitive_files = []
    safe_files = []
    
    for line in lines:
        if line.strip():
            status, filename = line.split(maxsplit=1)
            filename = filename.strip('"\'')
            
            # Check if it's a sensitive file
            is_sensitive = False
            for pattern in sensitive_patterns:
                if pattern in filename:
                    is_sensitive = True
                    break
            
            if is_sensitive:
                sensitive_files.append((status, filename))
            else:
                safe_files.append((status, filename))
    
    # Report results
    print("Files to be committed:")
    print()
    
    if safe_files:
        print("[OK] Safe files:")
        for status, filename in safe_files[:20]:  # Limit output
            print(f"  {status} {filename}")
        if len(safe_files) > 20:
            print(f"  ... and {len(safe_files) - 20} more")
        print()
    
    if sensitive_files:
        print("[FAIL] DANGER! Sensitive files detected:")
        for status, filename in sensitive_files:
            print(f"  {status} {filename}")
        print()
        print("[ACTION REQUIRED] These files contain secrets and should NOT be committed!")
        print("                 Add them to .gitignore immediately!")
        return False
    else:
        print("[OK] No sensitive files detected!")
        print()
    
    return True

def check_gitignore():
    """Check if .gitignore is properly configured"""
    print("=" * 70)
    print("Checking .gitignore file")
    print("=" * 70)
    print()
    
    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        print("[FAIL] .gitignore file not found!")
        print("        Create it to protect sensitive files.")
        return False
    
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_patterns = [
        'config.txt',
        'config/config.txt',
        '__pycache__',
        '*.log',
        '*.env',
    ]
    
    missing_patterns = []
    for pattern in required_patterns:
        if pattern not in content:
            missing_patterns.append(pattern)
    
    if missing_patterns:
        print("[WARNING] .gitignore missing some patterns:")
        for pattern in missing_patterns:
            print(f"  - {pattern}")
        print()
        return False
    else:
        print("[OK] .gitignore properly configured!")
        print()
        return True

def check_file_structure():
    """Check project structure"""
    print("=" * 70)
    print("Checking Project Structure")
    print("=" * 70)
    print()
    
    required_dirs = [
        'src/',
        'src/fetchers/',
        'src/services/',
        'config/',
        'scripts/',
        'docs/',
    ]
    
    required_files = [
        'src/fetchers/newsapi_fetcher.py',
        'src/fetchers/newsdata_fetcher.py',
        'src/services/news_service.py',
        'src/services/email_sender.py',
        'config/config.example.txt',
        'scheduler_app.py',
        'run.py',
        'requirements.txt',
        'README.md',
        '.gitignore',
    ]
    
    missing_dirs = []
    missing_files = []
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_dirs:
        print("[WARNING] Missing directories:")
        for dir_path in missing_dirs:
            print(f"  - {dir_path}")
        print()
    
    if missing_files:
        print("[WARNING] Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        print()
    
    if not missing_dirs and not missing_files:
        print("[OK] Project structure looks good!")
        print()
        return True
    
    return False

def check_config_security():
    """Check if config files contain secrets"""
    print("=" * 70)
    print("Checking Config Security")
    print("=" * 70)
    print()
    
    config_files = [
        'config/config.txt',
        'config.txt',
    ]
    
    example_file = Path('config/config.example.txt')
    
    if not example_file.exists():
        print("[WARNING] config/config.example.txt not found!")
        print("          Create it as a template without secrets.")
        return False
    
    # Check if real config files exist (they should NOT be committed)
    real_configs_exist = False
    for config_file in config_files:
        config_path = Path(config_file)
        if config_path.exists():
            # Try to read and check if it has real secrets (not placeholders)
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Check for placeholder patterns
                    if 'your_' in content or 'example.com' in content:
                        print(f"[OK] {config_file} appears to be a template")
                    else:
                        print(f"[INFO] {config_file} exists (should be gitignored)")
                        real_configs_exist = True
            except Exception as e:
                print(f"[INFO] Could not read {config_file}: {e}")
    
    print("[OK] Config security check complete!")
    print()
    return True

def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("Git Security & Structure Check")
    print("=" * 70)
    print()
    
    results = {}
    
    # Run checks
    results['gitignore'] = check_gitignore()
    results['structure'] = check_file_structure()
    results['config'] = check_config_security()
    results['git_status'] = check_git_status()
    
    # Summary
    print("=" * 70)
    print("Check Summary")
    print("=" * 70)
    print()
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"Total Checks: {total}")
    print(f"[OK] Passed: {passed}")
    print(f"[FAIL] Failed: {total - passed}")
    print()
    
    if passed == total:
        print("[SUCCESS] All checks passed! Safe to commit to GitHub.")
        print()
        print("Next steps:")
        print("  1. Review files with: git status")
        print("  2. Add files: git add .")
        print("  3. Commit: git commit -m 'Your message'")
        print("  4. Push: git push")
    else:
        print("[WARNING] Some checks failed. Fix issues before committing!")
        print()
        print("Common fixes:")
        print("  - Add missing files to .gitignore")
        print("  - Remove sensitive files from staging: git reset <file>")
        print("  - Verify .gitignore includes config.txt and *.log")
    
    print()
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nCheck interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

