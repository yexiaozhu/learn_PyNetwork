#!/usr/bin/env python3
#coding=utf-8
#author="yexiaozhu"
import ntplib
from time import ctime

def print_time():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('europe.pool.ntp.org', version=3)
    print(ctime(response.tx_time))

if __name__ == '__main__':
    print_time()