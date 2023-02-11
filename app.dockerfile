FROM python:3.11-buster
RUN apt-get update -qq
RUN apt-get install -qq python3-pip 
RUN apt-get install -qq nano pulseaudio libasound2-dev ffmpeg

RUN adduser pyuser
USER pyuser
ENV PATH=/home/pyuser/.local/bin:"$PATH"

RUN mkdir /home/pyuser/app
WORKDIR /home/pyuser/app
COPY ./app /home/pyuser/app
RUN pip install --user -r ./requirements.txt

