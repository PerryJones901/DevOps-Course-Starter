from api.api_helper import ApiHelper
from api.trello_config import TrelloConfig
import requests
from models.card import Card
from models.card_list import CardList
from typing import List

class TrelloHelper:
    def __init__(self, trello_config: TrelloConfig):
        self.config = trello_config
        self.api = ApiHelper(trello_config)
        
    def build_board_url(self,uri) -> str:
        return f"{self.config.BASE_URL}/boards/{self.config.BOARD_ID}/{uri}"

    def build_card_url(self,uri) -> str:
        return f"{self.config.BASE_URL}/cards{uri}"

    def get_board(self) -> dict:
        return self.api.get(self.build_board_url(""))

    def get_cards(self) -> List[Card]:
        response_json = self.api.get(self.build_board_url("cards"))
        return [Card.json_to_card(item) for item in response_json]

    def get_card(self, id) -> Card:
        response_json = self.api.get(self.build_board_url(f"cards/{id}"))
        return Card.json_to_card(response_json)

    def get_lists(self) -> List[CardList]:
        response_json = self.api.get(self.build_board_url("lists"))
        return [CardList.json_to_card_list(item) for item in response_json]

    def get_list(self, name) -> CardList:
        lists = self.get_lists()
        return next(card_list for card_list in lists if card_list.name == name)

    def add_card(self, title, list_id, due):
        params = {"name": title, "idList": list_id}
        if due != '':
            params = {**params, "due": due}
        return self.api.post(self.build_card_url(""), params=params)

    def move_card_to_list(self, card_id, list_id):
        params = {"idList": list_id}
        return self.api.put(self.build_card_url(f"/{card_id}"), params=params)

    def delete_card(self, id):
        return self.api.delete(self.build_card_url(f"/{id}"))

    def add_board(self) -> str:
        url = f"{self.config.BASE_URL}/boards"
        params = {"name": "Selenium Test Board"}
        return self.api.post(url, params).json()['id']

    def delete_board(self, id):
        url = f"{self.config.BASE_URL}/boards/{id}"
        return self.api.delete(url)
