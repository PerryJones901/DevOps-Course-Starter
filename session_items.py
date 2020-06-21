from flask import session

_DEFAULT_SORT_BY = 'idShort'

def get_sort_by_field():
    return session.get('sort_by', _DEFAULT_SORT_BY)

def change_sort_by_field(field):
    session['sort_by'] = field
