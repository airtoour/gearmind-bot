#!/bin/bash

until pg_isready -h db -U "${DB_USER}";
do sleep 1; done;
poetry run alembic upgrade head;

gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
