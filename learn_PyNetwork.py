#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"

import getpass
import argparse
import paramiko

SOURCE = 'learn_PyNetwork.py'
DESTINATION = '/home/yezi10/learn_PyNetwork.py'

def copy_file(hostname, port, username, password, src, dst):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    print "Connecting to %s \n with username=%s... \n" %(hostname, username)
    print port
    t = paramiko.Transport((hostname, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    print "Copying file:%s to path: %s" %(src, dst)
    sftp.put(src, dst)
    sftp.close()
    t.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remote file copy')
    parser.add_argument('--host', action="store", dest="host", default='localhost')
    parser.add_argument('--port', action="store", dest="port", default=22, type=int)
    parser.add_argument('--src', action="store", dest="src", default=SOURCE)
    parser.add_argument('--dst', action="store", dest="dst", default=DESTINATION)
    given_args = parser.parse_args()
    hostname, port = given_args.host, given_args.port
    src, dst = given_args.src, given_args.dst
    username = raw_input("Enter the username:")
    password = getpass.getpass("Enter password for %s: " % username)
    copy_file(hostname, port, username, password, src, dst)