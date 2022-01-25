from flask import Flask, render_template, request
from werkzeug.utils import redirect
from todo_app.data.session_items import add_item, save_item, get_item, get_items
#from todo_app.data.trello_items import get_items


from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    return render_template('index.html', tasks = get_items())

@app.route('/new', methods=['POST'])
def new_task():
    add_item(request.form.get('title'))
    return redirect("/")
