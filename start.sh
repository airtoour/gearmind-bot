#!/bin/bash

until pg_isready -h db -U "${DB_USER}";
do sleep 1; done;
poetry run alembic upgrade head;
python src/main.py
