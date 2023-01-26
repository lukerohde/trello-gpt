# BASIC INSTALL
FROM python:3.11-buster
RUN apt-get update -qq

python -m ensurepip --upgrade

RUN mkdir /app
WORKDIR /app
COPY ./app /app
