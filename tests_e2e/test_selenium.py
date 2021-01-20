import os
from threading import Thread

from dotenv import find_dotenv, load_dotenv
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from api.trello_config import TrelloConfig
from api.trello_helper import TrelloHelper
import app

@pytest.fixture(scope='module')
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=opts) as driver:
        yield driver

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    
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

    input_element = driver.find_element_by_id("title")
    input_element.send_keys("Do the washing")
    
    submit_button = driver.find_element_by_css_selector("button.add-task-button")
    submit_button.submit()
    
    task = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='task-id-and-name']"))
    )

    assert "Do the washing" in task.text
