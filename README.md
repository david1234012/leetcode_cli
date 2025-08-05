# LeetCode CLI Tool

A modern, feature-rich command-line interface tool for interacting with the LeetCode platform to check login status and retrieve problem information.

## Features

- 🔐 Check LeetCode session status and user information
- 📋 Fetch and display problem lists with advanced filtering
- 🎯 Filter problems by status (Solved/Attempted/To Do), difficulty, and more
- 📊 Display detailed problem information (difficulty, tags, acceptance rate, etc.)
- 🔍 Search problems by keywords
- 📤 Export data in multiple formats (JSON, CSV, Table, Summary, Wide)
- 📈 Generate statistics for fetched problems
- 🚀 Modern, modular architecture with comprehensive error handling
- 📄 Pagination support for large datasets
- 🧪 Full test coverage
- 📱 Dynamic terminal width detection and adaptive formatting
- 🎨 Smart text wrapping and truncation for optimal display
- 🔤 Case-insensitive argument parsing for better user experience

## Requirements

- Python 3.7+
- requests package

```bash
pip install -r requirements.txt
```

## Installation

### Option 1: Direct Usage
```bash
git clone https://github.com/david1234012/leetcode_cli.git
cd leetcode_cli
pip install -r requirements.txt
```

### Option 2: Install as Package
```bash
pip install -e .
```

## Setup

### 1. Get LeetCode Session Token

1. Login to LeetCode in your browser
2. Open Developer Tools (F12)
3. Navigate to Application/Storage → Cookies → https://leetcode.com
4. Copy the value of `LEETCODE_SESSION`

### 2. Create Session File

Save the session token to `leetcode_cli.session` file:

```bash
echo "your_session_token_here" > leetcode_cli.session
```

## Usage

### Basic Commands

```bash
# Check session validity and show user info
python3 leetcode_cli.py check_session

# Show all problems (default: first 50)
python3 leetcode_cli.py show_questions

# Show problems with specific status (case insensitive)
python3 leetcode_cli.py show_questions --status solved    # or SOLVED
python3 leetcode_cli.py show_questions --status attempted # or ATTEMPTED  
python3 leetcode_cli.py show_questions --status todo      # or TO_DO

# Filter by difficulty (case insensitive)
python3 leetcode_cli.py show_questions --difficulty easy   # or Easy
python3 leetcode_cli.py show_questions --difficulty medium # or Medium
python3 leetcode_cli.py show_questions --difficulty hard   # or Hard
```

### Advanced Usage

```bash
# Search problems by keyword
python3 leetcode_cli.py search --search "two sum"

# Combine filters (case insensitive)
python3 leetcode_cli.py show_questions --status solved --difficulty easy --limit 10

# Different output formats
python3 leetcode_cli.py show_questions --format summary
python3 leetcode_cli.py show_questions --format wide    # Full title display
python3 leetcode_cli.py show_questions --format json
python3 leetcode_cli.py show_questions --format csv

# Export to file
python3 leetcode_cli.py export --format json --output problems.json
python3 leetcode_cli.py export --status solved --format csv --output solved.csv

# Show statistics
python3 leetcode_cli.py show_questions --stats

# Pagination
python3 leetcode_cli.py show_questions --limit 20 --skip 40

# Exclude paid problems
python3 leetcode_cli.py show_questions --exclude-paid

# Wide format for long titles (adaptive to terminal width)
python3 leetcode_cli.py show_questions --format wide --limit 10

# Mixed case examples (all work the same)
python3 leetcode_cli.py show_questions --status SOLVED --difficulty HARD
python3 leetcode_cli.py show_questions --status solved --difficulty hard
python3 leetcode_cli.py show_questions --status Solved --difficulty Hard

# Direct execution (if executable)
./leetcode_cli.py --help
./leetcode_cli.py check_session
```

### Complete Command Reference

```bash
python3 leetcode_cli.py --help
```

For detailed usage examples, see [USAGE.md](USAGE.md).

## Output Formats

### Table Format (Default)
Detailed view with all problem information in a readable table format.

### Summary Format
Compact table view showing essential information in a condensed format. Automatically adapts to terminal width for optimal display.

### Wide Format
Full-width display that shows complete problem titles without truncation, ideal for viewing problems with long titles.

### JSON Format
Machine-readable JSON output suitable for integration with other tools.

### CSV Format
Comma-separated values format for spreadsheet applications.

## Project Structure

```
leetcode_cli/
├── src/                     # Source code modules
│   ├── __init__.py         # Package initialization
│   ├── config.py           # Configuration constants
│   ├── models.py           # Data models
│   ├── session.py          # Session management
│   ├── api.py              # LeetCode API client
│   ├── formatters.py       # Output formatters
│   ├── utils.py            # Terminal utilities and helpers
│   └── cli.py              # Command-line interface
├── tests/                   # Test files
│   ├── test_session.py     # Session management tests
│   └── test_models.py      # Data model tests
├── leetcode_cli.py         # Main entry point
├── leetcode_cli.session    # Session token file (create manually)
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup configuration
├── USAGE.md               # Detailed usage examples
└── README.md              # Project documentation
```

## Architecture

The tool is built with a modular architecture:

- **Models**: Data structures for questions, user info, and filters
- **Session Management**: Secure handling of LeetCode session tokens
- **API Client**: GraphQL client for LeetCode API with comprehensive error handling
- **Formatters**: Multiple output formats for different use cases
- **Utils**: Terminal utilities for dynamic display adaptation
- **CLI**: Modern argument parsing with comprehensive options

## Technical Implementation

- **LeetCode GraphQL API**: Direct integration with official API
- **HTTP Cookies Authentication**: Secure session-based authentication
- **Dynamic Terminal Detection**: Automatic terminal width detection and adaptive formatting
- **Smart Text Processing**: Intelligent text wrapping and truncation algorithms
- **Comprehensive Error Handling**: Detailed error messages and logging
- **Type Hints**: Full type annotation for better code quality
- **Modular Design**: Easy to extend and maintain
- **Test Coverage**: Unit tests for critical components

## Error Handling

The tool provides comprehensive error handling for:
- Invalid session tokens
- Network connectivity issues
- API rate limiting
- Invalid command arguments
- File I/O errors

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Or run individual test files:

```bash
python tests/test_session.py
python tests/test_models.py
```

## Important Notes

- Session tokens have expiration times and need to be updated periodically
- Do not publicly share your session token
- Ensure stable internet connection for API functionality
- Use pagination for large datasets to avoid timeouts
- The tool respects LeetCode's API rate limits
- Summary format automatically adapts to your terminal width for optimal display
- Use `--format wide` for viewing problems with long titles without truncation
- Terminal width is automatically detected; resize your terminal for different layouts

## Migration from Legacy Version

The current version (`leetcode_cli.py`) provides all functionality of the original script with significant enhancements:

1. **Same Command Interface**: Continue using `python3 leetcode_cli.py` as before
2. **Enhanced Options**: Additional filtering, formatting, and export options
3. **Better Error Handling**: More informative error messages
4. **Modular Code**: Easier to extend and maintain

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Changelog

### Version 1.2.0 (Latest)
- Added case-insensitive argument parsing for --status and --difficulty
- Unified input standards: accept both lowercase and uppercase inputs
- Improved user experience with flexible argument formats
- Enhanced error messages for invalid arguments
- Updated documentation with case-insensitive examples

### Version 1.1.0
- Added dynamic terminal width detection and adaptive formatting
- Implemented smart text wrapping and truncation algorithms
- Added new 'wide' format for full title display
- Enhanced summary format with terminal size adaptation
- Added terminal utilities module (utils.py)
- Improved user experience for different terminal sizes
- Fixed title truncation issues in summary format

### Version 1.0.0
- Complete rewrite with modular architecture
- Advanced filtering and search capabilities
- Multiple output formats (JSON, CSV, Table, Summary)
- Comprehensive error handling and logging
- Pagination support
- Statistics generation
- Full test coverage
- Type hints and documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.