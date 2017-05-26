#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import paramiko
# from web import models


class WebSsh:
    """使用时候记得给hostname，port，username，password重新赋值"""
    def __init__(self):
        self.hostname = ''
        self.port = 22
        self.username = ''
        self.password = ''

    def ssh_command(self, command):
        # 简单使用方法
        ssh = paramiko.SSHClient()  # 实例化ssh连接
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # 设置使用默认的证书
        ssh.connect(        # 要连接的远程机器信息
            hostname=self.hostname,      # 主机名，没有做dns解析或修改/etc/hosts文件，则需要使用主机IP
            port=self.port,
            username=self.username,
            password=self.password,
        )
        stdin, stdout, stderr = ssh.exec_command(command)    # 要执行的命令
        result = stdout.read()
        # print result # 查看执行结果
        ssh.close() # 关闭连接
        return result


def main():
    # 数据库中调用主机秘钥信息来执行命令，可以使用python manage.py shell进入命令行测试
    # web_ssh = WebSsh()
    # obj = models.Servers.objects.get(id=2) # 2是saltstack服务端主机在表中的id
    # # web_ssh.hostname = str(obj.ip)    # 默认是unicode需要转换
    # web_ssh.hostname = str(obj.hostname)
    # web_ssh.port = obj.serverpassword.port  # 查看类型是int，不需要转换
    # web_ssh.username = str(obj.serverpassword.username)
    # web_ssh.password = str(obj.serverpassword.password)
    # command = 'hostname'
    # web_ssh.ssh_command(command)

    # web_ssh = WebSsh()
    # # web_ssh.hostname = '172.16.0.20'
    # web_ssh.hostname = 'client1'
    # web_ssh.port = 22
    # web_ssh.username = 'root'
    # web_ssh.password = '123456'
    # command = 'hostname'
    # print web_ssh.ssh_command(command)

    for i in ['172.16.0.19', '172.16.0.20']:
        web_ssh = WebSsh()
        web_ssh.hostname = i
        web_ssh.port = 22
        web_ssh.username = 'root'
        web_ssh.password = '123456'
        for c in ['mkdir aaa', 'yum -y install wget']:
            print web_ssh.ssh_command(c)

if __name__ == '__main__':
    main()

webssh = WebSsh()