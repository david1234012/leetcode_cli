#!/usr/bin/env python3
"""
Simple test version of the LeetCode CLI Tool
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Test imports
try:
    from src.config import Config, QuestionStatus, Actions
    from src.models import QuestionFilter
    from src.session import SessionManager
    from src.api import LeetCodeAPI
    from src.formatters import OutputFormatter
    print("✓ All modules imported successfully!")
    
    # Test basic functionality
    print("✓ Testing configuration...")
    print(f"  API URL: {Config.LEETCODE_API_URL}")
    print(f"  Session file: {Config.SESSION_FILE}")
    
    print("✓ Testing question status constants...")
    print(f"  Available statuses: {QuestionStatus.all()}")
    
    print("✓ Testing session manager...")
    session_manager = SessionManager()
    print(f"  Session loaded: {session_manager.is_session_loaded()}")
    
    print("✓ All basic tests passed!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
