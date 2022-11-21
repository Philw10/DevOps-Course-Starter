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
This command loads the env vairables at runtime and publishes the app to port 5000.  It also uses a bind mount to link the container to the application code in the local todo_app directory.  This allows any code changes to be hot loaded into the running flask app for instant viewing.  It can be accessed on [`http://localhost:5000/`](http://localhost:5000/).

## Testing though Docker

The unit and integration tests can also be run through Docker.

The test image can be built with the following command:

```bash
docker build --target test --tag to-do-test-image .
```

The tests can then be run using the following:

```bash
docker run --env-file .env.test to-do-test-image
```
The Docker test uses the .env.test file in place of any secret environment variables.

## Azure

They app is now deployed to Azure via a GitHub action CI/CD pipeline

The app can be accessed on the following link:

```bash
https://philstodoapp.azurewebsites.net
```

## Mongo DB

The app uses a mongo document store database to store all of the to do items.

To configure your own to use with the app you will need to update the env file with your mongo connection string, database name, and collection name.

## Oauth authentication

The app uses GitHub authentication to log in.  

When you have logged in a secure cookie will be added to the users browser to store the session.

Once oAuth has been set up in GitHub the provided ID and Secret can be added to the env file.

## Authorisation

Only accounts given admin access will be able to edit the list.  This is done by adding the users GitHub ID to the .env file.  

All other users will have read only access.