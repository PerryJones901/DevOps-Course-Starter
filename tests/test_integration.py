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
    with mock.patch('pymongo.MongoClient', side_effect=mock_mongo_client):
        test_app = app.create_app()
    test_app.testing = True

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

def mock_mongo_client(*args, **kwargs):
    cards_mock = mock.Mock()
    cards_mock.find.return_value = const.CARD_ARR

    lists_mock = mock.Mock()
    lists_mock.find.return_value = const.LIST_ARR
    lists_mock.count_documents.return_value = 3

    board_metadata = mock.Mock()
    lists_mock.count_documents.return_value = 1

    return {
         os.environ.get('MONGO_DB_NAME'): {
            'cards': cards_mock,
            'lists': lists_mock,
            'board-metadata': board_metadata
        }
    }

@mock.patch('pymongo.MongoClient', side_effect=mock_mongo_client)
def test_index_page_contains_card_names(mock_mongo_client, client):
    response_data = client.get('/').data
    soup = BeautifulSoup(response_data, 'html.parser')
    all_task_id_and_name_elements = soup.find_all(class_="task-id-and-name")
    for index, card in enumerate(const.CARD_ARR):
        assert (card["name"] in all_task_id_and_name_elements[index].string)
