from celery import Celery

from config import settings

celery_app = Celery(
    'tasks',
    broker=settings.REDIS_URL,
    include=['hotels_app.tasks.tasks']
)

celery_app.conf.broker_connection_retry_on_startup = True
