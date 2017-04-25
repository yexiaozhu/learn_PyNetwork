#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"

from getpass import getpass
from fabric.api import settings, run, env, prompt, put, sudo
from fabric.contrib.files import exists

WWW_DOC_ROOT = "/data/apache/test/"
WWW_USER = "www-data"
WWW_GROUP = "www-data"
APACHE_SITES_PATH = "/etc/apache2/sites-enabled"
APACHE_INIT_SCRIPT = "etc/init.d/apache2"

def remote_server():
    env.hosts = ['127.0.0.1']
    env.user = prompt('Enter user name: ')
    env.password = getpass('Enter your system password: ')

def setup_vhost():
    """ Setup a test website """
    print "Preparing the Apache vhost setup..."

    print "Setting up the document root..."
    if exists(WWW_DOC_ROOT):
        sudo("rm -rf %s" %WWW_DOC_ROOT)
    sudo("mkdir -p %s" %WWW_DOC_ROOT)

    # setup file permissions
    sudo("chown -R %s.%s %s" %(env.user, env.user, WWW_DOC_ROOT))

    # upload a sample index.html file
    put(local_path="index.html", remote_path=WWW_DOC_ROOT)
    sudo("chown -R %s.%s %s" %(WWW_USER, WWW_GROUP, WWW_DOC_ROOT))

    print "Setting up the vhost..."
    sudo("chown -R %s.%s %s" %(env.user, env.user, APACHE_SITES_PATH))

    # upload a pre-configured vhost.conf
    put(local_path="vhost.conf", remote_path=APACHE_SITES_PATH)
    sudo("chown -R %s.%s %s" % ('root', 'root', APACHE_SITES_PATH))

    # restart Apache to take effect
    sudo("service apache2 restart")
    print "Setup complete. Now open the server path http://localhost/ in your web browser"
