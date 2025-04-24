FROM python:3.13-slim


RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app


COPY pyproject.toml poetry.lock ./


RUN poetry config virtualenvs.create false \
        && poetry install --no-interaction --no-ansi


COPY venv_addressbook/ ./venv_addressbook


CMD ["python", "/app/venv_addressbook/main.py"]
