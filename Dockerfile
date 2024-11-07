FROM python:3.11

WORKDIR /app

COPY pyproject.toml .

RUN pip install "poetry==1.8.3"
RUN poetry config virtualenvs.create false
RUN poetry config installer.max-workers 1
RUN poetry install

COPY . .

# Allow container to run bash sripts
#RUN chmod a+x /app/docker/*.sh

# Run(apply) migrations
RUN alembic upgrade head

CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
