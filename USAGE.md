# LeetCode CLI Tool - Usage Examples

This document provides detailed usage examples for the LeetCode CLI tool.

## Basic Usage

### Check Session Status
```bash
python leetcode_cli_new.py check_session
```

### Show All Questions
```bash
python leetcode_cli_new.py show_questions
```

### Show Questions with Filters
```bash
# Show only solved questions
python leetcode_cli_new.py show_questions --status SOLVED

# Show only easy questions
python leetcode_cli_new.py show_questions --difficulty Easy

# Show first 10 questions
python leetcode_cli_new.py show_questions --limit 10

# Exclude paid-only questions
python leetcode_cli_new.py show_questions --exclude-paid
```

## Advanced Usage

### Search Questions
```bash
# Search for specific questions
python leetcode_cli_new.py search --search "two sum"

# Search with limit
python leetcode_cli_new.py search --search "array" --limit 5
```

### Different Output Formats
```bash
# Summary format (compact table)
python leetcode_cli_new.py show_questions --format summary

# JSON format
python leetcode_cli_new.py show_questions --format json

# CSV format
python leetcode_cli_new.py show_questions --format csv
```

### Export to File
```bash
# Export to JSON file
python leetcode_cli_new.py export --format json --output questions.json

# Export solved questions to CSV
python leetcode_cli_new.py export --status SOLVED --format csv --output solved.csv
```

### Show Statistics
```bash
# Show statistics for all questions
python leetcode_cli_new.py show_questions --stats

# Show statistics for specific filter
python leetcode_cli_new.py show_questions --status SOLVED --stats
```

### Pagination
```bash
# Show first 20 questions
python leetcode_cli_new.py show_questions --limit 20

# Show next 20 questions (skip first 20)
python leetcode_cli_new.py show_questions --limit 20 --skip 20
```

## Combining Options

### Complex Filters
```bash
# Show easy solved questions in summary format
python leetcode_cli_new.py show_questions --status SOLVED --difficulty Easy --format summary

# Search for array problems and export to JSON
python leetcode_cli_new.py search --search "array" --format json --output array_problems.json

# Show medium questions excluding paid ones with statistics
python leetcode_cli_new.py show_questions --difficulty Medium --exclude-paid --stats
```

### Custom Session File
```bash
# Use custom session file
python leetcode_cli_new.py check_session --session-file /path/to/custom/session

# Show questions with custom session
python leetcode_cli_new.py show_questions --session-file /path/to/custom/session
```

## Troubleshooting

### Enable Verbose Logging
```bash
python leetcode_cli_new.py show_questions --verbose
```

### Check Version
```bash
python leetcode_cli_new.py --version
```

### Get Help
```bash
python leetcode_cli_new.py --help
python leetcode_cli_new.py show_questions --help
```

## Output Examples

### Table Format (Default)
```
============================================================
Question #1
ID             : 1
Title          : Two Sum
Difficulty     : Easy
Status         : SOLVED
Topics         : Array, Hash Table
Acceptance Rate: 51.3%
Paid Only      : No
URL            : https://leetcode.com/problems/two-sum

============================================================
Total Questions: 1
```

### Summary Format
```
ID     Title                                    Difficulty Status       Rate  
--------------------------------------------------------------------------------
1      Two Sum                                  Easy       SOLVED       51.3% 
2      Add Two Numbers                          Medium     Not Attempted 39.1% 
--------------------------------------------------------------------------------
Total Questions: 2
```

### JSON Format
```json
{
  "total_count": 1,
  "questions": [
    {
      "id": "1",
      "title": "Two Sum",
      "difficulty": "Easy",
      "status": "SOLVED",
      "topics": ["Array", "Hash Table"],
      "acceptance_rate": 51.3,
      "is_paid_only": false,
      "frequency": null,
      "url": "https://leetcode.com/problems/two-sum"
    }
  ]
}
```

## Performance Tips

1. **Use pagination** for large result sets to avoid long wait times
2. **Apply filters** to reduce the amount of data fetched
3. **Use summary format** for quick overview of many questions
4. **Enable verbose logging** only when debugging issues
