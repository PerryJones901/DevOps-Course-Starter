from flask import Flask, render_template, request, redirect, url_for
import session_items as session
import sorter as sorter
import trello_helper as trello

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/index')
def index():
    cards = trello.get_cards()
    sort_by_field = session.get_sort_by_field()
    items = sorter.sort_cards(cards, sort_by_field)
    return render_template('index.html', items=items)

@app.route('/sorted/<field>')
def sorted_by(field):
    session.change_sort_by_field(field)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_something():
    title = request.form.get('title')
    due = request.form.get('due')
    print(due)
    trello.add_card(title, due)
    return redirect(url_for('index'))

@app.route('/toggle/<id>', methods=['POST'])
def update_something(id):
    item = trello.get_card(id)
    if item is not None:
        if item.is_complete:
            trello.mark_card_todo(id)
        else:
            trello.mark_card_complete(id)
    return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST'])
def delete_item(id):
    trello.delete_card(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
