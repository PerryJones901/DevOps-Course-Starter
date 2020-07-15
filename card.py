import env_vars as env
from datetime import datetime

class Card:
    def __init__(self, id, idShort, title, due_date, list_id):
        self.id = id
        self.idShort = idShort
        self.title = title
        self.due_date = due_date
        self.list_id = list_id

    @classmethod
    def json_to_card(cls, json):
        id          = json['id']
        idShort     = json['idShort']
        title       = json['name']
        list_id     = json['idList']

        if json['due'] is None:
            due_date = None
        else:
            due_date = datetime.strptime(json['due'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%a %d %b %Y')

        return cls(id, idShort, title, due_date, list_id)
