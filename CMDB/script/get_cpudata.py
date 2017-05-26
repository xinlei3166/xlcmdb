#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import psutil
import time
import urllib, urllib2

while True:
    cpu_data = psutil.cpu_times()
    new_time = time.strftime("%Y-%m-%d %X", time.localtime())

    data = {
        "data": cpu_data.user,
        "time": new_time,
    }

    print data

    url = "http://127.0.0.1:8080/web/save/cpu/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    send_data = urllib.urlencode(data)
    request = urllib2.Request(url, data=send_data, headers=headers)
    opener = urllib2.urlopen(request)
    print opener.read()
    time.sleep(1)
