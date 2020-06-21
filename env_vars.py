import os

# URLs and IDs
BASE_URL = os.environ.get('TRELLO_BASE_URL')
BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
TODO_LIST_ID = os.environ.get('TRELLO_TODO_LIST_ID')
DONE_LIST_ID = os.environ.get('TRELLO_DONE_LIST_ID')

# Auth
KEY = os.environ.get('TRELLO_API_KEY')
TOKEN = os.environ.get('TRELLO_API_TOKEN')
