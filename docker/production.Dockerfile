FROM python:3.11

ENV PYTHONUNBUFFERED 1

ARG APP_DIR=/app

WORKDIR $APP_DIR

ADD ./ $APP_DIR

RUN apt-get update -y && \
    apt-get install --no-install-recommends -y  \
    nano  && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
