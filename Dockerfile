FROM python:3.11-alpine
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED 1
