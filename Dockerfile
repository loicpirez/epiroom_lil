FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /src
WORKDIR /src
ADD requirements.txt /src
ADD . /src