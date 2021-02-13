from datetime import date, datetime

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
        due_date        = cls._get_date_or_none_trello(json, 'due')
        last_modified   = cls._get_date_or_none_trello(json, 'dateLastActivity')

        return cls(id, idShort, title, list_id, due_date, last_modified)

    @classmethod
    def mongo_dict_to_card(cls, mongo_dict: dict):
        id = str(mongo_dict['_id'])
        idShort = mongo_dict['id_short']
        title = mongo_dict['name']
        list_id = mongo_dict['list_id']
        due_date = cls._get_date_or_none(mongo_dict['due_date'])
        last_modified = cls._get_date_or_none(mongo_dict['date_last_activity'])

        return cls(id, idShort, title, list_id, due_date, last_modified)

    @staticmethod
    def _get_date_or_none_trello(json, key):
        if json[key] is None:
            return None
        return datetime.strptime(json[key], '%Y-%m-%dT%H:%M:%S.%fZ').date()

    @staticmethod
    def _get_date_or_none(datetime: datetime):
        if datetime is None:
            return None
        return datetime.date()
