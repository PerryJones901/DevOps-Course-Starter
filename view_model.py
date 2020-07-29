from card import Card
from card_view_model import CardViewModel
from card_list import CardList
from card_list_view_model import CardListViewModel
from datetime import date
from typing import List

from pprint import pprint

DONE_LIST_NAME = 'Done'
DONE_LIST_CARD_LIMIT = 5

class ViewModel:
    def __init__(self, items: List[Card], lists: List[CardList], show_all_done_items: bool = True, today: date = None):
        lists = [CardListViewModel(card_list) for card_list in lists]
        lists_by_id = {card_list_vm.id:card_list_vm for card_list_vm in lists}
        for card in items:
            lists_by_id[card.list_id].add_card(CardViewModel(card))
        self._lists = lists
        self._show_all_done_items = show_all_done_items
        self._today = today

    @property
    def lists(self) -> List[CardListViewModel]:
        return self._lists

    @property
    def show_all_done_items(self) -> bool:
        return self._show_all_done_items

    @property
    def today(self) -> date:
        return self._today

    @property
    def card_lists_excl_done(self) -> List[CardListViewModel]:
        return self._lists_that_are_not_done_list(True)

    @property
    def done_list(self) -> CardListViewModel:
        return self._lists_that_are_not_done_list(False)[0]

    @property
    def done_list_items_view(self) -> List[CardViewModel]:
        if(self.show_all_done_items or len(self.done_list.cards) < DONE_LIST_CARD_LIMIT):
            return self.done_list.cards
        return self.recent_done_items

    def _lists_that_are_not_done_list(self, get_non_done_lists: bool):
        '''
        If 'get_non_done_lists' is true:
            Returns a list of all the CardListViewModels, EXCLUDING the Done List,
        Else:
            Otherwise return Done list wrapped in a list (so it's a singleton list)
        '''
        return [card_list for card_list in self.lists if (card_list.name != DONE_LIST_NAME) == get_non_done_lists]

    @property
    def older_done_items(self) -> List[CardViewModel]:
        return self._cards_in_done_modified_before_today(True)

    @property
    def recent_done_items(self) -> List[CardViewModel]:
        return self._cards_in_done_modified_before_today(False)

    def _cards_in_done_modified_before_today(self, before_today: bool) -> List[CardViewModel]:
        done_list = self.done_list
        return [item for item in done_list.cards if (item.last_modified < self.today) == before_today]
