from logging import Logger
from bson.objectid import ObjectId
from datetime import datetime
import pymongo
from typing import List
from pymongo.database import Database
from pymongo.mongo_client import MongoClient

from api.itask_data_manager import ITaskDataManager
from api.app_config import AppConfig
from models.card import Card
from models.card_list import CardList

class MongoHelper(ITaskDataManager):
    def __init__(self, app_config: AppConfig, logger: Logger):
        self.logger = logger
        self.client = self._get_mongo_client(app_config.MONGO_CONNECTION_STRING)
        self.db = self._get_mongo_db(app_config.MONGO_DB_NAME)
        self.board_metadata = self.db['board-metadata']
        self.cards = self.db['cards']
        self.lists = self.db['lists']
        self.initialise_db()

    def get_cards(self) -> List[Card]:
        self.logger.debug('Getting cards...')
        try:
            mongo_card_array = self.cards.find()
            return [Card.mongo_dict_to_card(mongo_card) for mongo_card in mongo_card_array]
        except Exception as e:
            self.logger.error('Error getting cards. Error message: %s', e)
    
    def get_card(self, id) -> Card:
        self.logger.debug('Getting Card %s ...', id)
        try:
            mongo_card = self.cards.find({'_id': ObjectId(id)})
            return Card.mongo_dict_to_card(mongo_card)
        except Exception as e:
            self.logger.error('Error getting Card %s. Error message: %s', id, e)

    def add_card(self, title, list_id, due) -> str:
        self.logger.debug('Creating new card...')
        try:
            id_short = self._increment_id_short_counter()
            due_date = self._get_due_or_default(due)
            latest_modified = datetime.now()
            result = self.cards.insert_one(self._mongo_card_dict(id_short, title, list_id, due_date, latest_modified))
            card_id = str(result.inserted_id)
        except Exception as e:
            self.logger.error('Error creating new card. Error message: %s', e)
        else:
            self.logger.info(f"Card added with ID %s", card_id)
            return card_id

    def delete_card(self, id):
        self.logger.debug('Deleting Card %s ...', id)
        try:
            self.cards.delete_one({'_id': ObjectId(id)})
        except Exception as e:
            self.logger.error('Error deleting Card %s. Error message: %s', id, e)
        else:
            self.logger.info('Deleted Card %s', id)

    def get_lists(self):
        self.logger.debug('Getting lists...')
        try:
            mongo_card_lists = self.lists.find()
            return [CardList.mongo_dict_to_card_list(mongo_list) for mongo_list in mongo_card_lists]
        except Exception as e:
            self.logger.error('Error getting lists. Error message: %s', e)

    def get_list(self, name):
        self.logger.debug('Getting list with name: %s ...', name)
        try:
            mongo_card_list = self.lists.find_one({'name': name})
            return CardList.mongo_dict_to_card_list(mongo_card_list)
        except Exception as e:
            self.logger.error('Error getting list with name: %s. Error message: %s', name, e)

    def move_card_to_list(self, card_id, list_id):
        self.logger.debug('Moving Card %s to List %s ...', card_id, list_id)
        try:
            datetime_now = datetime.now()
            self.cards.update_one({'_id': ObjectId(card_id)},{'$set':{'list_id': list_id, 'date_last_activity': datetime_now}})
        except Exception as e:
            self.logger.error('Error moving Card %s to List %s. Error message: %s', card_id, list_id, e)

    def add_test_db(self, name: str):
        self.logger.debug('Creating Test DB with name: %s ...', name)
        try:
            new_db = self.client[name]
        except Exception as e:
            self.logger.error('Error creating Test DB with name: %s. Error message: %s', name, e)
        

    def drop_test_db(self, name: str):
        self.logger.debug('Dropping Test DB with name: %s ...', name)
        try:
            self.client.drop_database(name)
        except Exception as e:
            self.logger.error('Error creating Test DB with name: %s. Error message: %s', name, e)

    def _get_mongo_client(self, mongo_connection_string) -> MongoClient:
        try:
            self.logger.debug('Connecting to Mongo...')
            client = pymongo.MongoClient(mongo_connection_string)
        except pymongo.errors.ConnectionFailure as e:
            self.logger.critical('Cannot connect to Mongo. Error message: %s', e)
            pass
        except Exception as e:
            self.logger.critical('Error occuring connecting to Mongo. Error message: %s', e)
            pass
        else:
            self.logger.info('Connected to Mongo')
            return client

    def _get_mongo_db(self, db_name) -> Database:
        try:
            self.logger.debug('Connecting to Mongo DB with name: %s ...', db_name)
            db = self.client[db_name]
        except Exception as e:
            self.logger.critical('Error occuring connecting to Mongo DB with name %s. Error message: %s', db_name, e)
            pass
        else:
            self.logger.info('Connected to Mongo DB with name: %s', db_name)
            return db

    def _increment_id_short_counter(self):
        self.logger.debug('Incrementing id_short counter...')
        try:
            metadata = self.board_metadata.find_one()
            latest_short_id = metadata['id_short_latest_used']
            new_short_id = latest_short_id + 1
            self.board_metadata.update_one({'_id': metadata['_id']},{'$set':{'id_short_latest_used': new_short_id}})
            return str(new_short_id)
        except Exception as e:
            self.logger.error('Error incrementing id_short counter. Error message: %s', e)

    @staticmethod
    def _mongo_card_dict(id_short: str, title: str, list_id: str, due: datetime, last_activity: datetime):
        return { 'id_short': id_short, 'name' : title, 'list_id': list_id, 'due_date': due, 'date_last_activity': last_activity }

    @staticmethod
    def _get_due_or_default(date_str: str):
        if "" == date_str:
            return None
        else:
            return datetime.strptime(date_str, '%Y-%m-%d')

    def initialise_db(self):
        if self.lists.count_documents({}) == 0:
            self.logger.warning('Database has no lists. Creating lists: To Do; Doing; Done; ...')
            try:
                self.lists.insert_many([{'name':'To Do'},{'name':'Doing'},{'name':'Done'}])
            except Exception as e:
                self.logger.error('Error adding lists. Error message: %s', e)
            else:
                self.logger.info('Lists added: To Do; Doing; Done;')

        if self.board_metadata.count_documents({}) == 0:
            self.logger.warning('Database has no board metadata. Creating metadata object ...')
            try:
                self.board_metadata.insert_one({'id_short_latest_used':0})
            except Exception as e:
                self.logger.error('Error adding metadata. Error message: %s', e)
            else:
                self.logger.info('Metadata added')
