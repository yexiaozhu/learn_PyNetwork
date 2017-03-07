#!/usr/bin/env python3
#coding=utf-8
#author="yexiaozhu"

import socket
import sys
import argparse

HOST = 'localhost'
BUFSIZE = 1024

def ipv6_echo_client(port, host=HOST):
    for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            sock = socket.socket(af, socktype, proto)
        except socket.error, err:
            print "Error:%s" %err
        try:
            sock.connect(sa)
        except socket.error, msg:
            sock.close()
            continue
    if sock is None:
        print  'Failed to open socktt!'
        sys.exit(1)
    msg = "Hello from ipv6 client"
    print "Send data to server: %s" %msg
    sock.send(msg)
    while True:
        data = sock.recv(BUFSIZE)
        print 'Received from server', repr(data)
        if not data:
            break
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IPv6 socket client example')
    parser.add_argument('--port', action="store", dest="port", type=int,required=True)
    given_args = parser.parse_args()
    port = given_args.port
    ipv6_echo_client(port)


if __name__ == '__main__':
    run_unix_domain_socket_client()