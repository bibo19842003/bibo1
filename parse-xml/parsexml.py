#!/usr/bin/env python

import xml.dom.minidom
import os

default_xml = "./default.xml"
dom = xml.dom.minidom.parse(default_xml)
manifest = dom.documentElement

defaultproject = manifest.getElementsByTagName("default")[0]
defaultrevision = defaultproject.getAttribute("revision")
defaultremote = defaultproject.getAttribute("remote")

projects = manifest.getElementsByTagName("project")
for project in projects:
    name = project.getAttribute("name")

    if project.getAttribute("path"):
        path = project.getAttribute("path")
    else:
        path = name

    if project.getAttribute("revision"):
        newrevision = project.getAttribute("revision")
    else:
        newrevision = defaultrevision

    if project.getAttribute("origin"):
        newremorte = project.getAttribute("origin")
    else:
        newremote = defaultremote

    print "%s:%s:%s:%s" % (name, path, newrevision, newremote)
