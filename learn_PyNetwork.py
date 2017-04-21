#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"
import base64
import urllib2

SEARCH_URL_BASE = 'https://api.github.com/repos'

import argparse
import requests
import json

def search_repository(author, repo, search_for='homepage'):
    url = "%s/%s/%s" %(SEARCH_URL_BASE, author, repo)
    token = "19c2cfeb60881c3640791584df8443472fb0615f"
    password = "x-oauth-basic"
    print "Searching Repo URL: %s" %url
    result = urllib2.Request(url)
    result.add_header("Authorization", "Basic " + base64.urlsafe_b64encode("%s:%s" % (token, password)))
    result.add_header("Content-Type", "application/json")
    result.add_header("Accept", "application/json")
    result = urllib2.urlopen(result)
    result = result.read()
    # print result
    if(result):
        repo_info = json.loads(result)
        print "Github repository info for: %s" %repo
        result = "No result found!"
        keys = []
        for key, value in repo_info.iteritems():
            if search_for in key:
                result = value
        return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Github search')
    parser.add_argument('--author', action="store", dest="author", required=True)
    parser.add_argument('--repo', action="store", dest="repo", required=True)
    parser.add_argument('--search_for', action="store", dest="search_for", required=True)
    given_args = parser.parse_args()
    result = search_repository(given_args.author, given_args.repo, given_args.search_for)

    if isinstance(result, dict):
        print "Got result for '%s'..." %(given_args.search_for)
        for key,value in result.iteritems():
            print "%s => %s" %(key,value)
    else:
        print "Got result for %s: %s" %(given_args.search_for, result)