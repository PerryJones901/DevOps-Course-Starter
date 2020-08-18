from datetime import date, datetime

import env_vars as env

class Card:
    def __init__(self, id: str, idShort: str, title: str, list_id: str, due_date: date, last_modified: date):
        self.id = id
        self.idShort = idShort
        self.title = title
        self.list_id = list_id
        self.due_date = due_date
        self.last_modified = last_modified

    @classmethod
    def json_to_card(cls, json):
        id              = json['id']
        idShort         = json['idShort']
        title           = json['name']
        list_id         = json['idList']
        due_date        = cls._getOrNoneDate(json, 'due')
        last_modified   = cls._getOrNoneDate(json, 'dateLastActivity')

        return cls(id, idShort, title, list_id, due_date, last_modified)

    @staticmethod
    def _getOrNoneDate(json, key):
        if json[key] is None:
            return None
        return datetime.strptime(json[key], '%Y-%m-%dT%H:%M:%S.%fZ').date()
