"""Configuration constants for the LeetCode CLI tool."""

class Config:
    """Configuration constants."""
    LEETCODE_API_URL = "https://leetcode.com/graphql"
    SESSION_FILE = "./leetcode_cli.session"
    DEFAULT_LIMIT = 50
    CACHE_DURATION = 3600
    
    HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "LeetCode-CLI/1.0.0"
    }


class QuestionStatus:
    """Question status constants."""
    SOLVED = "SOLVED"
    ATTEMPTED = "ATTEMPTED"
    TO_DO = "TO_DO"
    
    @classmethod
    def all(cls):
        """Get all supported status values."""
        return {cls.SOLVED, cls.ATTEMPTED, cls.TO_DO}


class Actions:
    """CLI action constants."""
    CHECK_SESSION = "check_session"
    SHOW_QUESTIONS = "show_questions"
    SEARCH = "search"
    EXPORT = "export"


class GraphQLQueries:
    """GraphQL queries for LeetCode API."""
    
    USER_INFO = """
    {
        user {
            username
            submitStats {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
    }
    """
    
    PROBLEM_LIST = """
    query problemsetQuestionListV2(
        $filters: QuestionFilterInput,
        $limit: Int,
        $skip: Int,
        $sortBy: QuestionSortByInput,
        $searchKeyword: String
    ) {
        problemsetQuestionListV2(
            filters: $filters
            limit: $limit
            skip: $skip
            sortBy: $sortBy
            searchKeyword: $searchKeyword
        ) {
            questions {
                questionFrontendId
                title
                titleSlug
                difficulty
                status
                topicTags {
                    name
                    slug
                }
                acRate
                paidOnly
                frequency
            }
            totalLength
            hasMore
        }
    }
    """
