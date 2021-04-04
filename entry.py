import socket
import sys
import docker
import time
import select
from threading import Thread

BUF_SIZE = 1024

HOST = "0.0.0.0"
REMOTE_PORT = int(sys.argv[1])
CLIENT_PORT = int(sys.argv[2])

IMAGE = sys.argv[3]

DOCKER_NET = sys.argv[4]

IP_LOOKUP = {}

def create_new_container(client, remote_ip):
    container = client.containers.run(
        IMAGE,
        network=DOCKER_NET,
        detach=True
    )
    container_id = container.attrs["Id"]
    IP_LOOKUP[remote_ip] = container_id
    return container_id

def get_container_ip(remote_ip):
    client = docker.from_env()
    if remote_ip not in IP_LOOKUP:
        container_id = create_new_container(client, remote_ip)
    else:
        container_id = IP_LOOKUP[remote_ip]
        try:
            container = client.containers.get(container_id)
        except docker.errors.NotFound:
            container_id = create_new_container(client, remote_ip)
    print("Container: " + container_id)
    for _ in range(30):
        container = client.containers.get(container_id)
        ip = container.attrs["NetworkSettings"]["Networks"][DOCKER_NET]["IPAddress"]
        if ip != "":
            return ip
        time.sleep(1)
    return None


def connection(remote_conn, remote_ip):
    ip = get_container_ip(remote_ip)
    if ip is None:
        return
    with remote_conn:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_conn:
            print("Connecting to client %s:%d" % (ip, CLIENT_PORT))
            for _ in range(30):
                try:
                    client_conn.connect((ip, CLIENT_PORT))
                    break
                except:
                    time.sleep(1)
            remote_conn.setblocking(0)
            client_conn.setblocking(0)

            sockets = [remote_conn, client_conn]

            while True:
                readable, writable, exceptional = select.select(sockets, sockets, sockets)
                for readable_sock in readable:
                    data = readable_sock.recv(BUF_SIZE)
                    if readable_sock is remote_conn:
                        client_conn.send(data)
                    else:
                        remote_conn.send(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, REMOTE_PORT))
    s.listen()
    print("Started server: %s:%d" % (HOST, REMOTE_PORT))
    while True:
        conn, (remote_ip, remote_port) = s.accept()
        print("Received connection from %s:%d" % (remote_ip, remote_port))
        Thread(target=connection, args=[conn, remote_ip]).start()
