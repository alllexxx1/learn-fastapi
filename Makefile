init-migration:
	alembic init migrations

make-migration:
	alembic revision --autogenerate -m ''

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1