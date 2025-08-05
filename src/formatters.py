"""Output formatters for the LeetCode CLI tool."""

import json
import csv
from typing import List, Dict, Any
from io import StringIO

from .models import Question, UserInfo


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
        """Format questions as a summary table.
        
        Args:
            questions: List of questions to format
            
        Returns:
            Formatted summary string
        """
        if not questions:
            return "No questions found."
        
        # Header
        output = []
        output.append(f"{'ID':<6} {'Title':<40} {'Difficulty':<10} {'Status':<12} {'Rate':<6}")
        output.append("-" * 80)
        
        # Questions
        for q in questions:
            title = q.title[:37] + "..." if len(q.title) > 40 else q.title
            status = (q.status or "Not Attempted")[:11]
            rate = f"{q.acceptance_rate:.1f}%"
            
            output.append(f"{q.id:<6} {title:<40} {q.difficulty:<10} {status:<12} {rate:<6}")
        
        output.append("-" * 80)
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
