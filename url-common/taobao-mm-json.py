#!/usr/bin/env python

# http://python.jobbole.com/81359/

import urllib
import re


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read().decode('gbk')
#    print html
    return html


def getImg(html):
    reg = '<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>'
    imgre = re.compile(reg, re.S)
    imglist = re.findall(imgre, html)
    x = 0
    for project in imglist:
        print project[0], project[1], project[2], project[3]



html = getHtml("https://mm.taobao.com/json/request_top_list.htm")
getImg(html)
