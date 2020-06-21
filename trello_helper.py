import requests
import os

BASE_URL = os.environ.get('TRELLO_BASE_URL')
BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
TODO_LIST_ID = os.environ.get('TRELLO_TODO_LIST_ID')
DONE_LIST_ID = os.environ.get('TRELLO_DONE_LIST_ID')
KEY = os.environ.get('TRELLO_API_KEY')
TOKEN = os.environ.get('TRELLO_API_TOKEN')

class Card:
    def __init__(self, id, idShort, title, is_complete):
        self.id = id
        self.idShort = idShort
        self.title = title
        self.is_complete = is_complete

def is_done_list(listId):
    return listId == DONE_LIST_ID

def json_to_card(json):
    id = json['id']
    idShort = json['idShort']
    title = json['name']
    is_complete = is_done_list(json['idList'])
    return Card(id, idShort, title, is_complete)

def params_with_auth(params):
    return {"key": KEY, "token": TOKEN, **params}

def build_board_url(uri):
    return f"{BASE_URL}/boards/{BOARD_ID}{uri}"

def build_card_url(uri):
    return f"{BASE_URL}/cards{uri}"

def get(url, params={}):
    return requests.get(url, params=params_with_auth(params)).json()

def post(url, params={}):
    return requests.post(url, params=params_with_auth(params)).json()

def put(url, params={}):
    print(url)
    return requests.put(url, params=params_with_auth(params)).json()

def delete(url, params={}):
    return requests.delete(url, params=params_with_auth(params)).json()

def get_board():
    return get(build_board_url(""))

def get_cards():
    response_json = get(build_board_url("/cards"))
    return [json_to_card(item) for item in response_json]

def get_card(id):
    response_json = get(build_board_url(f"/cards/{id}"))
    return json_to_card(response_json)

def get_lists():
    return get(build_board_url("/lists"))

def add_card(name='ToDo List item'):
    params = {"name": name, "idList": TODO_LIST_ID}
    return post(build_card_url(""), params=params)

def mark_card_todo(id):
    params = {"idList": TODO_LIST_ID}
    return put(build_card_url(f"/{id}"), params=params)

def mark_card_complete(id):
    params = {"idList": DONE_LIST_ID}
    return put(build_card_url(f"/{id}"), params=params)

def delete_card(id):
    return delete(build_card_url(f"/{id}"))
