"""Test cases for session management."""

import unittest
import tempfile
import os
from unittest.mock import patch, mock_open
import sys

# Add parent directory to path to import src modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from src.session import SessionManager


class TestSessionManager(unittest.TestCase):
    """Test cases for SessionManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.session_manager = SessionManager(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_load_session_success(self):
        """Test successful session loading."""
        test_token = "test_session_token"
        
        with open(self.temp_file.name, 'w') as f:
            f.write(test_token)
        
        result = self.session_manager.load_session()
        
        self.assertTrue(result)
        self.assertEqual(self.session_manager.session_token, test_token)
    
    def test_load_session_file_not_found(self):
        """Test session loading when file doesn't exist."""
        os.unlink(self.temp_file.name)
        
        result = self.session_manager.load_session()
        
        self.assertFalse(result)
        self.assertIsNone(self.session_manager.session_token)
    
    def test_load_session_empty_file(self):
        """Test session loading when file is empty."""
        with open(self.temp_file.name, 'w') as f:
            f.write("")
        
        result = self.session_manager.load_session()
        
        self.assertFalse(result)
        self.assertIsNone(self.session_manager.session_token)
    
    def test_save_session(self):
        """Test session saving."""
        test_token = "new_test_token"
        
        result = self.session_manager.save_session(test_token)
        
        self.assertTrue(result)
        self.assertEqual(self.session_manager.session_token, test_token)
        
        # Verify file content
        with open(self.temp_file.name, 'r') as f:
            content = f.read()
        self.assertEqual(content, test_token)
    
    def test_get_session_cookies(self):
        """Test getting session cookies."""
        test_token = "test_token"
        self.session_manager.session_token = test_token
        
        cookies = self.session_manager.get_session_cookies()
        
        expected = {"LEETCODE_SESSION": test_token}
        self.assertEqual(cookies, expected)
    
    def test_get_session_cookies_no_token(self):
        """Test getting session cookies when no token is loaded."""
        cookies = self.session_manager.get_session_cookies()
        
        self.assertEqual(cookies, {})
    
    def test_is_session_loaded(self):
        """Test session loaded check."""
        # Initially no session
        self.assertFalse(self.session_manager.is_session_loaded())
        
        # After setting token
        self.session_manager.session_token = "test_token"
        self.assertTrue(self.session_manager.is_session_loaded())


if __name__ == '__main__':
    unittest.main()
