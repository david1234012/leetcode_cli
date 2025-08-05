# LeetCode CLI Tool

A command-line interface tool for interacting with the LeetCode platform to check login status and retrieve problem information.

## Features

- 🔐 Check LeetCode session status
- 📋 Fetch and display problem lists
- 🎯 Filter problems by status (Solved/Attempted/To Do)
- 📊 Display detailed problem information (difficulty, tags, acceptance rate, etc.)

## Requirements

- Python 3.x
- requests package

```bash
pip install requests
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

### Check Login Status

```bash
python leetcode_cli.py check_session
```

### Show All Problems

```bash
python leetcode_cli.py show_questions
```

### Filter Problems by Status

```bash
# Show solved problems
python leetcode_cli.py show_questions SOLVED

# Show attempted problems
python leetcode_cli.py show_questions ATTEMPTED

# Show problems to do
python leetcode_cli.py show_questions TO_DO
```

## Sample Output

```
ID             : 1
Title          : Two Sum
Difficulty     : Easy
Status         : SOLVED
Topics         : ['Array', 'Hash Table']
Acceptance Rate: 51.3
URL            : https://leetcode.com/problems/two-sum

-----------------------------------------------
Total Questions: 3012
```

## Command Parameters

### Actions

- `check_session` - Check session validity
- `show_questions` - Fetch and display problems

### Question Status

- `SOLVED` - Completed problems
- `ATTEMPTED` - Tried but not fully solved
- `TO_DO` - Not attempted yet

## Error Handling

- Automatic session file existence check
- Session validity verification
- Network request error handling
- Input parameter validation

## File Structure

```
leetcode_cli/
├── leetcode_cli.py          # Main program
├── leetcode_cli.session     # LeetCode session token (create manually)
└── README.md               # Project documentation
```

## Technical Implementation

- Uses LeetCode GraphQL API
- Supports HTTP cookies authentication
- JSON data parsing
- Command-line argument processing

## Important Notes

- Session tokens have expiration times and need to be updated periodically
- Do not publicly share your session token
- Ensure stable internet connection for API functionality

## License

This project is licensed under open source terms.

## Contributing

Issues and Pull Requests are welcome to improve this tool.