FROM python:3.9-slim

WORKDIR /usr/src/dock/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt install gcc -y

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/dock/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/dock