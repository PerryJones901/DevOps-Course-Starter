from datetime import datetime
from pprint import pprint
import requests

from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, current_user
from oauthlib.oauth2 import WebApplicationClient

from api.auth import authorisation_disabled, get_user, requires_role
from api.auth_config import AuthConfig
from api.app_config import AppConfig
from api.mongo_helper import MongoHelper
import api.session_items as session
import api.sorter as sorter
from models.role import Role
from models.user import User
from models.view_model import ViewModel

def create_app():
    app = Flask(__name__)
    config = AppConfig()
    data_manager = MongoHelper(config)
    app.secret_key = config.SECRET_KEY
    app.data_manager = data_manager
    app.config.from_object(config)
    auth_config = AuthConfig()

    client = WebApplicationClient(auth_config.AUTH_CLIENT_ID)
    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        uri = client.prepare_request_uri('https://github.com/login/oauth/authorize')
        return redirect(uri)

    @app.route('/login/callback')
    def login_callback():
        code_param = request.args.get("code")
        url, headers, body = client.prepare_token_request('https://github.com/login/oauth/access_token', client_id=auth_config.AUTH_CLIENT_ID, client_secret=auth_config.AUTH_CLIENT_SECRET, code=code_param)
        token_response = requests.post(url, body, headers=headers)
        client.parse_request_body_response(token_response.text)
        user_uri, headers, body = client.add_token("https://api.github.com/user")
        github_user_profile= requests.get(user_uri, headers=headers).json()
        login_user(get_user(github_user_profile['id']))
        return redirect(url_for('index'))
    
    @login_manager.user_loader
    def load_user(user_id):
        return get_user(user_id)
    login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        cards = data_manager.get_cards()
        sort_by_field = session.get_sort_by_field()
        items = sorter.sort_cards(cards, sort_by_field)
        lists = data_manager.get_lists()
        show_all = session.get_show_all_completed_tasks()
        if(authorisation_disabled()):
            user_role = Role.WRITER
        else:
            user_role = get_user(current_user.get_id()).role

        item_view_model = ViewModel(items, lists, show_all, datetime.now().date(), user_role)
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
    @login_required
    @requires_role(Role.WRITER)
    def add_card_to_list():
        title = request.form.get('title')
        list_name = request.form.get('card_list')
        due = request.form.get('due')
        card_list = data_manager.get_list(list_name)
        data_manager.add_card(title, card_list.id, due)
        return redirect(url_for('index'))

    @app.route('/card/<card_id>', methods=['POST'])
    @login_required
    @requires_role(Role.WRITER)
    def move_card_to_list(card_id):
        list_id = request.form.get('card_list')
        data_manager.move_card_to_list(card_id, list_id)
        return redirect(url_for('index'))

    @app.route('/delete/<card_id>', methods=['POST'])
    @login_required
    @requires_role(Role.WRITER)
    def delete_item(card_id):
        data_manager.delete_card(card_id)
        return redirect(url_for('index'))

    if __name__ == '__main__':
        app.run()

    return app
