from abc import ABC, abstractmethod
from typing import List
from models.card import Card
from models.card_list import CardList

class ITaskDataManager(ABC):
    @abstractmethod
    def get_cards(self) -> List[Card]:
        pass
    
    @abstractmethod
    def get_card(self, id) -> Card:
        pass

    @abstractmethod
    def add_card(self, title, list_id, due) -> None:
        pass

    @abstractmethod
    def delete_card(self, id) -> None:
        pass

    @abstractmethod
    def get_lists(self) -> List[CardList]:
        pass

    @abstractmethod
    def get_list(self, name) -> CardList:
        pass

    @abstractmethod
    def move_card_to_list(self, card_id, list_id) -> None:
        pass
