#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import json
import urllib
import urllib2

# url = "http://172.16.0.1/api_jsonrpc.php"
# headers = {
#     "Content-type": "application/json-rpc"
# }
# data = {
#     "jsonrpc": "2.0",
#     "method": "user.login",
#     "params": {
#         "user": "junxi",
#         "password": "123456"
#     },
#     "id": 1,
# }
#
# sendData = json.dumps(data)
# request = urllib2.Request(url, data=sendData, headers=headers)
# opener = urllib2.urlopen(request)
# reader = opener.read()
# result = json.loads(reader)
# print result
# token = result["result"]
# print token

zabbix_api = "http://172.16.0.1/api_jsonrpc.php"


class ZabbixApi:
    def __init__(self, url, port=8080):
        self.url = url
        self.headers = {
            "Content-type": "application/json-rpc"
        }
        self.base_data = {
            "jsonrpc": "2.0",
            "method": "",
            "params": "",
            "id": 1,
            }
        self.token_method = self.base_data
        self.token_method["method"] = "user.login"
        self.token_method["params"] = {
            "user": "junxi",
            "password": "123456"
        }
        self.token = self.get_data(self.token_method)['result']
        self.base_data['auth'] = self.token

    def get_data(self, data):
        send_data = json.dumps(data)
        request = urllib2.Request(url=self.url, data=send_data, headers=self.headers)
        opener = urllib2.urlopen(request)
        reader = opener.read()
        result = json.loads(reader)
        return result

    def get_host(self):
        self.base_data['method'] = "host.get"
        self.base_data['params'] = {"output": ["hostid", "host"]}
        return self.get_data(self.base_data)

if __name__ == '__main__':
    zabbix = ZabbixApi(zabbix_api)
    token = zabbix.token
    # print token
    host = zabbix.get_host()
    print host
