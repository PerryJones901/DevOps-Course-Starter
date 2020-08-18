import api.api_helper as api
import env_vars as env
import requests
import os
from models.card import Card
from models.card_list import CardList
from typing import List

def build_board_url(uri) -> str:
    return f"{env.BASE_URL}/boards/{env.BOARD_ID}{uri}"

def build_card_url(uri) -> str:
    return f"{env.BASE_URL}/cards{uri}"

def get_board() -> dict:
    return api.get(build_board_url(""))

def get_cards() -> List[Card]:
    response_json = api.get(build_board_url("/cards"))
    return [Card.json_to_card(item) for item in response_json]

def get_card(id) -> Card:
    response_json = api.get(build_board_url(f"/cards/{id}"))
    return Card.json_to_card(response_json)

def get_lists() -> List[CardList]:
    response_json = api.get(build_board_url("/lists"))
    return [CardList.json_to_card_list(item) for item in response_json]

def get_list(name) -> CardList:
    lists = get_lists()
    return next(card_list for card_list in lists if card_list.name == name)

def add_card(title, list_id, due):
    params = {"name": title, "idList": list_id}
    if due != '':
        params = {**params, "due": due}
    return api.post(build_card_url(""), params=params)

def move_card_to_list(card_id, list_id):
    params = {"idList": list_id}
    return api.put(build_card_url(f"/{card_id}"), params=params)

def delete_card(id):
    return api.delete(build_card_url(f"/{id}"))

def add_board() -> str:
    url = f"{env.BASE_URL}/boards"
    params = {"name": "Selenium Test Board"}
    return api.post(url, params).json()['id']

def delete_board(id):
    url = f"{env.BASE_URL}/boards/{id}"
    return api.delete(url)