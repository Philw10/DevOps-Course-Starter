import os
import requests
from flask_login import LoginManager, login_required, UserMixin, login_user
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
from todo_app.data.mongo_items import get_items, add_item, doing_item, complete_item
from todo_app.flask_config import Config
from todo_app.data.view_model import ViewModel

class User(UserMixin):
        def __init__(self, id):
                self.id = id


def create_app():
        app = Flask(__name__)
        app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'
        app.config.from_object(Config())

        login_manager = LoginManager()

        @login_manager.unauthorized_handler
        def unauthenticated():
                client_id = os.getenv('GITHUB_OAUTH_CLIENT_ID')
                return redirect (f'https://github.com/login/oauth/authorize?client_id={client_id}')
               
        @login_manager.user_loader
        def load_user(user_id):
                return User(user_id)

        login_manager.init_app(app)

        @app.route('/login/callback')
        def validate_user():
                code = request.args.get('code', '')
                params = {'client_id': os.getenv('GITHUB_OAUTH_CLIENT_ID'), 'client_secret': os.getenv('GITHUB_OAUTH_SECRET'), 'code': code}
                headers_for_token = {'Accept': 'application/json'}
                access_token = (requests.post('https://github.com/login/oauth/access_token', params=params, headers=headers_for_token).json())['access_token']
                           
                headers_for_user = {'Authorization': f'Bearer {access_token}'}
                user_details = requests.get('https://api.github.com/user', headers=headers_for_user).json()
                id = User(user_details['id'])
                login_user(id)
                return redirect("/")

        @app.route('/')
        @login_required
        def index():
                task_view_model = ViewModel(get_items())
                return render_template('index.html', view_model = task_view_model)

        @app.route('/new', methods=['POST'])
        @login_required
        def new_task():
                add_item(request.form.get('title'))
                return redirect(url_for("index"))

        @app.route('/complete/<id>')
        @login_required
        def complete_task(id):
                complete_item(id)
                return redirect(url_for("index"))

        @app.route('/doing/<id>')
        @login_required
        def doing_task(id):
                doing_item(id)
                return redirect(url_for("index"))
        
        return app