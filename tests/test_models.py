"""Test cases for models."""

import unittest
import sys
import os

# Add parent directory to path to import src modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from src.models import Question, UserInfo, QuestionFilter


class TestQuestion(unittest.TestCase):
    """Test cases for Question model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_api_data = {
            'questionFrontendId': '1',
            'title': 'Two Sum',
            'titleSlug': 'two-sum',
            'difficulty': 'Easy',
            'status': 'SOLVED',
            'topicTags': [
                {'name': 'Array', 'slug': 'array'},
                {'name': 'Hash Table', 'slug': 'hash-table'}
            ],
            'acRate': 51.3,
            'paidOnly': False,
            'frequency': 0.8
        }
    
    def test_from_api_response(self):
        """Test creating Question from API response."""
        question = Question.from_api_response(self.sample_api_data)
        
        self.assertEqual(question.id, '1')
        self.assertEqual(question.title, 'Two Sum')
        self.assertEqual(question.title_slug, 'two-sum')
        self.assertEqual(question.difficulty, 'Easy')
        self.assertEqual(question.status, 'SOLVED')
        self.assertEqual(question.topics, ['Array', 'Hash Table'])
        self.assertEqual(question.acceptance_rate, 51.3)
        self.assertFalse(question.is_paid_only)
        self.assertEqual(question.frequency, 0.8)
    
    def test_url_property(self):
        """Test URL property."""
        question = Question.from_api_response(self.sample_api_data)
        expected_url = "https://leetcode.com/problems/two-sum"
        
        self.assertEqual(question.url, expected_url)
    
    def test_to_dict(self):
        """Test converting to dictionary."""
        question = Question.from_api_response(self.sample_api_data)
        result = question.to_dict()
        
        expected_keys = [
            'id', 'title', 'difficulty', 'status', 'topics', 
            'acceptance_rate', 'is_paid_only', 'frequency', 'url'
        ]
        
        for key in expected_keys:
            self.assertIn(key, result)


class TestUserInfo(unittest.TestCase):
    """Test cases for UserInfo model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_api_data = {
            'username': 'testuser',
            'submitStats': {
                'acSubmissionNum': [
                    {'difficulty': 'Easy', 'count': 50},
                    {'difficulty': 'Medium', 'count': 30},
                    {'difficulty': 'Hard', 'count': 10}
                ]
            }
        }
    
    def test_from_api_response(self):
        """Test creating UserInfo from API response."""
        user_info = UserInfo.from_api_response(self.sample_api_data)
        
        self.assertEqual(user_info.username, 'testuser')
        self.assertEqual(user_info.solved_counts['Easy'], 50)
        self.assertEqual(user_info.solved_counts['Medium'], 30)
        self.assertEqual(user_info.solved_counts['Hard'], 10)


class TestQuestionFilter(unittest.TestCase):
    """Test cases for QuestionFilter model."""
    
    def test_default_values(self):
        """Test default filter values."""
        filter_criteria = QuestionFilter()
        
        self.assertIsNone(filter_criteria.status)
        self.assertIsNone(filter_criteria.difficulty)
        self.assertIsNone(filter_criteria.search_keyword)
        self.assertEqual(filter_criteria.limit, 50)
        self.assertEqual(filter_criteria.skip, 0)
        self.assertTrue(filter_criteria.include_paid)
    
    def test_custom_values(self):
        """Test custom filter values."""
        filter_criteria = QuestionFilter(
            status='SOLVED',
            difficulty='Easy',
            search_keyword='two sum',
            limit=10,
            skip=5,
            include_paid=False
        )
        
        self.assertEqual(filter_criteria.status, 'SOLVED')
        self.assertEqual(filter_criteria.difficulty, 'Easy')
        self.assertEqual(filter_criteria.search_keyword, 'two sum')
        self.assertEqual(filter_criteria.limit, 10)
        self.assertEqual(filter_criteria.skip, 5)
        self.assertFalse(filter_criteria.include_paid)


if __name__ == '__main__':
    unittest.main()
