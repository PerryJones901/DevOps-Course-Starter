import env_vars as env

class Card:
    def __init__(self, id, idShort, title, is_complete):
        self.id = id
        self.idShort = idShort
        self.title = title
        self.is_complete = is_complete

    @staticmethod
    def is_done_list(id):
        return id == env.DONE_LIST_ID

    @staticmethod
    def json_to_card(json):
        id = json['id']
        idShort = json['idShort']
        title = json['name']
        is_complete = Card.is_done_list(json['idList'])
        return Card(id, idShort, title, is_complete)
