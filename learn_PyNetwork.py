#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"

from pygeocoder import Geocoder

def search_business(business_name):
    results = Geocoder.geocode(business_name)
    # print results
    # print results[0].coordinates
    for result in results:
        print result

if __name__ == '__main__':
    business_name = "Tian'anmen, Beijing"
    print "Searching %s" %business_name
    search_business(business_name)