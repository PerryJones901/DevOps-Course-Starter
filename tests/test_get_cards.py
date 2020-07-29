from datetime import datetime, timedelta

import pytest

from models.card import Card
from models.card_list import CardList
from models.view_model import ViewModel

LISTS = [
    CardList(101, "Todo"),
    CardList(102, "Doing"),
    CardList(103, "Done")
]

TODAY_DATE = datetime(2020,1,1).date()
YESTERDAY_DATE = TODAY_DATE - timedelta(days=1)

@pytest.fixture
def cards():
    card1 = Card(1, 1, "Task in Todo List", LISTS[0].id, None, None)
    card2 = Card(2, 2, "Task in Doing List", LISTS[1].id, None, None)
    card3 = Card(3, 3, "Task in Done List", LISTS[2].id, None, None)
    card4 = Card(4, 4, "Another Task in Todo List", LISTS[0].id, None, None)
    return [card1, card2, card3, card4]

@pytest.fixture
def cards_with_last_modified_dates():
    card1 = Card(1, 1, "Card 1 Todo Yesterday", LISTS[0].id, None, YESTERDAY_DATE)
    card2 = Card(2, 2, "Card 2 Todo Today", LISTS[0].id, None, TODAY_DATE)
    card3 = Card(3, 3, "Card 3 Done Yesterday", LISTS[2].id, None, YESTERDAY_DATE)
    card4 = Card(4, 4, "Card 4 Done Today", LISTS[2].id, None,  TODAY_DATE)
    return [card1, card2, card3, card4]

@pytest.fixture
def four_completed_tasks():
    card1 = Card(1, 1, "Card 1 Done", LISTS[2].id, None, YESTERDAY_DATE)
    card2 = Card(2, 2, "Card 2 Done", LISTS[2].id, None, YESTERDAY_DATE)
    card3 = Card(3, 3, "Card 3 Done", LISTS[2].id, None, YESTERDAY_DATE)
    card4 = Card(4, 4, "Card 4 Done", LISTS[2].id, None, YESTERDAY_DATE)
    return [card1, card2, card3, card4]

@pytest.fixture
def five_completed_tasks():
    card1 = Card(1, 1, "Card 1 Done", LISTS[2].id, None, YESTERDAY_DATE)
    card2 = Card(2, 2, "Card 2 Done", LISTS[2].id, None, YESTERDAY_DATE)
    card3 = Card(3, 3, "Card 3 Done", LISTS[2].id, None, YESTERDAY_DATE)
    card4 = Card(4, 4, "Card 4 Done", LISTS[2].id, None, YESTERDAY_DATE)
    card5 = Card(5, 5, "Card 5 Done", LISTS[2].id, None, YESTERDAY_DATE)
    return [card1, card2, card3, card4, card5]

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

def test_recent_done_items_returns_tasks_from_today(cards_with_last_modified_dates):
    # Act
    view_model = ViewModel(cards_with_last_modified_dates, LISTS, False, TODAY_DATE)

    # Assert
    assert len(view_model.older_done_items) == 1
    assert len(view_model.recent_done_items) == 1

    assert view_model.older_done_items[0].id == 3
    assert view_model.recent_done_items[0].id == 4

def test_lists_view_returns_all_tasks_if_show_all_tasks_false_and_under_five_tasks(four_completed_tasks):
    # Act
    view_model = ViewModel(four_completed_tasks, LISTS, False, TODAY_DATE)

    # Assert
    assert len(view_model.done_list_items_view) == 4

def test_lists_view_returns_no_old_tasks_if_show_all_tasks_false_and_five_or_more_tasks(five_completed_tasks):
    # Act
    view_model = ViewModel(five_completed_tasks, LISTS, False, TODAY_DATE)

    # Assert
    assert len(view_model.done_list_items_view) == 0
