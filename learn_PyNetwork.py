#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"

import urllib

URL = 'https://www.github.com'
PROXY_ADDRESS = "165.24.10.8:8080" # BY Googling free proxy server

if __name__ == '__main__':
    resp = urllib.urlopen(URL, proxies= {"http" : PROXY_ADDRESS})
    print "Proxy server returns response headers: %s" %resp.headers