TODO_LIST = {
    "id": "list1",
    "name": "To Do",
}

DOING_LIST = {
    "id": "list2",
    "name": "Doing",
}

DONE_LIST = {
    "id": "list3",
    "name": "Done",
}

LIST_ARR = [
    TODO_LIST,
    DOING_LIST,
    DONE_LIST
]

TODO_CARD = {
    "id": "abc1",
    "idList": TODO_LIST['id'],
    "idShort": 1,
    "name": "This is another To Do item",
    "due": None,
    "dateLastActivity": "2020-06-22T19:17:11.988Z",
}

DOING_CARD = {
    "id": "abc2",
    "idList": DOING_LIST['id'],
    "idShort": 2,
    "name": "This is another To Do item",
    "due": None,
    "dateLastActivity": "2020-06-22T19:17:11.988Z",
}

DONE_CARD = {
    "id": "abc3",
    "idList": DONE_LIST['id'],
    "idShort": 3,
    "name": "This is another To Do item",
    "due": None,
    "dateLastActivity": "2020-06-22T19:17:11.988Z",
}

CARD_ARR = [
    TODO_CARD,
    DOING_CARD,
    DONE_CARD
]
