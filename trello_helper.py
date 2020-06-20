import requests
import os

BASE_URL = os.environ.get('TRELLO_BASE_URL')
BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
TODO_LIST_ID = os.environ.get('TRELLO_TODO_LIST_ID')
DONE_LIST_ID = os.environ.get('TRELLO_DONE_LIST_ID')
KEY = os.environ.get('TRELLO_API_KEY')
TOKEN = os.environ.get('TRELLO_API_TOKEN')

class Card:
    def __init__(self, id, title, is_complete):
        self.id = id
        self.title = title
        self.is_complete = is_complete

def is_done_list(listId):
    return listId == DONE_LIST_ID

def json_to_card(json):
    id = json['id']
    title = json['name']
    is_complete = is_done_list(json['listId'])
    return Card(id=id, title=title, is_complete=is_complete)

def key_and_token():
    return {"key": KEY, "token": TOKEN}

def get_from_board(uri, extra_params={}):
    url = f"{BASE_URL}/boards/{BOARD_ID}{uri}"
    params = key_and_token().update(extra_params)
    return requests.get(url, params=params).json()

def post_to_board(uri, extra_params={}):
    url = f"{BASE_URL}/boards/{BOARD_ID}{uri}"
    params = key_and_token().update(extra_params)
    return requests.post(url, params=params).json()

def get_board():
    return get_from_board("")

def get_cards():
    response_json = get_from_board("/cards")
    return [json_to_card(item) for item in response_json]

def get_card(id):
    response_json = get_from_board("/cards/{id}")
    return json_to_card(response_json)

def get_lists():
    return get_from_board("/lists")

def add_card_to_leftmost_list(name='ToDo List item', desc='This needs completing!'):
    leftmost_list_id = int(get_lists()[0]['id'])
    extra_params = {"name": name, "desc": desc, "listId": leftmost_list_id}
    return post_to_board("/cards", extra_params=extra_params)