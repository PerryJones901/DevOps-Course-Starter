import os
from datetime import datetime, timedelta
from unittest import mock

from bs4 import BeautifulSoup
from dotenv import find_dotenv, load_dotenv
import flask
import pytest

import app
import tests.test_mongo_constants as const

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = app.create_app()
    test_app.testing = True

    cards_mock = mock.Mock()
    cards_mock.find.return_value = const.CARD_ARR
    test_app.data_manager.cards = cards_mock

    lists_mock = mock.Mock()
    lists_mock.find.return_value = const.LIST_ARR
    test_app.data_manager.lists = lists_mock

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

def test_index_page_contains_card_names(client):
    response_data = client.get('/').data
    soup = BeautifulSoup(response_data, 'html.parser')
    all_task_id_and_name_elements = soup.find_all(class_="task-id-and-name")
    for index, card in enumerate(const.CARD_ARR):
        assert (card["name"] in all_task_id_and_name_elements[index].string)
