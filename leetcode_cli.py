import requests
import sys

ACTION_CHECK_SESSION = "check_session"
ACTION_SHOW_QUESTIONS = "show_questions"

QUESTION_STATUS_SOLVED = "SOLVED"
QUESTION_STATUS_ATTEMPTED = "ATTEMPTED"
QUESTION_STATUS_TO_DO = "TO_DO"

FILE_SESSION = "./leetcode_cli.session"

url = "https://leetcode.com/graphql"

headers = {
	"Content-Type": "application/json",
}

cookies: dict = {}


def set_leetcode_session(session_token):
	cookies["LEETCODE_SESSION"] = session_token


def fetch_resolved_problems(question_status=None):
	# Supported enum values for question_status
	supported_statuses = {QUESTION_STATUS_SOLVED, QUESTION_STATUS_ATTEMPTED, QUESTION_STATUS_TO_DO}
	if question_status and question_status not in supported_statuses:
		print(f"Invalid question_status '{question_status}'. Supported values: {supported_statuses}")
		return False

	query = '''
	query problemsetQuestionListV2($filters: QuestionFilterInput, $limit: Int, $searchKeyword: String, $skip: Int, $sortBy: QuestionSortByInput, $categorySlug: String) {
	  problemsetQuestionListV2(
		filters: $filters
		limit: $limit
		searchKeyword: $searchKeyword
		skip: $skip
		sortBy: $sortBy
		categorySlug: $categorySlug
	  ) {
		questions {
		  id
		  titleSlug
		  title
		  translatedTitle
		  questionFrontendId
		  paidOnly
		  difficulty
		  topicTags {
			name
			slug
			nameTranslated
		  }
		  status
		  isInMyFavorites
		  frequency
		  acRate
		  contestPoint
		}
		totalLength
		finishedLength
		hasMore
	  }
	}
	'''
 
	if question_status:
		questionStatuses = [question_status]
	else:
		questionStatuses = []

	variables = {
		"filters": {
			"filterCombineType": "ALL",
			"statusFilter": {
				"questionStatuses": questionStatuses,
				"operator": "IS"
			},
		},
		"sortBy": {
			"sortField": "CUSTOM",
			"sortOrder": "ASCENDING"
		},
	}

	response = requests.post(
		url,
		headers=headers,
		cookies=cookies,
		json={"query": query, "variables": variables}
	)
	try:
		data = response.json()
	except Exception as e:
		print(f"Failed to parse JSON response: {e}")
		print(f"Response content: {response.text}")
		return False

	if response.status_code == 200:
		questions = data['data']['problemsetQuestionListV2']['questions']
  
		for q in questions:
			tag_names = [tag['name'] for tag in q['topicTags']] if q['topicTags'] else []
			print(f"ID             : {q['questionFrontendId']}")
			print(f"Title          : {q['title']}")
			print(f"Difficulty     : {q['difficulty']}")
			print(f"Status         : {q['status']}")
			print(f"Topics         : {tag_names}")
			print(f"Acceptance Rate: {q['acRate']}")
			print(f"URL            : https://leetcode.com/problems/{q['titleSlug']}\n")

		print("-----------------------------------------------")
		print(f"Total Questions: {len(questions)}")
		return True
	else:
		if 'errors' in data:
			for error in data['errors']:
				print(f"Error: {error.get('message')}")
	
		print(f"Request failed with status code: {response.status_code}")
		return False


def check_leetcode_session():
	query = """
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
	response = requests.post(url, headers=headers, cookies=cookies, json={"query": query})
	data = response.json()

	if response.status_code == 200:
		user_data = data.get('data', {}).get('user', None)
		if user_data:
			print(f"User: {user_data['username']}")
			return True
		else:
			print("Session is invalid.")
			return False
	else:
		if 'errors' in data:
			for error in data['errors']:
				print(f"Error: {error.get('message')}")
    
		print(f"Request failed with status code: {response.status_code}")
		return False

def help():
	print("Available actions:")
	print(f"  {ACTION_CHECK_SESSION} - Check session validity.")
	print(f"  {ACTION_SHOW_QUESTIONS} - Fetch and display questions.")
 
def set_session_from_file():
	try:
		with open(FILE_SESSION, "r") as f:
			token = f.read().strip()
			if token:
				set_leetcode_session(token)
				return True
			else:
				print("Session file is empty.")
				return False
	except FileNotFoundError:
		print(f"Session file '{FILE_SESSION}' not found.")
		return False
	except Exception as e:
		print(f"Error reading session file: {e}")
		return False

def main():
	if len(sys.argv) < 2:
		help()
		sys.exit(1)
  
	action = sys.argv[1]
 
	if action in (ACTION_CHECK_SESSION, ACTION_SHOW_QUESTIONS):
		if not set_session_from_file():
			sys.exit(1)
		if not check_leetcode_session():
			sys.exit(1)
		if action == ACTION_SHOW_QUESTIONS:
			question_status = sys.argv[2] if len(sys.argv) > 2 else None
			if not fetch_resolved_problems(question_status):
				sys.exit(1)
	else:
		help()
		sys.exit(1)

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(f"Unexpected error: {e}")
		sys.exit(1)