from bson.objectid import ObjectId
from pymongo import MongoClient
from api.itask_data_manager import ITaskDataManager
from api.mongo_config import MongoConfig

class MongoHelper(ITaskDataManager):
    def __init__(self, mongo_config: MongoConfig):
        self.config = mongo_config
        self.client = MongoClient(self._get_connection_string(mongo_config))
        self.db = self.client[mongo_config.MONGO_DB_NAME]
        self.cards = self.db['cards']
        self.lists = self.db['lists']
    
    def get_cards(self):
        self.cards.find()
    
    def get_card(self, id):
        self.cards.find({'_id': ObjectId(id)})

    def add_card(self, title, list_id, due):
        self.cards.insert_one(self._mongo_card_json(title, list_id, due))

    def delete_card(self, id):
        self.cards.delete_one({'_id': ObjectId(id)})

    def get_lists(self):
        self.lists.find()

    def get_list(self, name):
        self.lists.find({'name': name})

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