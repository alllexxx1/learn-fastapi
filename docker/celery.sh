#!bin/bash

if [["${1}" == "celery"]]; then
  celery --app=hotels_app.tasks.celery_app:celery_app worker --loglevel=INFO
elif [["${1}" == "flower"]]; then
  celery --app=hotels_app.tasks.celery_app:celery_app flower
fi
