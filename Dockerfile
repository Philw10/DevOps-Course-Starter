FROM python:3.7-buster as base

ENV PATH="/root/.poetry/bin:$PATH"
ENV PORT=80


RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false

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