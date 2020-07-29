class CardList:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    @classmethod
    def json_to_card_list(cls, json):
        id = json['id']
        name = json['name']
        return cls(id, name)