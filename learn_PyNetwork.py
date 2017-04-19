#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"

import argparse
import urllib
import re
from datetime import datetime

# SEARCH_URL = 'http://finance.google.com/finance?q='
SEARCH_URL = 'https://gupiao.baidu.com/stock/us%s.html'

def get_quote(symbol):
    # print SEARCH_URL + symbol
    url = SEARCH_URL % symbol
    print url
    content = urllib.urlopen(url).read()
    # print content
    m = re.search('class="_close".*?>(.*?)<', content)
    if m:
        quote = m.group(1)
    else:
        quote = 'No quote available for: ' + symbol
    return quote

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stock quote search')
    parser.add_argument('--symbol', action="store", dest="symbol", required=True)
    given_args = parser.parse_args()
    print "Searching stock quote for symbol '%s'" % given_args.symbol
    print "Stock quote for %s at %s: %s" % (given_args.symbol, datetime.today(), get_quote(given_args.symbol))