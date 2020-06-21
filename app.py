from flask import Flask, render_template, request, redirect, url_for
import session_items as session
import trello_helper as trello

app = Flask(__name__)
app.config.from_object('flask_config.Config')

def toggle_string(status_string):
    if status_string == 'Not Started':
        return 'Completed'
    return 'Not Started'

@app.route('/index')
def index():
    items = trello.get_cards()
    return render_template('index.html', items=items)

@app.route('/sorted/<field>')
def sorted_by(field):
    session.sort_by(field)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_something():
    trello.add_card(request.form.get('title'))
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>', methods=['POST'])
def update_something(id):
    item = trello.get_card(id)
    if item is not None:
        if item.is_complete:
            trello.mark_card_todo(id)
        else:
            trello.mark_card_complete(id)
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    trello.delete_card(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
