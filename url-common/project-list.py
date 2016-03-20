#!/usr/bin/env python

import urllib
import re


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


def getImg(html):
    reg = r"a title='(.+?)' href="
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    for project in imglist:
        print project


html = getHtml("https://us.codeaurora.org/cgit/quic/gerrit4msm")
getImg(html)
