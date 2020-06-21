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
    is_complete = is_done_list(json['idList'])
    return Card(id=id, title=title, is_complete=is_complete)

def params_with_auth(params):
    return {"key": KEY, "token": TOKEN, **params}

def build_url(uri):
    return f"{BASE_URL}/boards/{BOARD_ID}{uri}"

def get_from_board(uri, params={}):
    return requests.get(build_url(uri), params=params_with_auth(params)).json()

def post_to_board(uri, params={}):
    return requests.post(build_url(uri), params=params_with_auth(params)).json()

def put_to_board(uri, params={}):
    return requests.put(build_url(uri), params=params_with_auth(params)).json()

def delete_from_board(uri, params={}):
    return requests.delete(build_url(uri), params=params_with_auth(params)).json()

def get_board():
    return get_from_board("")

def get_cards():
    response_json = get_from_board("/cards")
    return [json_to_card(item) for item in response_json]

def get_card(id):
    response_json = get_from_board(f"/cards/{id}")
    return json_to_card(response_json)

def get_lists():
    return get_from_board("/lists")

def add_card(name='ToDo List item'):
    params = {"name": name, "listId": TODO_LIST_ID}
    return post_to_board("/cards", params=params)

def mark_card_todo(id):
    params = {"listId": TODO_LIST_ID}
    return put_to_board(f"/cards/{id}", params=params)

def mark_card_complete(id):
    params = {"listId": DONE_LIST_ID}
    return put_to_board(f"/cards/{id}", params=params)

def delete_card(id):
    return delete_from_board(f"/cards/{id}")