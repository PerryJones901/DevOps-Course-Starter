from card import Card
from card_list import CardList
from card_list_view_model import CardListViewModel
from typing import List

class ViewModel:
    def __init__(self, items: List[Card], lists: List[CardList]):
        lists = [CardListViewModel(card_list) for card_list in lists]
        lists_by_id = {card_list_vm.id:card_list_vm for card_list_vm in lists}
        for card in items:
            lists_by_id[card.list_id].add_card(card)
        self._lists = lists

    @property
    def lists(self) -> List[CardListViewModel]:
        return self._lists
