FROM ubuntu:16.04

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y python3 python3-pip docker.io

RUN pip3 install docker

WORKDIR /

COPY ./start.sh /start.sh
COPY ./entry.py /entry.py

RUN chmod +x /start.sh

ARG REMOTE_PORT
ARG CLIENT_POR
ARG IMAGE
ARG DOCKER_NET
EXPOSE $REMOTE_PORT

CMD ["/start.sh"]
