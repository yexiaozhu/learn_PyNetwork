#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"

import argparse
import json
import urllib
import requests

# BASE_URL = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0'
BASE_URL = 'https://developers.google.com/custom-search/'

def get_search_url(query):
    return "%s&%s" %(BASE_URL, query)

def search_info(tag):
    query = urllib.urlencode({'q': tag})
    url = get_search_url(query)
    response = requests.get(url)
    print response
    results = response.json()
    print results

    data = results['responseData']
    print data
    print 'Found total results: %s ' % data['cursor']['estimatedResultCount']
    hits = data['results']
    print 'Found top %d hits:' % len(hits)
    for h in hits:
        print ' ', h['url']
    print 'More results avilable from %s' % data['cursor']['moreResultsUrl']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search info from Google')
    parser.add_argument('--tag', action="store", dest="tag", default='Python books')
    # parse arguments
    given_args = parser.parse_args()
    search_info(given_args)
