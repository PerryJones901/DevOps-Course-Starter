import pytest
from card import Card
from card_list import CardList
from view_model import ViewModel

LISTS = [
    CardList(101, "Todo"),
    CardList(102, "Doing"),
    CardList(103, "Done")
]

@pytest.fixture
def cards():
    card1 = Card(1, 1, "Task in Todo List", None, LISTS[0].id)
    card2 = Card(2, 2, "Task in Doing List", None, LISTS[1].id)
    card3 = Card(3, 3, "Task in Done List", None, LISTS[2].id)
    card4 = Card(4, 4, "Another Task in Todo List", None, LISTS[0].id)
    return [card1, card2, card3, card4]

def test_view_model_keeps_list_order(cards):
    # Act
    view_model = ViewModel(cards, LISTS)

    # Assert
    assert view_model.lists[0].id == 101
    assert view_model.lists[1].id == 102
    assert view_model.lists[2].id == 103

def test_view_model_assigns_cards_to_correct_lists(cards):
    # Act
    view_model = ViewModel(cards, LISTS)

    # Assert
    assert view_model.lists[0].cards[0].id == 1
    assert view_model.lists[0].cards[1].id == 4
    assert view_model.lists[1].cards[0].id == 2
    assert view_model.lists[2].cards[0].id == 3
