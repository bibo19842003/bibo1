#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# http://python.jobbole.com/81359/

import urllib
import re
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read().decode('gbk')
#    print html
    return html


def getMmImg(mmhtml, foldername):
    reg = r'<img.*?src="(.*?)"'
    mmimgre = re.compile(reg, re.S)
    mmimglist = re.findall(mmimgre, mmhtml)
    x = 0
    for mmproject in mmimglist:
        mm = "https:" + mmproject.strip()
        print mm, foldername
        urllib.urlretrieve(mm, '%s/%s.jpg' % (foldername, x))
        x += 1


def getImg(html):
    reg = '<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>'
    imgre = re.compile(reg, re.S)
    imglist = re.findall(imgre, html)
    x = 0
    for project in imglist:
        print project[0], project[1], project[2], project[3], project[4]
        fo = open("menu.txt", "a+")
        content = project[0] + " " + project[1] + " " + project[2] + " " + project[3] + " " + project[4] + "\n"
        fo.write(content)
        fo.close()

        foldername = project[2].strip()
        isExists = os.path.exists(foldername)
        if not isExists:
            os.makedirs(foldername)

        mmurl = "https:" + project[0]
        mmhtml = getHtml(mmurl)

        getMmImg(mmhtml, foldername)


n = 7
for num in range(4, n):
    url = "https://mm.taobao.com/json/request_top_list.htm" + "?page=" + str(num)
    html = getHtml(url)
    getImg(html)
