#!/usr/bin/env python3
#-*- coding=utf-8 -*-
#author="yexiaozhu"

import socket
import argparse
import netifaces as ni
import netaddr as na

def extract_ipv6_info():
    """ Extracts IPv6 information"""
    print "IPV6 support built into Python: %s" %socket.has_ipv6
    for interface in ni.interfaces():
        all_addresses = ni.ifaddresses(interface)
        print "Interface %s:" %interface
        for family,addrs in all_addresses.iteritems():
            fam_name = ni.address_families[family]
            print 'Address family: %s' %fam_name
            for addr in addrs:
                if fam_name == 'AF_INET6':
                    addr = addr['addr']
                    has_eth_string = addr.split("%eth")
                    if has_eth_string:
                        addr = addr.split("%ens")[0]
                        # addr = addr.split("%eth")[0]
                        # print '1', addr
                    print "    IP Address: %s" %na.IPNetwork(addr)
                    print "    IP Version: %s" %na.IPNetwork(addr).version
                    print "    IP Prefix length: %s" %na.IPNetwork(addr).prefixlen
                    print "    Network: %s" %na.IPNetwork(addr).network
                    print "    Broadcast: %s" %na.IPNetwork(addr).broadcast

if __name__ == '__main__':
    extract_ipv6_info()