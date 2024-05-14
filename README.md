create venv

pip install -r requirements.txt

написание моделей данных (sqlalchemy/models)

alembic init migrations

alembic revision --autogenerate -m "Initial migration"

alembic upgrade head