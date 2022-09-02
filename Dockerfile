FROM python:3.7-buster as base

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1    
ENV PATH="$PATH:$POETRY_HOME/bin"
ENV PORT=80

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml ./

FROM base as production

RUN poetry install --no-dev

WORKDIR /app
COPY . /app

CMD poetry run gunicorn "todo_app.app:create_app()" --bind 0.0.0.0:$PORT

FROM base as development

RUN poetry install 

WORKDIR /app
COPY . /app

CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0" ]

FROM development as test

ENTRYPOINT [ "poetry", "run", "pytest" ]