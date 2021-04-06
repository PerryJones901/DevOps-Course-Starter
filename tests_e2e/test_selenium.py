import os
import random
import string
from threading import Thread

from dotenv import find_dotenv, load_dotenv
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import app
from api.mongo_config import MongoConfig
from api.mongo_helper import MongoHelper
import tests.test_mongo_constants as const

@pytest.fixture(scope='module')
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver

@pytest.fixture(scope='module')
def test_app():
    # Create a new Mongo Database & update the Mongo Database Name environment variable
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    
    config = MongoConfig()
    data_manager = MongoHelper(config)
    test_db_name = "selenium_test_db"
    data_manager.add_test_db(test_db_name)
    data_manager.client[test_db_name]['lists'].remove({})
    data_manager.client[test_db_name]['lists'].insert_many(const.LIST_ARR)
    data_manager.client[test_db_name]['board-metadata'].delete_many({})
    data_manager.client[test_db_name]['board-metadata'].insert_one({'id_short_latest_used': 0})
    os.environ['MONGO_DB_NAME'] = test_db_name
    os.environ['LOGIN_DISABLED'] = "True"
    
    # Create App
    application = app.create_app()
    
    # Start App in Thread
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    # Tear Down
    thread.join(1)
    data_manager.drop_test_db(test_db_name)

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
