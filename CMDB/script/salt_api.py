#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import yaml
import os
import requests
import json

try:
    import cookielib
except:
    import http.cookiejar as cookielib

# 使用urllib2请求https出错，做的设置
import ssl

context = ssl._create_unverified_context()

# 使用requests请求https出现警告，做的设置
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
salt_file = open(os.path.join(BASE_DIR, 'script/salt.yaml').replace("\\", "/"))
salt_conf = yaml.load(salt_file)
salt_api_address = salt_conf['salt-api']['address']
salt_api_username = salt_conf['salt-api']['username']
salt_api_password = salt_conf['salt-api']['password']


class SaltApi:
    """定义salt api接口的类"""
    def __init__(self):
        """初始化基本参数"""
        self.url = salt_api_address
        self.username = salt_api_username
        self.password = salt_api_password
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Content-type": "application/json"
            # "Content-type": "application/x-yaml"
        }
        self.params = {'client': 'local', 'fun': ''}

    def get_token(self):
        """初始化获得token"""
        login_url = self.url + "login"
        login_params = {'username': self.username, 'password': self.password, 'eauth': 'pam'}
        send_data = json.dumps(login_params)
        request = requests.post(login_url, data=send_data, headers=self.headers, verify=False)
        response = request.json()
        result = dict(response)
        token = result['return'][0]['token']
        return token

    def get_data(self, url, params):
        """post请求salt-api函数"""
        self.headers['X-Auth-Token'] = self.get_token()
        send_data = json.dumps(params)
        request = requests.post(url, data=send_data, headers=self.headers, verify=False)
        # response = request.text
        # response = eval(response)     使用x-yaml格式时使用这个命令把回应的内容转换成字典
        # print response
        # print request
        # print type(request)
        response = request.json()
        result = dict(response)
        # print result
        return result['return'][0]

    def command(self, tgt, method, arg=None):
        """远程执行命令，相当于salt 'client1' cmd.run 'free -m'"""
        if arg:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg}
        else:
            params = {'client': 'local', 'fun': method, 'tgt': tgt}
        print '命令参数: ', params
        result = self.get_data(self.url, params)
        return result

    def batch_command(self, tgt, method, arg=None):
        """
        远程多台客户端执行命令，请求参数带'expr_form': 'nodegroup'是以组的方式来执行salt命令, 'tgt'就是组名
        请求参数带'expr_form': 'list'是以列表的方式来执行salt命令, 'tgt'就是传入的一个主机列表，相当于salt -L 'client1,client2'
        salt -L 'client1,client2' cmd.run 'free -m'"""
        if arg:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg, 'expr_form': 'list'}
            # params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg, 'expr_form': 'nodegroup'}
        else:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'expr_form': 'list'}
            # params = {'client': 'local', 'fun': method, 'tgt': tgt, 'expr_form': 'nodegroup'}
        print '命令参数: ', params
        result = self.get_data(self.url, params)
        return result

    def async_command(self, tgt, method, arg=None):  # 异步执行salt命令，根据jid查看执行结果
        """远程异步执行命令"""
        if arg:
            params = {'client': 'local_async', 'fun': method, 'tgt': tgt, 'arg': arg}
        else:
            params = {'client': 'local_async', 'fun': method, 'tgt': tgt}
        jid = self.get_data(self.url, params)['jid']
        return jid

    def batch_async_command(self, tgt, method, arg=None):  # 异步执行salt命令，根据jid查看执行结果
        """远程多台客户端异步执行命令"""
        if arg:
            params = {'client': 'local_async', 'fun': method, 'tgt': tgt, 'arg': arg, 'expr_form': 'list'}
            # params = {'client': 'local_async', 'fun': method, 'tgt': tgt, 'arg': arg, 'expr_form': 'nodegroup'}
        else:
            params = {'client': 'local_async', 'fun': method, 'tgt': tgt, 'expr_form': 'list'}
            # params = {'client': 'local_async', 'fun': method, 'tgt': tgt, 'expr_form': 'nodegroup'}
        jid = self.get_data(self.url, params)['jid']
        return jid

    def deploy(self, tgt, arg):  # 同步进行salt模块安装
        """
        模块安装，相当于salt 'client1' state.sls httpd
        tgt等于*就是选择全部客户端
        """
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        print '命令参数: ', params
        result = self.get_data(self.url, params)
        return result

    def batch_deploy(self, tgt, arg):
        """远程多台模块安装，相当于salt 'client1,client2' state.sls httpd"""
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'list'}
        # params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
        print '命令参数: ', params
        result = self.get_data(self.url, params)
        return result

    def async_deploy(self, tgt, arg):  # 异步执行salt模块安装，根据jid查看执行结果
        """远程异步模块安装"""
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        jid = self.get_data(self.url, params)['jid']
        return jid

    def batch_async_deploy(self, tgt, arg):  # 异步执行salt模块安装，根据jid查看执行结果
        """远程多台异步模块安装"""
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'list'}
        # params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
        jid = self.get_data(self.url, params)['jid']
        return jid

    def look_jid(self, jid):  # 根据异步执行命令返回的jid查看事件结果
        params = {'client': 'runner', 'fun': 'jobs.lookup_jid', 'jid': jid}
        print params
        result = self.get_data(self.url, params)
        return result

    def list_all_key(self):
        """查看所有的key，相当于salt-key -L"""
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        print '命令参数: ', params
        response = self.get_data(self.url, params)
        print response
        minions_pre = response['data']['return']['minions_pre']
        # print minions_pre
        minions = response['data']['return']['minions']
        # print minions
        status = response['data']['success']
        print status
        return minions, minions_pre

    def accept_key(self, match):
        """添加key，相当salt-key -a"""
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': match}
        print '命令参数: ', params
        response = self.get_data(self.url, params)
        # print response
        try:
            result = response['data']['return']['minions']
            # print result
            status = response['data']['success']
            return status
        except KeyError:
            status = False
            print '认证失败，请重启salt-minion或检查minion配置'
            return status

    def delete_key(self, match):
        """删除key，相当salt-key -d"""
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': match}
        print '命令参数: ', params
        response = self.get_data(self.url, params)
        # print response
        # result = response['data']['return']
        # print result
        status = response['data']['success']
        return status


def main():
    print '============================='
    print '同步执行命令'
    salt1 = SaltApi()
    print salt1.get_token()
    salt_tgt = '*'
    salt_test = 'test.ping'
    salt_method = 'cmd.run'
    salt_arg = 'free -m'
    print salt1.command(salt_tgt, salt_test)
    print salt1.command(salt_tgt, salt_method, salt_arg)

    # print '============================='
    # print '列表形式同步执行命令'
    # salt5 = SaltApi()
    # salt_tgt = ['client1', 'saltstack']
    # salt_test = 'test.ping'
    # salt_method = 'cmd.run'
    # salt_arg = 'free -m'
    # print salt5.batch_command(salt_tgt, salt_test)
    # print salt5.batch_command(salt_tgt, salt_method, salt_arg)

    # print '==========================='
    # print '异步执行命令'
    # salt1 = SaltApi()
    # salt_tgt = '*'
    # salt_method = 'cmd.run'
    # salt_arg = 'df -hT'
    # jid = salt1.async_command(salt_tgt, salt_method, salt_arg)
    # print jid
    # print salt1.look_jid(jid)

    # print '==========================='
    # print '列表形式异步执行命令'
    # salt1 = SaltApi()
    # salt_tgt = ['client1', 'saltstack']
    # salt_method = 'cmd.run'
    # salt_arg = 'df -hT'
    # jid = salt1.batch_async_command(salt_tgt, salt_method, salt_arg)
    # print jid
    # print salt1.look_jid(jid)

    # print '==========================='
    # print '同步安装模块'
    # salt6 = SaltApi()
    # salt_tgt = 'client1'    # 客户端
    # salt_arg = 'httpd'  # 模块，即定义的sls脚本文件
    # result = salt6.deploy(salt_tgt, salt_arg)
    # print result

    # print '==========================='
    # print '列表形式同步安装模块'
    # salt6 = SaltApi()
    # salt_tgt = ['client1', 'saltstack']    # 客户端
    # salt_arg = 'httpd'  # 模块，即定义的sls脚本文件
    # result = salt6.batch_deploy(salt_tgt, salt_arg)
    # print result

    # print '==========================='
    # print '异步安装模块'
    # salt6 = SaltApi()
    # salt_tgt = 'client1'    # 客户端
    # salt_arg = 'httpd'  # 模块，即定义的sls脚本文件
    # jid = salt6.async_deploy(salt_tgt, salt_arg)
    # print jid
    # print salt6.look_jid(jid)

    # print '==========================='
    # print '列表形式异步安装模块'
    # salt6 = SaltApi()
    # salt_tgt = ['client1', 'saltstack']  # 客户端
    # salt_arg = 'httpd'  # 模块，即定义的sls脚本文件
    # jid = salt6.batch_async_deploy(salt_tgt, salt_arg)
    # print jid
    # print salt6.look_jid(jid)

    # print '========================'
    # print '查看所有key'
    # salt4 = SaltApi()
    # print salt4.list_all_key()

    # print '========================'
    # print '添加key'
    # salt2 = SaltApi()
    # print salt2.accept_key('*')

    # print '========================'
    # print '删除key'
    # salt3 = SaltApi()
    # print salt3.delete_key('*')

    # print '========================'
    # print '查看所有key'
    # salt4 = SaltApi()
    # print salt4.list_all_key()


if __name__ == '__main__':
    main()

salt = SaltApi()

"""
curl -sSk https://localhost:8001/login \
    -H 'Accept: application/x-yaml' \
    -d username=saltapi \
    -d password=salt2017 \
    -d eauth='pam'
curl -sSk https://localhost:8001 \
    -H 'Accept: application/x-yaml' \
    -H 'X-Auth-Token: 21dffd2f3c6e51c9478ca7505e52dc041328827f'\
    -d client=local \
    -d tgt='*' \
    -d fun=test.ping
"""
