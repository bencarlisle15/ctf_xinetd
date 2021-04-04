#!/bin/sh
python3 /entry.py $REMOTE_PORT $CLIENT_PORT $IMAGE $DOCKER_NET

# DO NOT DELETE
/etc/init.d/xinetd start;
sleep infinity;
