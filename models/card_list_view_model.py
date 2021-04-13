from typing import List

from .card_view_model import CardViewModel

class CardListViewModel:
    def __init__(self, card_list):
        self._id = card_list.id
        self._name = card_list.name
        self._cards = []

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def cards(self) -> List[CardViewModel]:
        return self._cards

    def add_cards(self, cards: List[CardViewModel]):
        self._cards = self._cards + cards

    def add_card(self, card: CardViewModel):
        self.cards.append(card)
