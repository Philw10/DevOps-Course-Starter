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

Pytest can then be run by entering the following into terminal

```bash
$ poetry run pytest
```

## Provision of VM via Ansible

The files to_do_playbook, and ansible-inventory are provided in the todo_app folder in order to set up a managed node from a Ansible controller node.

In order to run the playbook please make sure you have Ansible installed on the controller node by running the 'ansible --version' command.

Once installation confirmed the nodes need to be connected via SSH to continue.

Please place both the playbook, and inventory files onto the controller note.  The following command can then be used in order to provision and run the to-do app on the managed node:

```bash
$ ansible-playbook to_do_playbook.yml -i ansible-inventory
```
You will be required to input the apps enviromental config (e.g your trello keys) as the playbook runs.

The app can then be accessed via the IP address of your VM followed by :5000 (e.g 0.0.0.0:5000)

## Docker

A dockerfile is provided to provision containers through Docker.  

Using the supplied file Docker can create both a production environment using Gunicorn, and a development environment using Flask.

Please make sure a file is also created in the base directory called env.list.  This directory should include all secret environment environment vairables needed to run the app (Contents of the .env file).

The production, and development image can be created by using the following command.  Please make sure you have Docker running.

```bash
$ docker build --target production --tag todo-app:prod .
$ docker build --target development --tag todo-app:dev .
```
This command produces two images called todo-app with the tags prod, and dev.

Containers can be build and run using the images with the following commands:

Production:
```bash
docker run --env-file env.list --publish 80:80 todo-app:prod 
```
This command loads the env vairables at runtime and publishes the app to port 80.  It can be accessed on [`http://localhost:80/`](http://localhost:80/)

Development:
```bash
docker run --env-file env.list --publish 5000:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:dev
```
This command loads the env vairables at runtime and publishes the app to port 5000.  It also uses a bind mount to link the container to the code in the IDE.  This allows any code changes to be hot loaded into the running flask app for instant viewing.  It can be accessed on [`http://localhost:5000/`](http://localhost:5000/).