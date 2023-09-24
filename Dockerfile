FROM python:3.11.4-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml ./
RUN pip3 install poetry
RUN apt-get update && \
    apt-get  -y install  libpq-dev gcc && \
    poetry install  && \
    apt-get -y remove libpq-dev gcc

COPY . .