# BASIC INSTALL
FROM python:3.11-buster
RUN apt-get update -qq
RUN apt-get install pulseaudio libasound2-dev ffmpeg -qq
RUN apt-get install nano
RUN pip install --upgrade pip


RUN mkdir /app
WORKDIR /app

COPY ./app/requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /app/requirements.txt

COPY ./app /app

RUN adduser cgpt-user
USER cgpt-user
