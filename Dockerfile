FROM python:3.10
MAINTAINER Vladislav Moskvitin

ENV PYTHONUNBUFFERED 1

RUN mkdir /recipesBook
WORKDIR /recipesBook
COPY . /recipesBook

RUN python3 -m pip install --upgrade pip
RUN pip3 install poetry

COPY run.sh /run.sh
RUN chmod +x /run.sh

RUN adduser --disabled-password --gecos '' python
RUN adduser python sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER python

ENTRYPOINT "/run.sh"
