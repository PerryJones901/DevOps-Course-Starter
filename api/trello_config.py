import os

class TrelloConfig:
    def __init__(self):
        self._BASE_URL = os.environ.get('TRELLO_BASE_URL')
        self._BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
        self._KEY = os.environ.get('TRELLO_API_KEY')
        self._TOKEN = os.environ.get('TRELLO_API_TOKEN')

    @property
    def BASE_URL(self) -> str:
        return self._BASE_URL

    @property
    def BOARD_ID(self) -> str:
        return self._BOARD_ID

    @property
    def KEY(self) -> str:
        return self._KEY

    @property
    def TOKEN(self) -> str:
        return self._TOKEN
