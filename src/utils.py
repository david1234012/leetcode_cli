"""Utilities for the LeetCode CLI tool."""

import os
import shutil
from typing import Tuple


def get_terminal_size() -> Tuple[int, int]:
    """Get the current terminal size.
    
    Returns:
        Tuple of (width, height) of the terminal
    """
    try:
        # Try to get terminal size using shutil (Python 3.3+)
        size = shutil.get_terminal_size()
        return size.columns, size.lines
    except (AttributeError, OSError):
        # Fallback to environment variables or default
        try:
            width = int(os.environ.get('COLUMNS', 80))
            height = int(os.environ.get('LINES', 24))
            return width, height
        except (ValueError, TypeError):
            # Default size if all else fails
            return 80, 24


def calculate_column_widths(terminal_width: int, min_title_width: int = 20) -> dict:
    """Calculate optimal column widths based on terminal size.
    
    Args:
        terminal_width: Width of the terminal
        min_title_width: Minimum width for title column
        
    Returns:
        Dictionary with column widths
    """
    # Fixed column widths for non-title columns
    fixed_widths = {
        'id': 6,
        'difficulty': 10,
        'status': 12,
        'rate': 8,
        'separators': 4  # spaces between columns
    }
    
    # Calculate remaining width for title
    used_width = sum(fixed_widths.values())
    available_width = terminal_width - used_width
    
    # Ensure minimum title width
    title_width = max(min_title_width, available_width)
    
    return {
        'id': fixed_widths['id'],
        'title': title_width,
        'difficulty': fixed_widths['difficulty'],
        'status': fixed_widths['status'],
        'rate': fixed_widths['rate']
    }


def truncate_with_ellipsis(text: str, max_width: int) -> str:
    """Truncate text with ellipsis if it's too long.
    
    Args:
        text: Text to truncate
        max_width: Maximum width allowed
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_width:
        return text
    
    if max_width <= 3:
        return "..."[:max_width]
    
    return text[:max_width - 3] + "..."


def smart_wrap_title(title: str, max_width: int, preserve_words: bool = True) -> str:
    """Smart title wrapping that tries to preserve word boundaries.
    
    Args:
        title: Title to wrap
        max_width: Maximum width for the title
        preserve_words: Whether to try to preserve word boundaries
        
    Returns:
        Wrapped or truncated title
    """
    if len(title) <= max_width:
        return title
    
    if not preserve_words:
        return truncate_with_ellipsis(title, max_width)
    
    # Try to find a good break point
    words = title.split()
    result = ""
    
    for word in words:
        test_result = result + (" " if result else "") + word
        if len(test_result) <= max_width - 3:  # Reserve space for ellipsis
            result = test_result
        else:
            break
    
    if result and len(result) < len(title):
        return result + "..."
    else:
        # Fallback to character truncation
        return truncate_with_ellipsis(title, max_width)
