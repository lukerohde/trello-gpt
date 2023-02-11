FROM python:3.11-buster
RUN apt-get update -qq
RUN apt-get install -qq python3-pip 
RUN apt-get install -qq nano pulseaudio libasound2-dev ffmpeg

RUN adduser pyuser
USER pyuser
ENV PATH=/home/pyuser/.local/bin:"$PATH"

RUN mkdir /home/pyuser/app
WORKDIR /home/pyuser/app

COPY ./app/requirements.txt /home/pyuser/app/requirements.txt
RUN --mount=type=cache,target=/home/pyuser/.cache/pip pip install --user -r ./requirements.txt

COPY ./app /home/pyuser/app
