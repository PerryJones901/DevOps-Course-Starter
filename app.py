from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import session_items as session
import sorter as sorter
import trello_helper as trello
from view_model import ViewModel

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/')
def index():
    cards = trello.get_cards()
    sort_by_field = session.get_sort_by_field()
    items = sorter.sort_cards(cards, sort_by_field)
    lists = trello.get_lists()
    item_view_model = ViewModel(items, lists, True, datetime.now().date())
    return render_template('index.html', view_model=item_view_model)

@app.route('/sorted/<field>')
def sorted_by(field):
    session.change_sort_by_field(field)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_card_to_list():
    title = request.form.get('title')
    list_id = request.form.get('list_id')
    due = request.form.get('due')
    trello.add_card(title, list_id, due)
    return redirect(url_for('index'))

@app.route('/card/<card_id>/list/<list_id>', methods=['POST'])
def move_card_to_list(card_id, list_id):
    trello.move_card_to_list(card_id, list_id)
    return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST'])
def delete_item(id):
    trello.delete_card(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
