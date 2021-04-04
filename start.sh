#!/bin/sh
# Add your startup script
# systemctl start docker
# cd /home/ctf/image
# docker build -t image .
python3 /entry.py $REMOTE_PORT $CLIENT_PORT $IMAGE $DOCKER_NET

# DO NOT DELETE
/etc/init.d/xinetd start;
sleep infinity;
