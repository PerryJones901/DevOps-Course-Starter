import env_vars as env
from datetime import datetime

class Card:
    def __init__(self, id, idShort, title, due_date, is_complete):
        self.id = id
        self.idShort = idShort
        self.title = title
        self.due_date = due_date
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

        if json['due'] is None:
            due_date = None
        else:
            due_date = datetime.strptime(json['due'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%a %d %b %Y')

        return Card(id, idShort, title, due_date, is_complete)
