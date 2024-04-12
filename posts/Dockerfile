# pull official base image
FROM python:3.8.10-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set superuser credentials
ENV DJANGO_SUPERUSER_USERNAME admin
ENV DJANGO_SUPERUSER_EMAIL hirvahapjh@gmail.com
ENV DJANGO_SUPERUSER_PASSWORD Duss1256!@

COPY . /usr/src/app

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt