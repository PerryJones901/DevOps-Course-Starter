from card import Card
from card_list import CardList

class ViewModel:
    def __init__(self, items, lists):
        lists = [CardListViewModel(card_list) for card_list in lists]
        lists_by_id = {card_list_vm.id:card_list_vm for card_list_vm in lists}
        for card in items:
            lists_by_id[card.list_id].add_card(card)
        self._lists = lists

    @property
    def lists(self):
        return self._lists

class CardListViewModel:
    def __init__(self, card_list):
        self._id = card_list.id
        self._name = card_list.name
        self._cards = []

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def cards(self):
        return self._cards

    def add_card(self, card):
        self.cards.append(card)
