import os
from threading import Thread

import pytest
from selenium import webdriver

from api.trello_config import TrelloConfig
from api.trello_helper import TrelloHelper
import app

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable
    config = TrelloConfig()
    trello_helper = TrelloHelper(config)
    board_id = trello_helper.add_board()
    os.environ['TRELLO_BOARD_ID'] = board_id
    
    # construct the new application
    application = app.create_app()
    
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # Tear Down
    thread.join(1)
    trello_helper.delete_board(board_id)

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'The Perfect Productivity Platform'
