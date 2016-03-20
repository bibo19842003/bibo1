#!/usr/bin/env python

import ConfigParser

cf = ConfigParser.ConfigParser()

cf.add_section("db")
cf.set("db", "db_pass", "xgmtest")
cf.set("db", "db_user", "qqq")
cf.write(open("conf2", "w"))

secs = cf.sections()
print 'sections:', secs

opts = cf.options("db")
print 'options:', opts

kvs = cf.items("db")
print 'account:', kvs
