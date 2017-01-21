#!/usr/bin/env python3
#-*- coding=utf-8 -*-
#author="yexiaozhu"

import os
import argparse
import socket
import struct
import select
import time
import sys

ICMP_ECHO_REQUEST = 8 # Platform specific
DEFAULT_TIMEOUT = 2
DEFAULT_COUNT = 4

class Pinger(object):
    """ Pings to a host -- the Pythonic way """

    def __init__(self, target_host, count=DEFAULT_COUNT, timeout=DEFAULT_TIMEOUT):
        self.target_host = target_host
        self.count = count
        self.timeout = timeout

    def do_checksum(self, source_string):
        """ Verify the packet integritity"""
        sum = 0
        #print('source_string=', source_string)
        #print('source_string=', type(source_string))
        source_string = source_string.decode('utf-16')
        max_count = (len(source_string)/2)*2
        count = 0
        while count < max_count:
            val = ord(source_string[count + 1])*256 + ord(source_string[count]) # ord()返回字符串对应当ascii码
            sum = sum + val
            sum = sum & 0xffffffff # & 位运算 全部为1，结果为1
            count = count + 2

        if max_count<len(source_string):
            sum = sum + ord(source_string[len(source_string) - 1])
            sum = sum & 0xffffffff

        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16) # >>右移运算符 把>>左边运算数二进制全部右移若干位
        answer = ~sum # ～按位取反 对数据二进制取反 0变1 1变0
        answer = answer & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer

    def receive_ping(self, sock, ID, timeout):
        """ Receive ping from the socket."""
        time_remaining = timeout
        while True:
            start_time = time.time()
            readable = select.select([sock], [], [], time_remaining)
            time_spent = (time.time() - start_time)
            if readable[0] == []: # Timeout
                return
            time_received = time.time()
            recv_packet, addr = sock.recvfrom(1024)
            icmp_header = recv_packet[20:28]
            type, code, checksum, pack_ID, sequence = struct.unpack('bbHHh', icmp_header)
            print(type, code, checksum, pack_ID, sequence)
            if pack_ID == ID:
                bytes_In_double = struct.calcsize("d")
                time_sent = struct.unpack("d", recv_packet[28:28 + bytes_In_double])[0]
                return time_received - time_spent

            time_remaining = time_remaining - time_spent
            if time_remaining <= 0:
                return

    def send_ping(self, sock, ID):
        """ Send ping to the target host"""
        target_addr = socket.gethostbyname(self.target_host)

        my_checksum = 0

        # Create a dummy heder with a 0 checksum.
        #print(ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
        #print('header=', header)
        bytes_In_double = struct.calcsize('d')
        #print(bytes_In_double)
        data = (192 - bytes_In_double) * "Q"
        #print(type(data))
        #print('data=', data)
        #print('data1=', struct.pack("d", time.time()))
        data = struct.pack("d", time.time()) + data.encode(encoding='utf-8')
        #print('data2=', data)

        # Get the checksum
        my_checksum = self.do_checksum(header + data)
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1)
        packet = header + data
        sock.sendto(packet, (target_addr, 1))

    def ping_once(self):
        """ Returns the delay (in seconds) or none on timeout."""
        icmp = socket.getprotobyname("icmp")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except socket.error as e:
            (errno, msg) = e
            if errno == 1:
                # Not superuser, so operation not permitted
                msg += "ICMP messages can only be sent from root user processes"
                raise socket.error(msg)
        except Exception as e:
            print("Execption: %s" %(e))

        my_ID = os.getpid() & 0xFFFF
        print(sock, my_ID)
        self.send_ping(sock, my_ID)
        delay = self.receive_ping(sock, my_ID, self.timeout)
        sock.close()
        #print(delay)
        return delay

    def ping(self):
        """ Run the ping process"""
        for i in range(self.count):
            print("Ping to %s..." %self.target_host)
            try:
                delay = self.ping_once()
            except socket.gaierror as e:
                print("Pin failed. (socket error: '%s')" %e[1])
                break

            if delay == None:
                print("Ping failed. (timeout within % ssec.)" %self.timeout)
            else:
                delay = delay * 1000
                print("Get ping in %0.4fms" %delay)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python ping')
    parser.add_argument('--target-host', action="store", dest="target_host",
    required=True)
    given_args = parser.parse_args()
    target_host = given_args.target_host
    pinger = Pinger(target_host=target_host)
    pinger.ping()