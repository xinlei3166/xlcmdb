#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import paramiko

# 简单使用方法
ssh = paramiko.SSHClient()  # 实例化ssh连接
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # 设置使用默认的证书
ssh.connect(        # 要连接的远程机器信息
    hostname="saltstack", # 主机名，没有做dns解析或修改/etc/hosts文件，则需要使用主机IP
    port=22,
    username="root",
    password="123456",
)
stdin, stdout, stderr = ssh.exec_command("ls")    # 要执行的命令
print stdout.read() # 查看执行结果
ssh.close() # 关闭连接


# 进阶
ssh = paramiko.SSHClient()  # 实例化ssh连接
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # 设置使用默认的证书
ssh.connect(        # 要连接的远程机器信息
    hostname="172.16.0.1",
    port=22,
    username="root",
    password="123456",
)
channel = ssh.invoke_shell()
channel.settimeout(1)
while True:
    command = raw_input("> ")
    channel.send("%s\n" % command)
    while True:
        try:
            rep = channel.recv(9999)    # 进行命令结果接收，括号内是一次接收多少
            print rep
        except Exception as e:
            break
        if command == 'exit':
            break
