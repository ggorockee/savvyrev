alembic revision --autogenerate -m "Create users table"
alembic upgrade head

alembic revision --autogenerate -m "Add full_name to User model"
alembic upgrade head
