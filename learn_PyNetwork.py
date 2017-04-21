#!/usr/bin/env python2.7.12
#coding=utf-8
#author="yexiaozhu"

from getpass import getpass
from fabric.api import settings, run, env, prompt, cd

def remote_server():
    # Edit this list to include remote hosts
    env.hosts = ['127.0.0.1']
    env.user = prompt('Enter user name: ')
    env.password = getpass('Enter password: ')
    env.mysqlhost = 'localhost'
    env.mysqluser = prompt('Enter your db username: ')
    env.mysqlpassword = getpass('Enter your db user password: ')
    env.db_name = ''

def show_dbs():
    """ Wraps mysql show databases cmd"""
    q = "show databases"
    run("echo '%s' | mysql -u%s -p%s" %(q, env.mysqluser, env.mysqlpassword))

def run_sql(db_name, query):
    """ Generic function to run sql"""
    with cd('/home/yezi10'):
        run("echo '%s' | mysql -u%s -p%s -D%s" %(query, env.mysqluser, env.mysqlpassword, db_name))

def create_db():
    """Create a MYSQL DB for App version"""
    if not env.db_name:
        db_name = prompt("Enter the DB name:")
    else:
        db_name = env.db_name
    run('echo "CREATE DATABASE %s default character set utf8 collate utf8_unicode_ci;"|mysql --batch --user=%s --password=%s --host=%s'\
        % (db_name, env.mysqluser, env.mysqlpassword, env.mysqlhost), pty=True)

def ls_db():
    """ List a dbs with size in MB"""
    if not env.db_name:
        db_name = prompt("Which DB to ls?")
    else:
        db_name = env.db_name
    query = """SELECT table_schema "DB Name",
        Round(Sum(data_length + index_length) / 1024 / 1024, 1) "DB Size in MB"
        FROM information_schema.tables
        WHERE table_schema = \"%s\"
        GROUP BY table_schema """ %db_name
    run_sql(db_name, query)

def empty_db():
    """Empty all tables of a given DB """
    db_name = prompt("Enter DB name to empty:")
    cmd = """
    (echo 'SET foreign_key_checks = 0;';
    (mysqldump -u%s -p%s --add-drop-table --no-data %s |
    grep ^DROP);
    echo 'SET foreign_key_checks = 1;') | \
    mysql -u%s -p%s -b %s"""%(env.mysqluser, env.mysqlpassword, db_name, env.mysqluser, env.mysqlpassword, db_name)
    run(cmd)