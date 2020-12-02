import os
import tests.test_constants as const
from datetime import datetime, timedelta
from unittest import mock

import flask
import pytest
from dotenv import find_dotenv, load_dotenv

import app
from models.card import Card
from models.card_list import CardList
from models.view_model import ViewModel

from .helpers.mock_response import MockResponse

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

def params_url_string(params):
    config = flask.current_app.config
    params = {"key": config.KEY, "token": config.TOKEN, **params}
    params_url_suffix = '?'
    for (key, value) in params:
        params_url_suffix = params_url_suffix + f'{key}={value}'
    return params_url_suffix

def mock_get_requests(*args, **kwargs):
    config = flask.current_app.config
    if args[0] == f'https://api.trello.com/1/boards/{config["BOARD_ID"]}/cards':
        return MockResponse(const.CARD_ARR, 200)
    elif args[0] == f'https://api.trello.com/1/boards/{config["BOARD_ID"]}/lists':
        return MockResponse(const.LIST_ARR, 200)

    return MockResponse(None, 404)

@mock.patch('requests.get', side_effect=mock_get_requests)
def test_index_page(mock_get_requests, client):
    response = client.get('/')
    assert response.status_code == 200
