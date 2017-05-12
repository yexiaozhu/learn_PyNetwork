#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"

import os
from scapy import *
from scapy.all import *
def modify_packet_header(pkt):
    """ Parse the header and add an extra header"""
    if pkt.haslayer(TCP) and pkt.getlayer(TCP).dport == 80 and pkt.haslayer(Raw):
        # print 1
        print 'pkt:', pkt
    #     hdr = pkt[TCP].payload
    #     hdr.__dict__
    #     print type(hdr)
    #     extra_item = {'Extra Header': ' extra value'}
    #     hdr.update(extra_item)
    #     send_hdr = '\r\n'.join(hdr)
    #     # print 'send_hdr:', send_hdr
    #     pkt[TCP].payload = send_hdr

        pkt.show()

        del pkt[IP].chksum
        send(pkt)
    # else:
    #     print 2

if __name__ == '__main__':
    # start sniffing
    sniff(filter="tcp and ( port 80 )", prn=modify_packet_header)