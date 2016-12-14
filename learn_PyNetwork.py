#!/usr/bin/env python3
#coding=utf-8
#author="yexiaozhu"
import os
import socket
import socketserver
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 0 # tells the kernel to pick up a port dynamically
BUF_SIZE = 1024
ECHO_MSG = 'Hello echo server!'

class ForkingClient():
    """A client to tes forking server"""
    def __init__(self, ip, port):
        # Create a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connection to the server
        self.sock.connect((ip, port))

    def run(self):
        """ Client playing with the server"""
        # Send the data to server
        current_process_id = os.getpid()
        print("PID %s Sending echo message to server : %s" %(current_process_id, ECHO_MSG))
        send_data_length = self.sock.send(ECHO_MSG.encode(encoding='utf-8'))
        print("Sent: %d characters, so far..." %send_data_length)

        # Display server response
        response = self.sock.recv(BUF_SIZE)
        response = response.decode('utf-8')
        print("PID %s received: %s" %(current_process_id, response[5:]))

    def shutdown(self):
        """ Cleanup the client socket """
        self.sock.close()

class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Send the echo back to the client
        data = self.request.recv(BUF_SIZE)
        data = data.decode('utf-8')
        current_process_id = os.getpid()
        response = "%s: %s" %(current_process_id, data)
        print("Server sending response [current_process_id: data] = [%s]" %response)
        self.request.send(response.encode(encoding='utf-8'))
        return

class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    """Nothing to add here, inherited everything necessary from parents"""
    pass

def main():
    # Launch the server
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    ip, port = server.server_address # Retrieve the port number
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True) # don't hang on exit
    server_thread.start()
    print("Server loop running PID: %s" %os.getpid())

    # Launch the client(s)
    client1 = ForkingClient(ip, port)
    client1.run()

    client2 = ForkingClient(ip, port)
    client2.run()
    # Clean them up
    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    server.socket.close()

if __name__ == '__main__':
    main()