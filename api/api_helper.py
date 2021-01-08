from api.trello_config import TrelloConfig
import os
import requests

class ApiHelper:
    def __init__(self, trello_config: TrelloConfig):
        self._KEY = trello_config.KEY
        self._TOKEN = trello_config.TOKEN

    def get(self, url, params={}) -> dict:
        return requests.get(url, params=self.__params_with_auth(params)).json()

    def post(self, url, params={}) -> dict:
        return requests.post(url, params=self.__params_with_auth(params))

    def put(self, url, params={}) -> dict:
        return requests.put(url, params=self.__params_with_auth(params))

    def delete(self, url, params={}) -> dict:
        return requests.delete(url, params=self.__params_with_auth(params))

    def __params_with_auth(self, params) -> dict:
        return {"key": self._KEY, "token": self._TOKEN, **params}
