#!/usr/bin/env python

import urllib
import re


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
#    print html
    return html


def getImg(html):
    reg = r'data-ks-lazyload="(https:\/\/img\.alicdn\.com\/imgextra.+?.jpg)" alt='
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    x = 0
    for project in imglist:
        print project
        urllib.urlretrieve(project,'%s.jpg' % x)
        x+=1


html = getHtml("https://mm.taobao.com")
getImg(html)
