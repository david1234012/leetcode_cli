#!/usr/bin/env python3
"""
LeetCode CLI Tool
A modern command-line interface for interacting with the LeetCode platform.
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from src.cli import main
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running this script from the correct directory.")
    sys.exit(1)

if __name__ == '__main__':
    sys.exit(main())
