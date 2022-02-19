FROM python:3.10
MAINTAINER Vladislav Moskvitin

ENV PYTHONUNBUFFERED 1

RUN mkdir /recipesBook
WORKDIR /recipesBook
COPY . /recipesBook

RUN pip3 install poetry

RUN chmod +x /recipesBook/run.sh

RUN adduser --disabled-password --gecos '' python
RUN adduser python sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER python


