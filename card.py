import env_vars as env
from datetime import datetime

class Card:
    def __init__(self, id, idShort, title, due_date, is_complete):
        self.id = id
        self.idShort = idShort
        self.title = title
        self.due_date = due_date
        self.is_complete = is_complete

    @classmethod
    def json_to_card(cls, json, is_complete):
        id = json['id']
        idShort = json['idShort']
        title = json['name']

        if json['due'] is None:
            due_date = None
        else:
            due_date = datetime.strptime(json['due'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%a %d %b %Y')

        return cls(id, idShort, title, due_date, is_complete)
