"""LeetCode API client."""

import json
import logging
from typing import List, Optional, Dict, Any
import requests

from .config import Config, QuestionStatus, GraphQLQueries
from .models import Question, UserInfo, QuestionFilter
from .session import SessionManager


class LeetCodeAPIError(Exception):
    """Custom exception for LeetCode API errors."""
    pass


class LeetCodeAPI:
    """LeetCode API client."""
    
    def __init__(self, session_manager: SessionManager):
        """Initialize API client.
        
        Args:
            session_manager: Session manager instance
        """
        self.session_manager = session_manager
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GraphQL request to LeetCode API.
        
        Args:
            query: GraphQL query string
            variables: Query variables
            
        Returns:
            API response data
            
        Raises:
            LeetCodeAPIError: If request fails
        """
        if not self.session_manager.is_session_loaded():
            raise LeetCodeAPIError("Session not loaded. Please load session first.")
        
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        try:
            response = requests.post(
                Config.LEETCODE_API_URL,
                headers=Config.HEADERS,
                cookies=self.session_manager.get_session_cookies(),
                json=payload,
                timeout=30
            )
            
            data = response.json()
            
            if response.status_code != 200:
                error_msg = f"API request failed with status code: {response.status_code}"
                if 'errors' in data:
                    errors = [error.get('message', 'Unknown error') for error in data['errors']]
                    error_msg += f". Errors: {', '.join(errors)}"
                raise LeetCodeAPIError(error_msg)
            
            if 'errors' in data:
                errors = [error.get('message', 'Unknown error') for error in data['errors']]
                raise LeetCodeAPIError(f"GraphQL errors: {', '.join(errors)}")
            
            return data
            
        except requests.RequestException as e:
            self.logger.error(f"Network error: {e}")
            raise LeetCodeAPIError(f"Network error: {e}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            raise LeetCodeAPIError(f"Failed to parse JSON response: {e}")
    
    def check_session(self) -> UserInfo:
        """Check if session is valid and get user info.
        
        Returns:
            User information
            
        Raises:
            LeetCodeAPIError: If session is invalid or request fails
        """
        try:
            data = self._make_request(GraphQLQueries.USER_INFO)
            
            user_data = data.get('data', {}).get('user')
            if not user_data:
                raise LeetCodeAPIError("Session is invalid or expired.")
            
            return UserInfo.from_api_response(user_data)
            
        except LeetCodeAPIError:
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error checking session: {e}")
            raise LeetCodeAPIError(f"Unexpected error checking session: {e}")
    
    def fetch_questions(self, filter_criteria: QuestionFilter) -> List[Question]:
        """Fetch questions based on filter criteria.
        
        Args:
            filter_criteria: Filter criteria for questions
            
        Returns:
            List of questions
            
        Raises:
            LeetCodeAPIError: If request fails
        """
        try:
            # Validate status filter
            if filter_criteria.status and filter_criteria.status not in QuestionStatus.all():
                raise LeetCodeAPIError(
                    f"Invalid question status '{filter_criteria.status}'. "
                    f"Supported values: {QuestionStatus.all()}"
                )
            
            # Build variables for GraphQL query
            variables = {
                "limit": filter_criteria.limit,
                "skip": filter_criteria.skip,
                "sortBy": {
                    "sortField": "CUSTOM",
                    "sortOrder": "ASCENDING"
                }
            }
            
            # Add search keyword if provided
            if filter_criteria.search_keyword:
                variables["searchKeyword"] = filter_criteria.search_keyword
            
            # Build filters
            filters = {"filterCombineType": "ALL"}
            
            # Add status filter
            if filter_criteria.status:
                filters["statusFilter"] = {
                    "questionStatuses": [filter_criteria.status],
                    "operator": "IS"
                }
            
            # Add difficulty filter
            if filter_criteria.difficulty:
                filters["difficultyFilter"] = {
                    "difficulties": [filter_criteria.difficulty.upper()],
                    "operator": "IS"
                }
            
            # Add paid filter
            if not filter_criteria.include_paid:
                filters["paidOnlyFilter"] = {
                    "paidOnly": False,
                    "operator": "IS"
                }
            
            variables["filters"] = filters
            
            # Make API request
            data = self._make_request(GraphQLQueries.PROBLEM_LIST, variables)
            
            # Parse response
            problem_data = data.get('data', {}).get('problemsetQuestionListV2', {})
            questions_data = problem_data.get('questions', [])
            
            # Convert to Question objects
            questions = [Question.from_api_response(q) for q in questions_data]
            
            self.logger.info(f"Fetched {len(questions)} questions")
            return questions
            
        except LeetCodeAPIError:
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error fetching questions: {e}")
            raise LeetCodeAPIError(f"Unexpected error fetching questions: {e}")
    
    def search_questions(self, keyword: str, limit: int = 20) -> List[Question]:
        """Search questions by keyword.
        
        Args:
            keyword: Search keyword
            limit: Maximum number of results
            
        Returns:
            List of matching questions
        """
        filter_criteria = QuestionFilter(
            search_keyword=keyword,
            limit=limit
        )
        return self.fetch_questions(filter_criteria)
