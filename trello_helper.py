import requests
import os

BASE_URL = os.environ.get('TRELLO_BASE_URL')
BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
KEY = os.environ.get('TRELLO_API_KEY')
TOKEN = os.environ.get('TRELLO_API_TOKEN')

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
    return get_from_board("/cards")

def get_card(id):
    return get_from_board("/cards/{id}")

def get_lists():
    return get_from_board("/lists")

def add_card_to_leftmost_list(name='ToDo List item', desc='This needs completing!'):
    leftmost_list_id = int(get_lists()[0]['id'])
    extra_params = {"name": name, "desc": desc, "listId": leftmost_list_id}
    return post_to_board("/cards", extra_params=extra_params)