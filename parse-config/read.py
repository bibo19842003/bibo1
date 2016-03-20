#!/usr/bin/env python

import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("config")
# return all section
secs = cf.sections()
print 'sections:', secs

opts = cf.options("account")
print 'options:', opts

kvs = cf.items("account")
print 'account:', kvs

# read by type
username = cf.get("account", "username")
password = cf.get("account", "password")

print "username:", username
print "password:", password
