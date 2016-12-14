#!/usr/bin/env python3
#coding=utf-8
#author="yexiaozhu"
import argparse
import socket
host = 'localhost'
def echo_client(port):
    """ A simple echo server"""
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    server_address = (host, port)
    print("Connecting to %s port %s" % server_address)
    sock.connect(server_address)

    # Send data
    try:
        message = "Test message. This will be echoed"
        print("Sending %s" %message)
        sock.sendall(message.encode(encoding='utf-8'))
        # Look for the response
        amount_received = 0
        amount_excepted = len(message)
        while amount_received < amount_excepted:
            data = sock.recv(16)
            amount_received += len(data)
            print("Received: %s" %data)
    except socket.error as err:
        print("Socket error: %s" %str(err))
    except Exception as e:
        print("Other exception: %s" %str(e))
    finally:
        print("Closing connection to the server")
        sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_client(port)