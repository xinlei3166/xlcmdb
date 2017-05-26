#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import urllib
import urllib2
import salt.client

client = salt.client.LocalClient()
status = client.cmd("*", "test.ping")
# ip = client.cmd("*", "grains.item", ['ip_addr'])
# system = client.cmd("*", "grains.item", ['system_info'])
ret = {}
for i in status.keys():
    ret[i] = {
        "hostname": str(i),
        # "ip": str(ip[i]['ip_addr']),
        "status": status[i]
    }

# print ret

host_url = 'http://172.16.0.1:8080/web/server/salt/test/api/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
}

data = urllib.urlencode(ret)
req = urllib2.Request(url=host_url, data=data, headers=headers)
opener = urllib2.urlopen(req)
print opener.read()
