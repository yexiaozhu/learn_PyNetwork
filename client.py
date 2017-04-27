import argparse
import xmlrpclib

def run_client(host, port, username, password):
    server = xmlrpclib.ServerProxy('http://%s:%s@%s:%s' %(username, password, host, port, ))
    msg = "hello server..."
    print "Sending message to server: %s " %msg
    print "Got reply: %s" %server.echo(msg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Multithreaded multicall XMLRPC Server/Proxy')
    parser.add_argument('--host', action="store", dest="host", default='localhost')
    parser.add_argument('--port', action="store", dest="port", default=8003, type=int)
    parser.add_argument('--username', action="store", dest="username", default='user')
    parser.add_argument('--password', action="store", dest="password", default='pass')
    # parse arguments
    given_args = parser.parse_args()
    host, port = given_args.host, given_args.port
    username, password = given_args.username, given_args.password
    run_client(host, port, username, password)