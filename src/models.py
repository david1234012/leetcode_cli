"""Data models for the LeetCode CLI tool."""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class Question:
    """Represents a LeetCode question."""
    id: str
    title: str
    title_slug: str
    difficulty: str
    status: Optional[str]
    topics: List[str]
    acceptance_rate: float
    is_paid_only: bool
    frequency: Optional[float]
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'Question':
        """Create Question instance from API response data."""
        return cls(
            id=data['questionFrontendId'],
            title=data['title'],
            title_slug=data['titleSlug'],
            difficulty=data['difficulty'],
            status=data.get('status'),
            topics=[tag['name'] for tag in data.get('topicTags', [])],
            acceptance_rate=data.get('acRate', 0.0),
            is_paid_only=data.get('paidOnly', False),
            frequency=data.get('frequency')
        )
    
    @property
    def url(self) -> str:
        """Get the LeetCode URL for this question."""
        return f"https://leetcode.com/problems/{self.title_slug}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        return {
            'id': self.id,
            'title': self.title,
            'difficulty': self.difficulty,
            'status': self.status,
            'topics': self.topics,
            'acceptance_rate': self.acceptance_rate,
            'is_paid_only': self.is_paid_only,
            'frequency': self.frequency,
            'url': self.url
        }


@dataclass
class UserInfo:
    """Represents user information from LeetCode."""
    username: str
    solved_counts: Dict[str, int]
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'UserInfo':
        """Create UserInfo instance from API response data."""
        username = data['username']
        solved_counts = {}
        
        if 'submitStats' in data and 'acSubmissionNum' in data['submitStats']:
            for submission in data['submitStats']['acSubmissionNum']:
                difficulty = submission['difficulty']
                count = submission['count']
                solved_counts[difficulty] = count
        
        return cls(username=username, solved_counts=solved_counts)


@dataclass
class QuestionFilter:
    """Filter criteria for questions."""
    status: Optional[str] = None
    difficulty: Optional[str] = None
    search_keyword: Optional[str] = None
    limit: int = 50
    skip: int = 0
    include_paid: bool = True
