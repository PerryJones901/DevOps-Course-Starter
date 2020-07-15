import api_helper as api
import env_vars as env
import requests
import os
from card import Card
from card_list import CardList
from typing import List

def build_board_url(uri) -> str:
    return f"{env.BASE_URL}/boards/{env.BOARD_ID}{uri}"

def build_card_url(uri) -> str:
    return f"{env.BASE_URL}/cards{uri}"

def get_board() -> dict:
    return api.get(build_board_url(""))

def get_cards() -> List[Card]:
    done_list_id = get_list('Done').id
    response_json = api.get(build_board_url("/cards"))
    return [Card.json_to_card(item, is_complete=item['idList'] == done_list_id) for item in response_json]

def get_card(id) -> Card:
    done_list_id = get_list('Done').id
    response_json = api.get(build_board_url(f"/cards/{id}"))
    if(response_json['idList'] == done_list_id):
        is_complete = True
    else:
        is_complete = False
    return Card.json_to_card(response_json, is_complete)

def get_lists() -> List[CardList]:
    response_json = api.get(build_board_url("/lists"))
    return [CardList.json_to_card_list(item) for item in response_json]

def get_list(name) -> CardList:
    lists = get_lists()
    return next(card_list for card_list in lists if card_list.name == name)

def add_card(title, due) -> Card:
    todo_list_id = get_list('To Do').id
    params = {"name": title, "idList": todo_list_id}
    if due != '':
        params = {**params, "due": due}
    return api.post(build_card_url(""), params=params)

def mark_card_todo(id) -> Card:
    todo_list_id = get_list('To Do').id
    params = {"idList": todo_list_id}
    return api.put(build_card_url(f"/{id}"), params=params)

def mark_card_complete(id) -> Card:
    done_list_id = get_list('Done').id
    params = {"idList": done_list_id}
    return api.put(build_card_url(f"/{id}"), params=params)

def delete_card(id) -> Card:
    return api.delete(build_card_url(f"/{id}"))
