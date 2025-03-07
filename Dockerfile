FROM python:3.12.0-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update -y && \
    apt install -y python3-dev postgresql-client && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod +x /app/start.sh

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && \
    pip install poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . .

ENV PYTHONPATH="/app/src"
