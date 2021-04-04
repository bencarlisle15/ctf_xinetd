FROM ubuntu:16.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd python3 python3-pip docker.io

RUN pip3 install docker

WORKDIR /

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh
COPY ./entry.py /entry.py
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh

ARG REMOTE_PORT
ARG CLIENT_POR
ARG IMAGE
ARG DOCKER_NET
EXPOSE $REMOTE_PORT

CMD ["/start.sh"]
