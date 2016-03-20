#!/usr/bin/env python

import xml.dom.minidom
import os

default_xml = "./default.xml"
dom = xml.dom.minidom.parse(default_xml)
manifest = dom.documentElement
projects = manifest.getElementsByTagName("project")
for project in projects:
    path = project.getAttribute("path")
    name = project.getAttribute("name")
#    print project
#    print path, name
    print "%s:%s" % (name, path)
