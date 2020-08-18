from enum import Enum

def sort_lambda(field):
    return {
        'id' : lambda item: item.idShort,
        'title' : lambda item: item.title,
    }.get(field, lambda item: item.idShort)

def sort_cards(cards, field):
    return sorted(cards, key=sort_lambda(field))
