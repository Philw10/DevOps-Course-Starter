# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Using Trello to manage list

The program uses Trello to manage the list items.  In order for this to work you will need a Trello account.

Please go to (https://www.trello.com) to sign up for an account and create a new board for the to do list.

You will also need to register for an API key, and token.  Instructions on completing this are accessed on the following link (https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/).

Please then update the '.env' file with the key and token by copying, pasting, and modifying the following:-

```bash
API_KEY=YOUR KEY ADDED HERE
API_TOKEN=YOUR TOKEN ADDED HERE
BOARD_ID=THE ID FOR YOUR BOARD CONTAINING YOUR LISTS
OPEN_LIST_ID=THE ID FOR YOUR OPEN LIST
CLOSED_LIST_ID=THE ID FOR YOUR CLOSED LIST
```
## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing

This app utilises pytest for its unit and integration tests.

In order to use pytest please first install it using pip and the following in the terminal

```bash
$ pip install pytest
```

Pytest can then be run by entering the following into terminal

```bash
$ poetry run pytest
```