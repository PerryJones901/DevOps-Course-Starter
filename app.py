from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for

from api.mongo_config import MongoConfig
from api.mongo_helper import MongoHelper
import api.session_items as session
import api.sorter as sorter
from models.view_model import ViewModel

def create_app():
    app = Flask(__name__)
    config = MongoConfig()
    data_manager = MongoHelper(config)
    app.config.from_object(config)

    @app.route('/')
    def index():
        cards = data_manager.get_cards()
        sort_by_field = session.get_sort_by_field()
        items = sorter.sort_cards(cards, sort_by_field)
        lists = data_manager.get_lists()
        show_all = session.get_show_all_completed_tasks()
        item_view_model = ViewModel(items, lists, show_all, datetime.now().date())
        return render_template('index.html', view_model=item_view_model)

    @app.route('/sorted/<field>')
    def sorted_by(field):
        session.change_sort_by_field(field)
        return redirect(url_for('index'))

    @app.route('/show_all')
    def show_all_completed_tasks():
        session.toggle_show_all_completed_tasks()
        return redirect(url_for('index'))

    @app.route('/add', methods=['POST'])
    def add_card_to_list():
        title = request.form.get('title')
        list_name = request.form.get('card_list')
        due = request.form.get('due')
        card_list = data_manager.get_list(list_name)
        data_manager.add_card(title, card_list.id, due)
        return redirect(url_for('index'))

    @app.route('/card/<card_id>', methods=['POST'])
    def move_card_to_list(card_id):
        list_id = request.form.get('card_list')
        data_manager.move_card_to_list(card_id, list_id)
        return redirect(url_for('index'))

    @app.route('/delete/<card_id>', methods=['POST'])
    def delete_item(card_id):
        data_manager.delete_card(card_id)
        return redirect(url_for('index'))

    if __name__ == '__main__':
        app.run()

    return app
