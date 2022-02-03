# syntax=docker/dockerfile:1
FROM python:3.10.2-slim
RUN apt-get -yqq update
WORKDIR /app
ADD . /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD python3 main.py
