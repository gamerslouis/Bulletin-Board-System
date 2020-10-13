import sys
import boto3
import re
import socket
from client import Client


if __name__ == "__main__":
    try:
        ip = sys.argv[1]
        assert re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip), 'Invalid ip address'
        port = int(sys.argv[2])
        assert port >= 1 and port <= 65536, 'port number can only between 1 and 65536'
    except (ValueError, IndexError):
        print('Usage: {} [IP] [Port]'.format(sys.argv[0]), file=sys.stderr)
        exit(1)

    s3 = boto3.resource('s3')
    try:
        sock = socket.socket()
        sock.connect((ip, port))
    except Exception:
        print('Server connection error')
        exec(1)

    Client(sock, s3).exec()
