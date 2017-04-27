#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"

import xmlrpclib
import argparse
from base64 import b64decode
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

class SecureXMLRPCServer(SimpleXMLRPCServer):

    def __init__(self, host, port, username, password, *args, **kargs):
        self.username = username
        self.password = password
        # authenticate method is called from inner class
        class VerifyingRequestHandler(SimpleXMLRPCRequestHandler):
            # method to override
            def parse_request(request):
                if SimpleXMLRPCRequestHandler.parse_request(request):
                    # authenticate
                    if self.authenticate(request.headers):
                        return True
                    else:
                        # if authentication fails return 401
                        request.send_error(401, 'Authentication failed, Try again.')
                return False
        # initialize
        SimpleXMLRPCServer.__init__(self, (host, port), requestHandler=VerifyingRequestHandler, *args, **kargs)

    def authenticate(self, headers):
        headers = headers.get('Authorization').split()
        basic, encoded = headers[0], headers[1]
        if basic != 'Basic':
            print 'Only basic anthentication supported'
            return False
        secret = b64decode(encoded).split(':')
        username, password = secret[0], secret[1]
        return True if (username==self.username and password==self.password) else False

def run_server(host, port, username, password):
    server = SecureXMLRPCServer(host, port, username, password)
    # simple test function
    def echo(msg):
        """Reply client in uppser case"""
        reply = msg.upper()
        print "Client said: %s. So we echo that in uppercase: %s" % (msg, reply)
        return reply
    server.register_function(echo, 'echo')
    print "Running a HTTP auth enabled XMLRPC server on %s:%s..." % (host, port)
    server.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Multithreaded multicall XMLRPCServer / Proxy')
    parser.add_argument('--host', action="store", dest="host", default='localhost')
    parser.add_argument('--port', action="store", dest="port", default=8003, type=int)
    parser.add_argument('--username', action="store", dest="username", default='user')
    parser.add_argument('--password', action="store", dest="password", default='pass')
    # parse arguments
    given_args = parser.parse_args()
    host, port = given_args.host, given_args.port
    username, password = given_args.username, given_args.password
    run_server(host, port, username, password)