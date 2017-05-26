#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import json
import urllib
import urllib2

dingtalk_api = "https://oapi.dingtalk.com/robot/send?access_token=6b208a1edc2b50d4be17c765cd9a07edf3c87e6ae9d0f8eaa" \
               "b0832ded3a19d24"
headers = {
    "Content-Type": "application/json",
    "Charset": "utf-8"
}
data = {
    "msgtype": "text",
    "text": {
        "content": "小乖乖儿， 快把门开开。"
    },
    "at": {
        # "atMobiles": [        # 发送给指定的人
        #     "156xxxx8827",
        #     "189xxxx8325"
        # ],
        # "isAtAll": 'false'
        "isAtAll": 'True'   # 发送群里
    }
}

send_data = json.dumps(data)
request = urllib2.Request(url=dingtalk_api, data=send_data, headers=headers)
opener = urllib2.urlopen(request)
reader = opener.read()
print reader
