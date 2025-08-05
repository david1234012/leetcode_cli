"""Command-line interface for the LeetCode CLI tool."""

import argparse
import logging
import sys
from typing import Optional

from .config import Config, QuestionStatus, Actions
from .models import QuestionFilter
from .session import SessionManager
from .api import LeetCodeAPI, LeetCodeAPIError
from .formatters import OutputFormatter


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration.
    
    Args:
        verbose: Enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('leetcode_cli.log'),
            logging.StreamHandler() if verbose else logging.NullHandler()
        ]
    )


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI.
    
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description='LeetCode CLI Tool - A command-line interface for LeetCode platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  leetcode_cli check_session                     # Check session validity
  leetcode_cli show_questions                    # Show all questions
  leetcode_cli show_questions --status solved   # Show solved questions
  leetcode_cli show_questions --status SOLVED   # Show solved questions (case insensitive)
  leetcode_cli show_questions --difficulty easy # Show easy questions
  leetcode_cli show_questions --limit 10        # Show first 10 questions
  leetcode_cli search "two sum"                  # Search for questions
  leetcode_cli export --format json             # Export to JSON
        """
    )
    
    parser.add_argument(
        'action',
        choices=[Actions.CHECK_SESSION, Actions.SHOW_QUESTIONS, Actions.SEARCH, Actions.EXPORT],
        help='Action to perform'
    )
    
    # Question filtering options
    parser.add_argument(
        '--status',
        help='Filter questions by status (solved, attempted, todo - case insensitive)'
    )
    
    parser.add_argument(
        '--difficulty',
        help='Filter questions by difficulty (easy, medium, hard - case insensitive)'
    )
    
    parser.add_argument(
        '--search',
        help='Search questions by keyword'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=Config.DEFAULT_LIMIT,
        help=f'Maximum number of questions to fetch (default: {Config.DEFAULT_LIMIT})'
    )
    
    parser.add_argument(
        '--skip',
        type=int,
        default=0,
        help='Number of questions to skip (for pagination)'
    )
    
    parser.add_argument(
        '--include-paid',
        action='store_true',
        default=True,
        help='Include paid-only questions'
    )
    
    parser.add_argument(
        '--exclude-paid',
        action='store_true',
        help='Exclude paid-only questions'
    )
    
    # Output options
    parser.add_argument(
        '--format',
        choices=['table', 'summary', 'wide', 'json', 'csv'],
        default='table',
        help='Output format (default: table)'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show statistics for fetched questions'
    )
    
    # General options
    parser.add_argument(
        '--session-file',
        default=Config.SESSION_FILE,
        help=f'Path to session file (default: {Config.SESSION_FILE})'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='LeetCode CLI Tool 1.0.0'
    )
    
    return parser


class LeetCodeCLI:
    """Main CLI application class."""
    
    def __init__(self, args: argparse.Namespace):
        """Initialize CLI application.
        
        Args:
            args: Parsed command line arguments
        """
        self.args = args
        self.session_manager = SessionManager(args.session_file)
        self.api = LeetCodeAPI(self.session_manager)
        self.logger = logging.getLogger(__name__)
    
    def run(self) -> int:
        """Run the CLI application.
        
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Setup logging
            setup_logging(self.args.verbose)
            
            # Load session for most actions
            if self.args.action != Actions.CHECK_SESSION:
                if not self.session_manager.load_session():
                    return 1
            
            # Execute action
            if self.args.action == Actions.CHECK_SESSION:
                return self.check_session()
            elif self.args.action == Actions.SHOW_QUESTIONS:
                return self.show_questions()
            elif self.args.action == Actions.SEARCH:
                return self.search_questions()
            elif self.args.action == Actions.EXPORT:
                return self.export_questions()
            else:
                print(f"Unknown action: {self.args.action}", file=sys.stderr)
                return 1
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.", file=sys.stderr)
            return 1
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 1
    
    def check_session(self) -> int:
        """Check session validity.
        
        Returns:
            Exit code
        """
        try:
            if not self.session_manager.load_session():
                return 1
            
            user_info = self.api.check_session()
            output = OutputFormatter.format_user_info(user_info)
            
            self._write_output(output)
            return 0
            
        except LeetCodeAPIError as e:
            print(f"Session check failed: {e}", file=sys.stderr)
            return 1
    
    def show_questions(self) -> int:
        """Show questions based on filters.
        
        Returns:
            Exit code
        """
        try:
            filter_criteria = self._build_filter_criteria()
            questions = self.api.fetch_questions(filter_criteria)
            
            if not questions:
                print("No questions found matching the criteria.")
                return 0
            
            # Format output
            output = self._format_questions(questions)
            self._write_output(output)
            
            # Show statistics if requested
            if self.args.stats:
                stats = OutputFormatter.format_statistics(questions)
                print("\n" + stats)
            
            return 0
            
        except LeetCodeAPIError as e:
            print(f"Failed to fetch questions: {e}", file=sys.stderr)
            return 1
    
    def search_questions(self) -> int:
        """Search questions by keyword.
        
        Returns:
            Exit code
        """
        if not self.args.search:
            print("Search keyword is required for search action.", file=sys.stderr)
            return 1
        
        try:
            questions = self.api.search_questions(self.args.search, self.args.limit)
            
            if not questions:
                print(f"No questions found for keyword: '{self.args.search}'")
                return 0
            
            output = self._format_questions(questions)
            self._write_output(output)
            
            return 0
            
        except LeetCodeAPIError as e:
            print(f"Search failed: {e}", file=sys.stderr)
            return 1
    
    def export_questions(self) -> int:
        """Export questions to file.
        
        Returns:
            Exit code
        """
        try:
            filter_criteria = self._build_filter_criteria()
            questions = self.api.fetch_questions(filter_criteria)
            
            if not questions:
                print("No questions found to export.")
                return 0
            
            output = self._format_questions(questions)
            
            if self.args.output:
                with open(self.args.output, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"Questions exported to: {self.args.output}")
            else:
                self._write_output(output)
            
            return 0
            
        except LeetCodeAPIError as e:
            print(f"Export failed: {e}", file=sys.stderr)
            return 1
        except IOError as e:
            print(f"Failed to write output file: {e}", file=sys.stderr)
            return 1
    
    def _normalize_status(self, status: Optional[str]) -> Optional[str]:
        """Normalize status input to standard format.
        
        Args:
            status: Raw status input
            
        Returns:
            Normalized status or None if invalid
        """
        if not status:
            return None
        
        status_mapping = {
            'solved': QuestionStatus.SOLVED,
            'attempted': QuestionStatus.ATTEMPTED,
            'todo': QuestionStatus.TO_DO,
            'to_do': QuestionStatus.TO_DO,
            'to-do': QuestionStatus.TO_DO,
            # Also accept already uppercase versions
            'SOLVED': QuestionStatus.SOLVED,
            'ATTEMPTED': QuestionStatus.ATTEMPTED,
            'TO_DO': QuestionStatus.TO_DO
        }
        
        normalized = status_mapping.get(status.lower())
        if not normalized:
            valid_options = ['solved', 'attempted', 'todo']
            raise ValueError(f"Invalid status '{status}'. Valid options: {', '.join(valid_options)}")
        
        return normalized
    
    def _normalize_difficulty(self, difficulty: Optional[str]) -> Optional[str]:
        """Normalize difficulty input to standard format.
        
        Args:
            difficulty: Raw difficulty input
            
        Returns:
            Normalized difficulty or None if invalid
        """
        if not difficulty:
            return None
        
        difficulty_mapping = {
            'easy': 'Easy',
            'medium': 'Medium',
            'hard': 'Hard',
            # Also accept already capitalized versions
            'Easy': 'Easy',
            'Medium': 'Medium',
            'Hard': 'Hard'
        }
        
        normalized = difficulty_mapping.get(difficulty.lower())
        if not normalized:
            valid_options = ['easy', 'medium', 'hard']
            raise ValueError(f"Invalid difficulty '{difficulty}'. Valid options: {', '.join(valid_options)}")
        
        return normalized

    def _build_filter_criteria(self) -> QuestionFilter:
        """Build filter criteria from command line arguments.
        
        Returns:
            Filter criteria object
        """
        try:
            # Normalize and validate inputs
            normalized_status = self._normalize_status(self.args.status)
            normalized_difficulty = self._normalize_difficulty(self.args.difficulty)
            
            include_paid = not self.args.exclude_paid if hasattr(self.args, 'exclude_paid') else True
            
            return QuestionFilter(
                status=normalized_status,
                difficulty=normalized_difficulty,
                search_keyword=self.args.search,
                limit=self.args.limit,
                skip=self.args.skip,
                include_paid=include_paid
            )
        except ValueError as e:
            print(f"Invalid argument: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _format_questions(self, questions) -> str:
        """Format questions based on output format.
        
        Args:
            questions: List of questions to format
            
        Returns:
            Formatted output string
        """
        format_mapping = {
            'table': OutputFormatter.format_questions_table,
            'summary': OutputFormatter.format_questions_summary,
            'wide': OutputFormatter.format_questions_wide,
            'json': OutputFormatter.format_questions_json,
            'csv': OutputFormatter.format_questions_csv
        }
        
        formatter = format_mapping.get(self.args.format, OutputFormatter.format_questions_table)
        return formatter(questions)
    
    def _write_output(self, output: str) -> None:
        """Write output to stdout or file.
        
        Args:
            output: Output string to write
        """
        print(output)


def main() -> int:
    """Main entry point for the CLI application.
    
    Returns:
        Exit code
    """
    parser = create_parser()
    args = parser.parse_args()
    
    cli = LeetCodeCLI(args)
    return cli.run()


if __name__ == '__main__':
    sys.exit(main())
