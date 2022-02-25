from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
from todo_app.data.trello_items import complete_item, get_items, add_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    return render_template('index.html', tasks = get_items())

@app.route('/new', methods=['POST'])
def new_task():
    add_item(request.form.get('title'))
    return redirect(url_for("index"))

@app.route('/complete/<id>')
def complete_task(id):
    complete_item(id)
    return redirect(url_for("index"))