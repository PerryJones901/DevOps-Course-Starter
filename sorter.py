from enum import Enum

def sort_lambda(field):
    return {
        'id' : lambda item: item.idShort,
        'title' : lambda item: item.title,
        'status' : lambda item: item.is_complete
    }.get(field, lambda item: item.idShort)

def sort_cards(cards, field):
    return sorted(cards, key=sort_lambda(field))