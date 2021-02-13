class CardList:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
    
    @classmethod
    def json_to_card_list(cls, json):
        id = json['id']
        name = json['name']
        return cls(id, name)

    @classmethod
    def mongo_dict_to_card_list(cls, mongo_dict: dict):
        id = str(mongo_dict['_id'])
        name = mongo_dict['name']
        return cls(id, name)