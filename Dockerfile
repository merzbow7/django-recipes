FROM python:3.10
MAINTAINER Vladislav Moskvitin

ENV PYTHONUNBUFFERED 1

RUN mkdir /recipesBook
WORKDIR /recipesBook
COPY . /recipesBook

RUN pip3 install poetry

COPY run.sh /run.sh
RUN chmod +x /run.sh
ENTRYPOINT "/run.sh"
