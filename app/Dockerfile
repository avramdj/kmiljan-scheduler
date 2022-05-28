FROM python:3.9.13-buster

ARG WORKER_COUNT=1
ENV WORKER_COUNT=${WORKER_COUNT}

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn -w $WORKER_COUNT --bind=0.0.0.0:3333 --log-level=debug wsgi:app 