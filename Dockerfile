FROM python:3.7-buster as base

ENV PYTHONFAULTHANDLER=1 \
PYTHONUNBUFFERED=1 \
PYTHONHASHSEED=random \
PIP_NO_CACHE_DIR=off \
PIP_DISABLE_PIP_VERSION_CHECK=on \
PIP_DEFAULT_TIMEOUT=100 \
PATH="/root/.poetry/bin:$PATH" 

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false

FROM base as production

RUN poetry install --no-dev

WORKDIR /app
COPY . /app

CMD [ "gunicorn", "todo_app.app:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:80" ]

FROM base as development

RUN poetry install 

WORKDIR /app
COPY . /app

CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0" ]