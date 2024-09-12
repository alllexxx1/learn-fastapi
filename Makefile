init-migrations:
	alembic init migrations

make-migrations:
	alembic revision --autogenerate -m ''

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1