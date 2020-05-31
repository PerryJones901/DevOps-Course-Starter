from flask import Flask, render_template, request, redirect, url_for
import session_items as session

app = Flask(__name__)
app.config.from_object('flask_config.Config')

def toggle_string(status_string):
    if status_string == 'Not Started':
        return 'Completed'
    return 'Not Started'

@app.route('/')
def index():
    items = session.get_items()
    return render_template('index.html', items=items)

@app.route('/sorted/<field>')
def sorted_by(field):
    if field == 'status':
        reverse = True
    else:
        reverse = False
    sorted_items = sorted(session.get_items(), key=lambda item: item[field], reverse=reverse)
    return render_template('index.html', items=sorted_items)

@app.route('/add', methods=['POST'])
def add_something():
    session.add_item(request.form.get('title'))
    return index()

@app.route('/toggle/<int:id>', methods=['POST'])
def update_something(id):
    item = session.get_item(id)
    if item is not None:
        item['status'] = toggle_string(item['status'])
        session.save_item(item)
    return index()

@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    session.delete_item(id)
    return index()

if __name__ == '__main__':
    app.run()
