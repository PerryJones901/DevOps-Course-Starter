from bson.objectid import ObjectId
from pymongo import MongoClient
from typing import List

from api.itask_data_manager import ITaskDataManager
from api.mongo_config import MongoConfig
from models.card import Card
from models.card_list import CardList

class MongoHelper(ITaskDataManager):
    def __init__(self, mongo_config: MongoConfig):
        self.config = mongo_config
        self.client = MongoClient(self._get_connection_string(mongo_config))
        self.db = self.client[mongo_config.MONGO_DB_NAME]
        self.cards = self.db['cards']
        self.lists = self.db['lists']
    
    def get_cards(self) -> List[Card]:
        mongo_card_array = self.cards.find()
        return [Card.mongo_dict_to_card(mongo_card) for mongo_card in mongo_card_array]
    
    def get_card(self, id) -> Card:
        mongo_card = self.cards.find({'_id': ObjectId(id)})
        return Card.mongo_dict_to_card(mongo_card)

    def add_card(self, title, list_id, due):
        self.cards.insert_one(self._mongo_card_json(title, list_id, due))

    def delete_card(self, id):
        self.cards.delete_one({'_id': ObjectId(id)})

    def get_lists(self):
        mongo_card_lists = self.lists.find()
        return [CardList.mongo_dict_to_card_list(mongo_list) for mongo_list in mongo_card_lists]

    def get_list(self, name):
        mongo_card_list = self.lists.find({'name': name})
        return CardList.mongo_dict_to_card_list(mongo_card_list)

    def move_card_to_list(self, card_id, list_id):
        self.cards.update_one({'_id': ObjectId(card_id)},{'$set':{'list_id': list_id}})

    @staticmethod
    def _get_connection_string(config: MongoConfig):
        return f"mongodb+srv://{config.MONGO_USERNAME}:\
            {config.MONGO_PASSWORD}@cluster0.vwqib.mongodb.net/\
            {config.MONGO_DB_NAME}?retryWrites=true&w=majority"

    @staticmethod
    def _mongo_card_json(title: str, list_id, due):
        return { 'title' : title, 'list_id': list_id, 'due': due }