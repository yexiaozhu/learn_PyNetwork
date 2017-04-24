#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"

from getpass import getpass
from fabric.api import settings, run, env, prompt, cd, open_shell, local, get, put

def remote_server():
    env.hosts = ['127.0.0.1']
    env.password = getpass('Enter your system password: ')
    env.home_folder = '/tmp'

def login():
    open_shell(command="cd %s" %env.home_folder)

def download_file():
    print "Checking local disk space..."
    local("df -h")
    remote_path = prompt("Enter the remote file path:")
    local_path = prompt("Enter the local file path:")
    get(remote_path=remote_path, local_path=local_path)
    local("ls %s" %local_path)

def upload_file():
    print "Checking remote disk space..."
    run("df -h")
    local_path = prompt("Enter the remote file path:")
    remote_path = prompt("Enter the local file path:")
    put(remote_path=remote_path, local_path=local_path)
    run("ls %s" %remote_path)
