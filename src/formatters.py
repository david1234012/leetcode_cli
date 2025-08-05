"""Output formatters for the LeetCode CLI tool."""

import json
import csv
from typing import List, Dict, Any
from io import StringIO

from .models import Question, UserInfo
from .utils import get_terminal_size, calculate_column_widths, smart_wrap_title


class OutputFormatter:
    """Formats output for different display formats."""
    
    @staticmethod
    def format_questions_table(questions: List[Question]) -> str:
        """Format questions as a table.
        
        Args:
            questions: List of questions to format
            
        Returns:
            Formatted table string
        """
        if not questions:
            return "No questions found."
        
        output = []
        
        for i, q in enumerate(questions, 1):
            topics_str = ", ".join(q.topics) if q.topics else "None"
            status_str = q.status or "Not Attempted"
            
            output.append(f"{'='*60}")
            output.append(f"Question #{i}")
            output.append(f"ID             : {q.id}")
            output.append(f"Title          : {q.title}")
            output.append(f"Difficulty     : {q.difficulty}")
            output.append(f"Status         : {status_str}")
            output.append(f"Topics         : {topics_str}")
            output.append(f"Acceptance Rate: {q.acceptance_rate:.1f}%")
            output.append(f"Paid Only      : {'Yes' if q.is_paid_only else 'No'}")
            output.append(f"URL            : {q.url}")
            output.append("")
        
        output.append("="*60)
        output.append(f"Total Questions: {len(questions)}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_questions_summary(questions: List[Question]) -> str:
        """Format questions as a summary table with dynamic column widths.
        
        Args:
            questions: List of questions to format
            
        Returns:
            Formatted summary string
        """
        if not questions:
            return "No questions found."
        
        # Get terminal size and calculate column widths
        terminal_width, _ = get_terminal_size()
        widths = calculate_column_widths(terminal_width)
        
        # Header
        output = []
        header = (f"{'ID':<{widths['id']}} "
                 f"{'Title':<{widths['title']}} "
                 f"{'Difficulty':<{widths['difficulty']}} "
                 f"{'Status':<{widths['status']}} "
                 f"Rate")
        output.append(header)
        
        # Dynamic separator line  
        total_width = widths['id'] + widths['title'] + widths['difficulty'] + widths['status'] + 8 + 4  # Rate + spaces
        output.append("-" * total_width)
        
        # Questions
        for q in questions:
            # Smart title handling
            title = smart_wrap_title(q.title, widths['title'])
            status = (q.status or "Not Attempted")
            if len(status) > widths['status']:
                status = status[:widths['status']-1] + "…"
            
            rate = f"{q.acceptance_rate:.1f}%"
            
            row = (f"{q.id:<{widths['id']}} "
                  f"{title:<{widths['title']}} "
                  f"{q.difficulty:<{widths['difficulty']}} "
                  f"{status:<{widths['status']}} "
                  f"{rate}")
            output.append(row)
        
        output.append("-" * total_width)
        output.append(f"Total Questions: {len(questions)}")
        
        # Add terminal info for debugging (optional)
        if terminal_width < 100:
            output.append(f"(Terminal width: {terminal_width}, Title column: {widths['title']})")
        
        return "\n".join(output)
    
    @staticmethod
    def format_questions_wide(questions: List[Question]) -> str:
        """Format questions in wide format with full titles.
        
        Args:
            questions: List of questions to format
            
        Returns:
            Formatted wide table string
        """
        if not questions:
            return "No questions found."
        
        # Calculate maximum title length for better formatting
        max_title_len = max(len(q.title) for q in questions) if questions else 20
        title_width = min(max_title_len + 2, 80)  # Cap at 80 chars
        
        # Fixed widths for other columns
        widths = {
            'id': 6,
            'title': title_width,
            'difficulty': 10,
            'status': 15,
            'rate': 8
        }
        
        # Header
        output = []
        header = (f"{'ID':<{widths['id']}} "
                 f"{'Title':<{widths['title']}} "
                 f"{'Difficulty':<{widths['difficulty']}} "
                 f"{'Status':<{widths['status']}} "
                 f"{'Rate':<{widths['rate']}}")
        output.append(header)
        
        # Separator line
        separator_length = sum(widths.values()) + 4
        output.append("=" * separator_length)
        
        # Questions
        for q in questions:
            status = q.status or "Not Attempted"
            rate = f"{q.acceptance_rate:.1f}%"
            
            row = (f"{q.id:<{widths['id']}} "
                  f"{q.title:<{widths['title']}} "
                  f"{q.difficulty:<{widths['difficulty']}} "
                  f"{status:<{widths['status']}} "
                  f"{rate:<{widths['rate']}}")
            output.append(row)
        
        output.append("=" * separator_length)
        output.append(f"Total Questions: {len(questions)}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_questions_json(questions: List[Question]) -> str:
        """Format questions as JSON.
        
        Args:
            questions: List of questions to format
            
        Returns:
            JSON formatted string
        """
        data = {
            "total_count": len(questions),
            "questions": [q.to_dict() for q in questions]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def format_questions_csv(questions: List[Question]) -> str:
        """Format questions as CSV.
        
        Args:
            questions: List of questions to format
            
        Returns:
            CSV formatted string
        """
        if not questions:
            return "No questions found."
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'ID', 'Title', 'Difficulty', 'Status', 'Topics', 
            'Acceptance Rate', 'Paid Only', 'URL'
        ])
        
        # Data
        for q in questions:
            topics_str = "; ".join(q.topics) if q.topics else ""
            writer.writerow([
                q.id,
                q.title,
                q.difficulty,
                q.status or "Not Attempted",
                topics_str,
                q.acceptance_rate,
                q.is_paid_only,
                q.url
            ])
        
        return output.getvalue()
    
    @staticmethod
    def format_user_info(user_info: UserInfo) -> str:
        """Format user information.
        
        Args:
            user_info: User information to format
            
        Returns:
            Formatted user info string
        """
        output = []
        output.append(f"User: {user_info.username}")
        
        if user_info.solved_counts:
            output.append("Solved Problems:")
            total_solved = 0
            for difficulty, count in user_info.solved_counts.items():
                output.append(f"  {difficulty}: {count}")
                total_solved += count
            output.append(f"  Total: {total_solved}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_statistics(questions: List[Question]) -> str:
        """Format question statistics.
        
        Args:
            questions: List of questions to analyze
            
        Returns:
            Formatted statistics string
        """
        if not questions:
            return "No questions to analyze."
        
        # Count by difficulty
        difficulty_counts = {}
        status_counts = {}
        
        for q in questions:
            # Difficulty stats
            difficulty_counts[q.difficulty] = difficulty_counts.get(q.difficulty, 0) + 1
            
            # Status stats
            status = q.status or "Not Attempted"
            status_counts[status] = status_counts.get(status, 0) + 1
        
        output = []
        output.append("Question Statistics:")
        output.append("-" * 30)
        
        output.append("By Difficulty:")
        for difficulty, count in sorted(difficulty_counts.items()):
            percentage = (count / len(questions)) * 100
            output.append(f"  {difficulty}: {count} ({percentage:.1f}%)")
        
        output.append("\nBy Status:")
        for status, count in sorted(status_counts.items()):
            percentage = (count / len(questions)) * 100
            output.append(f"  {status}: {count} ({percentage:.1f}%)")
        
        output.append(f"\nTotal Questions: {len(questions)}")
        
        return "\n".join(output)
