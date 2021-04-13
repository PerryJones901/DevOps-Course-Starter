from bson.objectid import ObjectId
from datetime import date, datetime
import pymongo
from typing import List

from api.itask_data_manager import ITaskDataManager
from api.mongo_config import MongoConfig
from models.card import Card
from models.card_list import CardList

class MongoHelper(ITaskDataManager):
    def __init__(self, mongo_config: MongoConfig):
        self.config = mongo_config
        self.client = pymongo.MongoClient(self._get_connection_string(mongo_config))
        self.db = self.client[mongo_config.MONGO_DB_NAME]
        self.board_metadata = self.db['board-metadata']
        self.cards = self.db['cards']
        self.lists = self.db['lists']
        self.initialise_db()

    def get_cards(self) -> List[Card]:
        mongo_card_array = self.cards.find()
        return [Card.mongo_dict_to_card(mongo_card) for mongo_card in mongo_card_array]
    
    def get_card(self, id) -> Card:
        mongo_card = self.cards.find({'_id': ObjectId(id)})
        return Card.mongo_dict_to_card(mongo_card)

    def add_card(self, title, list_id, due):
        id_short = self._increment_id_short_counter()
        due_date = self._get_due_or_default(due)
        latest_modified = datetime.now()
        self.cards.insert_one(self._mongo_card_dict(id_short, title, list_id, due_date, latest_modified))

    def delete_card(self, id):
        self.cards.delete_one({'_id': ObjectId(id)})

    def get_lists(self):
        mongo_card_lists = self.lists.find()
        return [CardList.mongo_dict_to_card_list(mongo_list) for mongo_list in mongo_card_lists]

    def get_list(self, name):
        mongo_card_list = self.lists.find_one({'name': name})
        return CardList.mongo_dict_to_card_list(mongo_card_list)

    def move_card_to_list(self, card_id, list_id):
        datetime_now = datetime.now()
        self.cards.update_one({'_id': ObjectId(card_id)},{'$set':{'list_id': list_id, 'date_last_activity': datetime_now}})

    def add_test_db(self, name: str):
        new_db = self.client[name]

    def drop_test_db(self, name: str):
        self.client.drop_database(name)

    def _increment_id_short_counter(self):
        metadata = self.board_metadata.find_one()
        latest_short_id = metadata['id_short_latest_used']
        new_short_id = latest_short_id + 1
        self.board_metadata.update_one({'_id': metadata['_id']},{'$set':{'id_short_latest_used': new_short_id}})
        return str(new_short_id)

    @staticmethod
    def _get_connection_string(config: MongoConfig):
        return f"mongodb+srv://{config.MONGO_USERNAME}:"\
        + f"{config.MONGO_PASSWORD}@"\
        + f"{config.MONGO_CLUSTER_NAME}/"\
        + f"{config.MONGO_DB_NAME}?retryWrites=true&w=majority"

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
            self.lists.insert_many([{'name':'To Do'},{'name':'Doing'},{'name':'Done'}])
        if self.board_metadata.count_documents({}) == 0:
            self.board_metadata.insert_one({'id_short_latest_used':0})
