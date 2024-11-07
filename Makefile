init-migration:
	alembic init migrations

make-migration:
	alembic revision --autogenerate -m ''

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1

celery-up:
	celery -A hotels_app.tasks.celery_app:celery_app worker --loglevel=INFO

flower-celery-up:
	celery -A hotels_app.tasks.celery_app:celery_app flowerr
