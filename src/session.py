"""Session management for LeetCode CLI tool."""

import os
import logging
from typing import Optional

from .config import Config


class SessionManager:
    """Manages LeetCode session tokens."""
    
    def __init__(self, session_file: str = Config.SESSION_FILE):
        """Initialize session manager.
        
        Args:
            session_file: Path to the session file
        """
        self.session_file = session_file
        self.session_token: Optional[str] = None
        self.logger = logging.getLogger(__name__)
    
    def load_session(self) -> bool:
        """Load session token from file.
        
        Returns:
            True if session loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(self.session_file):
                self.logger.error(f"Session file '{self.session_file}' not found.")
                print(f"Session file '{self.session_file}' not found.")
                print("Please create the session file with your LeetCode session token.")
                return False
            
            with open(self.session_file, 'r', encoding='utf-8') as f:
                token = f.read().strip()
                
            if not token:
                self.logger.error("Session file is empty.")
                print("Session file is empty.")
                return False
            
            self.session_token = token
            self.logger.info("Session loaded successfully.")
            return True
            
        except IOError as e:
            self.logger.error(f"Error reading session file: {e}")
            print(f"Error reading session file: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error loading session: {e}")
            print(f"Unexpected error loading session: {e}")
            return False
    
    def save_session(self, token: str) -> bool:
        """Save session token to file.
        
        Args:
            token: Session token to save
            
        Returns:
            True if session saved successfully, False otherwise
        """
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                f.write(token)
            
            self.session_token = token
            self.logger.info("Session saved successfully.")
            return True
            
        except IOError as e:
            self.logger.error(f"Error saving session file: {e}")
            print(f"Error saving session file: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error saving session: {e}")
            print(f"Unexpected error saving session: {e}")
            return False
    
    def get_session_cookies(self) -> dict:
        """Get session cookies for API requests.
        
        Returns:
            Dictionary containing session cookies
        """
        if not self.session_token:
            return {}
        
        return {"LEETCODE_SESSION": self.session_token}
    
    def is_session_loaded(self) -> bool:
        """Check if session is loaded.
        
        Returns:
            True if session is loaded, False otherwise
        """
        return self.session_token is not None
