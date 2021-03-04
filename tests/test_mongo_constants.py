from datetime import datetime

TODO_LIST = {
    "_id": "list1",
    "name": "To Do",
}

DOING_LIST = {
    "_id": "list2",
    "name": "Doing",
}

DONE_LIST = {
    "_id": "list3",
    "name": "Done",
}

TODO_CARD = {
    "_id": "111111",
    "id_short":"1",
    "name": "Test Name 1",
    "list_id": TODO_LIST["_id"],
    "due_date": None,
    "date_last_activity": datetime.strptime("2020-01-01T19:17:11.988Z", '%Y-%m-%dT%H:%M:%S.%fZ')
}

DOING_CARD = {
    "_id": "222222",
    "id_short":"2",
    "name": "Test Name 2",
    "list_id": DOING_LIST["_id"],
    "due_date": datetime.strptime("2022-01-01T22:17:11.988Z", '%Y-%m-%dT%H:%M:%S.%fZ'),
    "date_last_activity": datetime.strptime("2020-05-06T00:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%fZ')
}

DONE_CARD = {
    "_id": "333333",
    "id_short":"3",
    "name": "Test Name 3",
    "list_id": DONE_LIST["_id"],
    "due_date": datetime.strptime("2019-12-31T19:17:11.988Z", '%Y-%m-%dT%H:%M:%S.%fZ'),
    "date_last_activity": datetime.strptime("2021-02-12T06:09:45.638Z", '%Y-%m-%dT%H:%M:%S.%fZ')
}

LIST_ARR = [
    TODO_LIST,
    DOING_LIST,
    DONE_LIST,
]

CARD_ARR = [
    TODO_CARD,
    DOING_CARD,
    DONE_CARD
]
