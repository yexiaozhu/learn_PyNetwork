#!/usr/bin/env python
# coding=utf-8
# author=yexiaozhu

# Import modules for CGI handling
import cgi
import cgitb

# Create instance of FiledStorage
form = cgi.FieldStorage()

# Get data from files
name = form.getvalue('Name')
comment = form.getvalue('Comment')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>CGI Program Example </title>"
print "</head>"
print "<body>"
print "<h2> %s sends a comment: %s</h2>" %(name, comment)
print "</body>"
print "</html>"