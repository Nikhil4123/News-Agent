#!/usr/bin/env python3
"""
Main entry point for Indian News Fetcher
Run: python run.py
"""

import sys
from pathlib import Path

# Add src to path if running from project root
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scheduler_app import main

if __name__ == "__main__":
    main()

