FROM python:3.9.13-buster

ARG WORKER_COUNT=1
ENV WORKER_COUNT=${WORKER_COUNT}

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
ENTRYPOINT python server.py