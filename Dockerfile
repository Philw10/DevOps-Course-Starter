FROM python:3.7-buster

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

RUN poetry install --no-dev

WORKDIR /
COPY . .

CMD [ "gunicorn", "todo_app.app:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:80" ]

