from datetime import datetime

from .card import Card

class CardViewModel:
    def __init__(self, card: Card):
        self.id = card.id
        self.idShort = card.idShort
        self.title = card.title
        self.list_id = card.list_id
        self.due_date = self._getOrNoneDateFormatStr(card.due_date)
        self.last_modified = self._getOrNoneDateFormatStr(card.last_modified)

    @staticmethod
    def _getOrNoneDateFormatStr(date):
        if date is None:
            return None
        # return datetime.combine(date, datetime.min.time()).strftime('%a %d %b %Y')
        return date
