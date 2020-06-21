import api_helper as api
import env_vars as env
import requests
import os
from card import Card
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

def get_lists() -> dict:
    return api.get(build_board_url("/lists"))

def add_card(title, due) -> Card:
    params = {"name": title, "idList": env.TODO_LIST_ID}
    if due is not '':
        params = {**params, "due": due}
    return api.post(build_card_url(""), params=params)

def mark_card_todo(id) -> Card:
    params = {"idList": env.TODO_LIST_ID}
    return api.put(build_card_url(f"/{id}"), params=params)

def mark_card_complete(id) -> Card:
    params = {"idList": env.DONE_LIST_ID}
    return api.put(build_card_url(f"/{id}"), params=params)

def delete_card(id) -> Card:
    return api.delete(build_card_url(f"/{id}"))
