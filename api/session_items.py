from flask import session

_DEFAULT_SORT_BY = 'idShort'
_DEFAULT_SHOW_ALL_COMPLETED = True

def get_sort_by_field():
    return session.get('sort_by', _DEFAULT_SORT_BY)

def get_show_all_completed_tasks():
    return session.get('show_all_complete', _DEFAULT_SHOW_ALL_COMPLETED)

def change_sort_by_field(field):
    session['sort_by'] = field

def toggle_show_all_completed_tasks():
    session['show_all_complete'] = not get_show_all_completed_tasks()
