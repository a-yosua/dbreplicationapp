# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/

COPY installmsodbcdriver17.sh /code/
RUN chmod +x installmsodbcdriver17.sh
RUN ./installmsodbcdriver17.sh

RUN pip install -r requirements.txt
COPY . /code/
