#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os

def our_test():
    grains = {}
    grains["say"] = "hello world"
    return grains

def our_test1():
    grains = {}
    command = "free -m"
    with os.popen(command) as f:
        grains["mem_usage"] = f.read()
    return grains

def get_ip():
    grains = {}
    command = "ifconfig ens32|awk 'NR==2{printf $2}'"
    with os.popen(command) as f:
        grains["ip_addr"] = f.read()
    return grains

def get_syetem():
    grains = {}
    command = "cat /etc/redhat-release"
    with os.popen(command) as f:
        grains["system_info"] = f.read()
    return grains
