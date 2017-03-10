#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"

import cookielib
import urllib
import urllib2

ID_USERNAME = 'id_username'
ID_PASSWORD = 'id_password'
USERNAME = '557703988@139.com'
PASSWORD = 'wang051206git'
LOGIN_URL = 'https://github.com/login'
NORMAL_URL = 'https://github.com/'
headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'
        }
def extract_cookie_info():
    """ Fake login to a site with cookie """
    # setuo cookie jar
    cj = cookielib.CookieJar()
    # print cj
    login_data = urllib.urlencode({ID_USERNAME: USERNAME,
                                   ID_PASSWORD: PASSWORD})
    # create url opener
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # opener.addheaders = headers
    # urllib2.install_opener(opener)
    # opener = urllib2.build_opener(headers)
    # urllib2.install_opener(opener)
    # resp = opener.open(LOGIN_URL, login_data)
    resp = urllib2.Request(LOGIN_URL, login_data, headers)

    # send login info
    for cookie in cj:
        print "----First time cookie: %s --> %s" %(cookie.name, cookie.value)

    print "Headers: %s" %resp.headers

    # now acess without any login info
    resp = opener.open(NORMAL_URL)
    for cookie in cj:
        print "++++Second time cookie: %s --> %s" %(cookie.name, cookie.value)

    print "Header: %s" %resp.headers

if __name__ == '__main__':
    extract_cookie_info()