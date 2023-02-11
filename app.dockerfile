# BASIC INSTALL
FROM python:3.11-buster
RUN apt-get update -qq
RUN apt-get install pulseaudio libasound2-dev ffmpeg -qq
RUN apt-get install nano
RUN python -m ensurepip --upgrade

RUN mkdir /app
WORKDIR /app
COPY ./app /app

