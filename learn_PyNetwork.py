#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"

import requests
import urllib
import urllib2

ID_MOBILEPHONE = 'id_mobilePhone'
ID_EMAIL = 'id_Email'
ID_PASSWORD = 'id_Password'
ID_RELOAD_PASSWORD = 'id_reload_Password'
MOBILEPHONE = 'XXXXXX'
# USERNAME = 'XXXXXX'
EMAIL = 'XXXXXX'
PASSWORD = 'XXXXXX'
SIGUP_URL = 'https://accounts.ctrip.com/member/regist/register.aspx'

def submit_form():
    """ Submit a from """
    payload = {ID_MOBILEPHONE : MOBILEPHONE,
               ID_EMAIL : EMAIL,
               ID_PASSWORD : PASSWORD,
               ID_RELOAD_PASSWORD : PASSWORD}

    # make a get request
    resp = requests.get(SIGUP_URL)
    print "Response to GET request: %s" %resp.content

    # send POST request
    resp = requests.post(SIGUP_URL, payload)
    print "Headers from a POST request response: %s" %resp.headers
    # print "HTML Response: %s" %resp.read()

if __name__ == '__main__':
    submit_form()
