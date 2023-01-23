import os
import requests
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
from todo_app.data.mongo_items import get_items, add_item, doing_item, complete_item
from todo_app.flask_config import Config
from todo_app.data.view_model import ViewModel
from loggly.handlers import HTTPSHandler
from logging import Formatter

class User(UserMixin):
        def __init__(self, id):
                self.id = id
                self.role = 'writer' if id == os.getenv('ADMIN_ID') else 'reader'

def create_app():
        app = Flask(__name__)
        app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'
        app.config['LOG_LEVEL'] = os.getenv('LOG_LEVEL')
        app.config['LOGGLY_TOKEN'] = os.getenv('LOGGLY_TOKEN')
        app.config.from_object(Config())

        if app.config['LOGGLY_TOKEN'] is not None:
                handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
                handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
                )
                app.logger.addHandler(handler)

        app.logger.setLevel(app.config['LOG_LEVEL'])
      
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
                app.logger.info("User ID %s successfully logged in", id)
                return redirect("/")

        def authorized():
                return ((app.config['LOGIN_DISABLED'] == True) or (current_user.role == 'writer'))                         
        
        @app.route('/')
        @login_required
        def index():
                try:
                        task_view_model = ViewModel(get_items())
                except:
                        app.logger.critical("To do list data failed to generate")            
                auth_type = 'writer' if app.config['LOGIN_DISABLED'] == True else current_user.role
                return render_template('index.html', view_model = task_view_model, auth_type = auth_type)

        @app.route('/new', methods=['POST'])
        @login_required
        def new_task():
                if authorized():
                        try:
                                add_item(request.form.get('title'))
                                app.logger.debug("Task successfully added: %s", request.form.get('title'))
                        except:
                                app.logger.error("Error adding new item to list: %s", request.form.get('title'))

                return redirect(url_for("index"))

        @app.route('/complete/<id>')
        @login_required
        def complete_task(id):
                if authorized():
                        try:
                                complete_item(id)
                                app.logger.debug("Task successfully completed: %s", id)
                        except:
                                app.logger.error("Error completing item ID: %s", id)

                return redirect(url_for("index"))

        @app.route('/doing/<id>')
        @login_required
        def doing_task(id):
                if authorized():
                        try:
                                doing_item(id)
                                app.logger.debug("Task successfully moved to doing list: %s", id)                                
                        except:
                                app.logger.error("Error moving item to doing list.  ID: %s", request.form.get('title'))
                return redirect(url_for("index"))
     
        return app