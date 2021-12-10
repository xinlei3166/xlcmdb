#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from . import models
from .form import *
from script.salt_api import salt
from script.web_ssh import webssh
from django.contrib.auth.hashers import make_password, check_password
# from django.forms.models import model_to_dict
from django.core import serializers
import datetime
import json
import hashlib
import re
import time
import os


def valid_login(func):  # 验证session
    def inner(request, *args, **kwargs):
        username = request.session.get("username", "")
        if username:
            user_data = models.UserProfile.objects.get(username=username)
            user_permission = [i.codename for i in user_data.permission.filter()]  # 用户所有权限
            group_permission = [i.codename for i in user_data.group.permission.filter()]  # 用户所在组所有权限
            context = {
                "id": user_data.id,
                "username": user_data.username,
                "password": user_data.password,
                "nickname": user_data.nickname,
                "email": user_data.email,
                "phone": user_data.phone,
                "headimg": str(user_data.headimg),
                "user_permission": user_permission,
                "group_permission": group_permission,
            }
            request.session["userdata"] = context
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/web/login/")

    return inner


# def hash_md5(password):       # md5加密
#     md5 = hashlib.md5()
#     md5.update(password.encode('utf-8'))
#     md5_password = md5.hexdigest()
#     return md5_password


def hash_sha256(password, username):  # sha256加密
    sha256 = hashlib.sha256()
    sha256.update((password + username).encode('utf-8'))
    sha256_password = sha256.hexdigest()
    return sha256_password


@valid_login
def index(request):  # 首页
    # print request.session['userdata']['group_permission']
    # username = request.COOKIES.get('username', 'None')
    return render(request, 'index.html', locals())


def register(request):  # 用户注册
    departments = models.Departments.objects.all()
    if request.method == 'POST' and request.POST:
        user = models.UserProfile()
        username = request.POST['username']
        password = request.POST['password'].split(',')[0]
        user.username = username
        password = hash_sha256(password, username)
        user.password = password
        user.nickname = request.POST['nickname']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        if request.FILES:
            user.headimg = upload_file(username, request.FILES['headimg'])
        else:
            print 'headimg为空'
        user.departments_id = request.POST['departments']
        user.group_id = models.GroupProfile.objects.get(name='user').id  # 新创建用户默认添加到普通用户组里(user)
        user.save()
        new_user = models.UserProfile.objects.get(username=username)
        view_server = models.Permission.objects.get(codename='view_server')  # 查看主机权限
        add_server = models.Permission.objects.get(codename='add_server')  # 增加主机权限
        new_user.permission.add(view_server, add_server)  # 给新用户增加默认权限
        return HttpResponseRedirect("/web/login/")
    else:
        return render(request, 'register.html', locals())


def upload_file(username, f):
    print("--->", f.name)
    base_img_upload_path = 'static/upload/headimg'
    user_path = "%s/%s" % (base_img_upload_path, username)
    if not os.path.exists(user_path):
        os.mkdir(user_path)
    with open('%s/%s' % (user_path, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return "upload/headimg/%s/%s" % (username, f.name)


def user_valid(username):
    userlist = models.UserProfile.objects.filter(username=username)
    if userlist:
        # return {"password": userlist[0].password}
        return True
    else:
        return False


def login(request):  # 用户登录
    if request.method == 'POST' and request.POST:
        # 获取提交上来的用户名和密码
        username = request.POST['username']
        password = request.POST['password']
        # print request.POST
        # 判断该用户是否存在
        if user_valid(username):
            data = models.UserProfile.objects.get(username=username)  # 获取用户单条信息
            print data.password
            password = hash_sha256(password, username)
            print password
            if password == data.password:  # 判断密码相同
                response = HttpResponseRedirect("/web/")  # 实例化一个response响应
                # response.set_cookie("username", username)  # cookie 对响应设置cookie
                request.session['username'] = username  # 设置session
                return response  # 返回首页
            else:  # 判断密码不同
                return HttpResponseRedirect("/web/login")
        else:  # 如果用户不存在
            return HttpResponseRedirect("/web/login")
    else:  # 如果请求的方式不对或者请求数据为空
        return render(request, "login.html", locals())


def logout(request):  # 用户注销
    request.session['username'] = None
    return HttpResponseRedirect('/')


@valid_login
def user_profile(request, user_id):  # 用户查看个人信息
    user_data = models.UserProfile.objects.get(id=user_id)
    return render(request, 'user-profile.html', locals())


@valid_login
def update_profile(request, user_id):  # 用户修改个人信息
    user_data = models.UserProfile.objects.get(id=user_id)
    departments = models.Departments.objects.all()
    if request.method == 'POST' and request.POST:
        print request.POST
        print request.FILES
        username = user_data.username
        user_data.departments_id = request.POST['departments']
        user_data.nickname = request.POST['nickname']
        user_data.email = request.POST['email']
        user_data.phone = request.POST['phone']
        if request.FILES:
            user_data.headimg = upload_file(username, request.FILES['headimg'])
        else:
            print 'headimg为空'
        user_data.save()
        return HttpResponseRedirect('/web/user/profile/%d' % int(user_id))
    return render(request, 'update-profile.html', locals())


@valid_login
def change_password(request, user_id):  # 修改密码
    user_data = models.UserProfile.objects.get(id=user_id)
    if request.method == 'POST' and request.POST:
        print request.POST
        old_password = request.POST['old_password']
        username = user_data.username
        old_password = hash_sha256(old_password, username)
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']
        if old_password != user_data.password:
            status = 'error'
        elif new_password1 != new_password2:
            status = 'inconsistent'
        else:
            user_data.password = hash_sha256(new_password1, username)
            user_data.save()
            status = 'success'
    return render(request, 'change-password.html', locals())


def help(request):
    return render(request, 'help.html')


@valid_login
def view_user_list(request):  # 管理员查看用户列表
    user_data = models.UserProfile.objects.all()
    permissions = models.Permission.objects.all()
    if request.method == 'POST' and request.POST:
        data = request.POST
        print data
        if models.UserProfile.objects.filter(username=data['select']):
            user_data = models.UserProfile.objects.filter(username=data['select'])
            return render(request, 'view-user-list.html', locals())
        elif models.UserProfile.objects.filter(nickname=data['select']):
            user_data = models.UserProfile.objects.filter(nickname=data['select'])
        else:
            error = 'no exist'
            return render(request, 'view-user-list.html', locals())
    return render(request, 'view-user-list.html', locals())


@valid_login
def view_user_profile(request, user_id):  # 管理员查看用户信息
    user_data = models.UserProfile.objects.get(id=user_id)
    return render(request, 'view-user-profile.html', locals())


@valid_login
def update_user_profile(request, user_id):  # 管理员修改用户信息
    user_data = models.UserProfile.objects.get(id=user_id)
    departments = models.Departments.objects.all()
    groups = models.GroupProfile.objects.all()
    if request.method == 'POST' and request.POST:
        print request.POST
        print request.FILES
        username = user_data.username
        user_data.departments_id = request.POST['departments']
        user_data.nickname = request.POST['nickname']
        user_data.email = request.POST['email']
        user_data.phone = request.POST['phone']
        user_data.group_id = request.POST['group']
        if request.FILES:
            user_data.headimg = upload_file(username, request.FILES['headimg'])
        else:
            print 'headimg为空'
        user_data.save()
        return HttpResponseRedirect('/web/view/user/profile/%d' % int(user_id))
    return render(request, 'update-user-profile.html', locals())


@valid_login
def reset_password(request, user_id):  # 管理员重置密码
    user_data = models.UserProfile.objects.get(id=user_id)
    if request.method == 'POST' and request.POST:
        print request.POST
        username = user_data.username
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']
        if new_password1 != new_password2:
            status = 'inconsistent'
        else:
            user_data.password = hash_sha256(new_password1, username)
            user_data.save()
            status = 'success'
    return render(request, 'reset-password.html', locals())


@valid_login
def alter_permisson(request, user_id):  # 管理员修改用户权限
    user = models.UserProfile.objects.get(id=user_id)
    if request.method == 'POST' and request.POST:
        print dict(request.POST)
        permissions = models.Permission.objects.all()
        try:
            new_permissions = dict(request.POST)['permission']  # 如果前台一个权限也没选的话触发异常，清空用户的所有权限
        except:
            for i in permissions:
                permission = models.Permission.objects.get(id=i.id)
                user.permission.remove(permission)
        else:
            new_permissions = dict(request.POST)['permission']
            new_permissions = [int(i) for i in new_permissions]
            for i in permissions:
                if i.id in new_permissions:
                    permission = models.Permission.objects.get(id=i.id)
                    user.permission.add(permission)
                else:
                    permission = models.Permission.objects.get(id=i.id)
                    user.permission.remove(permission)
    return HttpResponseRedirect('/web/view/user/list/')


@valid_login
def add_user(request):  # 添加用户
    departments = models.Departments.objects.all()
    if request.method == 'POST' and request.POST:
        print request.POST
        username = request.POST['username']
        try:
            u = models.UserProfile.objects.get(username=username)
            new_user_status = 'exist'
            return render(request, 'add-user.html', locals())
        except:
            user = models.UserProfile()
            password = request.POST['password'].split(',')[0]
            user.username = username
            password = hash_sha256(password, username)
            user.password = password
            user.nickname = request.POST['nickname']
            user.email = request.POST['email']
            if request.FILES:
                user.headimg = upload_file(username, request.FILES['headimg'])
            else:
                print 'headimg为空'
            user.departments_id = request.POST['departments']
            user.group_id = models.GroupProfile.objects.get(name='user').id  # 新创建用户默认添加到普通用户组里(user)
            user.save()
            new_user = models.UserProfile.objects.get(username=username)
            view_server = models.Permission.objects.get(codename='view_server')  # 查看主机权限
            add_server = models.Permission.objects.get(codename='add_server')  # 增加主机权限
            new_user.permission.add(view_server, add_server)  # 给新用户增加默认权限
            new_user_status = 'success'
            return render(request, 'add-user.html', locals())
    else:
        return render(request, 'add-user.html', locals())


@valid_login
def del_user(request):  # 管理员删除用户
    if request.method == 'POST' and request.POST:
        user_id = int(request.POST['id'])
        user_data = models.UserProfile.objects.get(id=user_id)
        user_data.delete()
        result = {'status': 'success'}
    else:
        result = {'status': 'error'}
    return JsonResponse(result)


@valid_login
def view_group(request):
    groups = models.GroupProfile.objects.all()
    permissions = models.Permission.objects.all()
    return render(request, 'view-group-list.html', locals())


@valid_login
def add_group(request):  # 添加用户组
    permissons = models.Permission.objects.all()
    group = models.GroupProfile()
    if request.method == 'POST' and request.POST:
        print request.POST
        name = request.POST['name']  # 组名
        try:
            g = models.GroupProfile.objects.get(name=name)
            new_group_status = 'exist'
            return render(request, 'add-group.html', locals())
        except:
            group.name = name
            group.description = request.POST['description']
            group.save()
            new_group = models.GroupProfile.objects.get(name=name)
            permissions = models.Permission.objects.all()
            choice_permissions = dict(request.POST)['permission']  # 前台传过来选中的权限id
            choice_permissions = [int(i) for i in choice_permissions]
            for i in choice_permissions:
                permission = models.Permission.objects.get(id=i)
                new_group.permission.add(permission)
            new_group_status = 'success'
            return render(request, 'add-group.html', locals())
    else:
        return render(request, 'add-group.html', locals())


def update_group(request, group_id):
    permissions = models.Permission.objects.all()
    group = models.GroupProfile.objects.get(id=group_id)
    if request.method == 'POST' and request.POST:
        print request.POST
        name = request.POST['name']  # 组名
        group.name = name
        group.description = request.POST['description']
        group.save()
        try:
            choice_permissions = dict(request.POST)['permission']  # 如果前台一个权限也没选的话触发异常，清空组的所有权限
        except:
            for i in permissions:
                permission = models.Permission.objects.get(id=i.id)
                group.permission.remove(permission)
        else:
            choice_permissions = dict(request.POST)['permission']
            choice_permissions = [int(i) for i in choice_permissions]
            for i in permissions:
                if i.id in choice_permissions:
                    permission = models.Permission.objects.get(id=i.id)
                    group.permission.add(permission)
                else:
                    permission = models.Permission.objects.get(id=i.id)
                    group.permission.remove(permission)
        update_group_status = 'success'
        return render(request, 'update-group.html', locals())
    return render(request, 'update-group.html', locals())


@valid_login
def delete_group(request):
    if request.method == 'POST' and request.POST:
        group_id = int(request.POST['id'])
        group_data = models.GroupProfile.objects.get(id=group_id)
        group_data.delete()
        result = {'status': 'success'}
    else:
        result = {'status': 'error'}
    return JsonResponse(result)


@valid_login
def alter_group_permisson(request, group_id):  # 管理员修改用户权限
    group = models.GroupProfile.objects.get(id=group_id)
    if request.method == 'POST' and request.POST:
        print dict(request.POST)
        permissions = models.Permission.objects.all()
        try:
            new_permissions = dict(request.POST)['permission']      # 如果前台一个权限也没选的话触发异常，清空组的所有权限
        except:
            for i in permissions:
                permission = models.Permission.objects.get(id=i.id)
                group.permission.remove(permission)
        else:
            new_permissions = dict(request.POST)['permission']
            new_permissions = [int(i) for i in new_permissions]
            for i in permissions:
                if i.id in new_permissions:
                    permission = models.Permission.objects.get(id=i.id)
                    group.permission.add(permission)
                else:
                    permission = models.Permission.objects.get(id=i.id)
                    group.permission.remove(permission)
    return HttpResponseRedirect('/web/view/group/')


@valid_login
def server_list(request):  # 主机列表视图函数
    server_data = models.Servers.objects.all()
    if request.method == 'POST' and request.POST:
        data = request.POST
        reg = re.compile(r'(\d{2,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})')
        if reg.findall(data['select']):  # 判断输入是否IP，如果是则使用IP查询
            server_data = models.Servers.objects.filter(ip=data['select'])
            if server_data:
                return render(request, 'server-list.html', locals())
            else:
                error = 'unkown'
                return render(request, 'server-list.html', locals())
        else:  # 否则使用主机名查询
            server_data = models.Servers.objects.filter(hostname=data['select'])
            if server_data:
                return render(request, 'server-list.html', locals())
            else:
                error = 'unkown'
                return render(request, 'server-list.html', locals())
    return render(request, 'server-list.html', locals())


@valid_login
def servers(request, server_id):  # 单个主机详情页视图函数
    server_id = int(server_id)
    server_data = models.Servers.objects.get(id=server_id)
    return render(request, 'servers.html', locals())


@valid_login
def server_register(request):  # 主机添加视图函数
    departments = models.Departments.objects.all()
    if request.method == 'POST' and request.POST:
        server = models.Servers()
        server.hostname = request.POST['hostname']
        server.ip = request.POST['ip']
        server.mac = request.POST['mac']
        server.cpu = request.POST['cpu']
        server.mainboard = request.POST['mainboard']
        server.mem = request.POST['mem']
        server.disk = request.POST['disk']
        server.system = request.POST['system']
        server.is_active = request.POST['is_active']
        server.departments_id = request.POST['departments']
        server.save()
        new_server = models.Servers.objects.get(hostname=request.POST['hostname'])
        if new_server:
            print new_server.id
            print new_server.hostname
            return render(request, 'server-register.html', locals())
        else:
            return HttpResponseRedirect('/web/server/register/')
    else:
        return render(request, 'server-register.html', locals())


@valid_login
def server_update(request, server_id):  # 主机修改视图函数
    departments = models.Departments.objects.all()
    server_data = models.Servers.objects.get(id=server_id)
    if request.method == 'POST' and request.POST:
        server = models.Servers.objects.get(id=server_id)
        server.hostname = request.POST['hostname']
        server.ip = request.POST['ip']
        server.mac = request.POST['mac']
        server.cpu = request.POST['cpu']
        server.mainboard = request.POST['mainboard']
        server.mem = request.POST['mem']
        server.disk = request.POST['disk']
        server.system = request.POST['system']
        server.is_active = request.POST['is_active']
        server.departments_id = request.POST['departments']
        server.save()
        return HttpResponseRedirect('/web/servers/%d' % int(server_id))
    else:
        return render(request, 'server-update.html', locals())


@valid_login
def del_server(request):  # 删除主机
    if request.method == 'POST' and request.POST:
        server_id = int(request.POST["id"])
        print 'server_id', server_id
        server = models.Servers.objects.get(id=server_id)
        server.delete()
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error"})


@valid_login
def save_cpudata(request):
    if request.method == 'POST' and request.POST:
        time = request.POST['time']
        data = request.POST['data']
        cpu_data = models.CpuUse()
        cpu_data.data = data
        cpu_data.time = time
        cpu_data.save()
        result = {"status": "success"}
    else:
        result = {"status": "error"}
    return JsonResponse(result)


def reboot_server(hostname):  # 重启主机
    try:
        obj = models.Servers.objects.get(hostname=hostname)
        # hostname = str(obj.ip)    # 默认是unicode需要转换
        webssh.hostname = str(obj.hostname)  # 主机名，没有做dns解析或修改/etc/hosts文件，则需要使用主机IP
        webssh.port = obj.serverpassword.port  # 查看类型是int，不需要转换
        webssh.username = str(obj.serverpassword.username)
        webssh.password = str(obj.serverpassword.password)
        command1 = 'reboot'
        result = webssh.ssh_command(command1)
        time.sleep(1)
        print '%s正在重启中......' % hostname
        return True
        # print result
        # if result >= 3:
        #     return True
        # else:
        #     return False
    except:
        print '%s主机重启失败。' % hostname
        return False


def shutwodn_server(hostname):  # 关闭主机
    try:
        obj = models.Servers.objects.get(hostname=hostname)
        # hostname = str(obj.ip)    # 默认是unicode需要转换
        webssh.hostname = str(obj.hostname)  # 主机名，没有做dns解析或修改/etc/hosts文件，则需要使用主机IP
        webssh.port = obj.serverpassword.port  # 查看类型是int，不需要转换
        webssh.username = str(obj.serverpassword.username)
        webssh.password = str(obj.serverpassword.password)
        command1 = 'shutdown -h now'
        result = webssh.ssh_command(command1)
        time.sleep(1)
        print '%s正在关机中......' % hostname
        return True
        # print result
        # if result >= 3:
        #     return True
        # else:
        #     return False
    except:
        print '%s主机关机失败。' % hostname
        return False


@valid_login
def salt_test_api(request):  # 用户客户端执行salt_status脚本然后返回认证通信状态，请求的api接口
    if request.method == 'POST' and request.POST:
        s = models.Servers.objects.values('hostname')  # 获得Servers表中字段为hostname的对象集合
        all_host = [i['hostname'] for i in s]  # 获得Servers表中所有的主机名(即key为hostname的值)
        # print all_host
        data_item = request.POST
        # print data_item
        for i in all_host:
            if data_item.get(
                    i):  # salt '*' test.ping会返回一个字典，如果主机状态是true，则字典中就会存在其主机名，否则不存在。不存在就说明主机没Ping通，那么状态值即为0，也就是未连接。
                data_dic = eval(data_item[i])
                # print data_dic
                server_data = models.Servers.objects.get(hostname=i)
                if data_dic['status']:  # 等同于if data_dic['status'] == True
                    server_data.is_connect = 1
                server_data.save()
            else:
                server_data = models.Servers.objects.get(hostname=i)
                server_data.is_connect = 0
                server_data.save()
        result = {"status": "success"}
    else:
        result = {"status": "error"}
    return JsonResponse(result)


def salt_update_status(tgt):  # 更新状态，传入*是更新所有，传入单台客户端即更新单台的状态。
    try:
        cmd_result = salt.command(tgt, 'test.ping')  # 返回结果是一个字典
        print cmd_result
        if tgt == '*':
            s = models.Servers.objects.values('hostname')  # 获得Servers表中字段为hostname的对象集合
            all_host = [i['hostname'] for i in s]  # 获得Servers表中所有的主机名(即key为hostname的值)
            for hostname in all_host:
                if cmd_result.get(
                        hostname):  # salt '*' test.ping会返回一个字典，如果主机状态是true，则字典中就会存在其主机名，否则不存在。不存在就说明主机没Ping通，那么状态值即为0，也就是未连接。
                    server_data = models.Servers.objects.get(hostname=hostname)
                    if cmd_result[hostname]:  # 等同于if cmd_result[hostname] == True
                        server_data.is_connect = 1
                    server_data.save()
                else:
                    server_data = models.Servers.objects.get(hostname=hostname)
                    server_data.is_connect = 0
                    server_data.save()
        else:
            # cmd_result = salt.command(tgt, 'test.ping')  # 返回结果是一个字典
            # print cmd_result
            if cmd_result.get(
                    tgt):  # salt '*' test.ping会返回一个字典，如果主机状态是true，则字典中就会存在其主机名，否则不存在。不存在就说明主机没Ping通，那么状态值即为0，也就是未连接。
                server_data = models.Servers.objects.get(hostname=tgt)
                print cmd_result.get(tgt)
                if cmd_result[tgt]:  # 等同于if cmd_result[tgt] == True
                    server_data.is_connect = 1
                server_data.save()
            else:
                server_data = models.Servers.objects.get(hostname=tgt)
                server_data.is_connect = 0
                server_data.save()
                # print '更新状态成功'
    except:
        print 'what happend'


def salt_minion(hostname):  # 客户端安装salt-minion
    try:
        obj = models.Servers.objects.get(hostname=hostname)
        # hostname = str(obj.ip)    # 默认是unicode需要转换
        webssh.hostname = str(obj.hostname)  # 主机名，没有做dns解析或修改/etc/hosts文件，则需要使用主机IP
        webssh.port = obj.serverpassword.port  # 查看类型是int，不需要转换
        webssh.username = str(obj.serverpassword.username)
        webssh.password = str(obj.serverpassword.password)
        sed_master = 'sed -i "s/#master: salt/master: %s/" /etc/salt/minion' % 'saltstack'
        sed_id = 'sed -i "s/#id:/id: %s/" /etc/salt/minion' % hostname
        command = [
            'yum -y install wget',
            'mv /etc/yum.repos.d/epel.repo /etc/yum.repos.d/epel.repo.backup_`date +%F`',
            'mv /etc/yum.repos.d/epel-testing.repo /etc/yum.repos.d/epel-testing.repo.backup_`date +%F`',
            'wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo',
            'yum -y install salt-minion',
            'sed -i "s/#default_include/default_include/g" /etc/salt/minion',
            sed_master,
            sed_id,
            'systemctl enable salt-minion',
            'systemctl restart salt-minion'
        ]  # 一定要做hosts解析；master: saltstack ==> slatsatck服务端的主机名或IP; id: client1 ==> 客户端的主机名
        # command = ["mv /etc/yum.repos.d/epel.repo /etc/yum.repos.d/epel.repo.backup_`date +%F`", 'mkdir aaa']
        for i in command:
            ret = webssh.ssh_command(i)
        # ret = webssh.ssh_command(command)
        time.sleep(2)
        command1 = 'ps -ef|grep salt-minion|wc -l'
        result = webssh.ssh_command(command1)
        # print result
        if result >= 3:
            return True
        else:
            return False
    except:
        print '%s主机无法连接，安装已停止。请检查主机连接信息。' % hostname
        return False


def salt_minion_accept_key(hostname):  # 客户端安装salt-minion及认证
    ret = salt_minion(hostname)
    if ret:
        server_data = models.Servers.objects.get(hostname=hostname)
        server_data.exist_salt_minion = 1
        server_data.save()
        print '%s安装salt-minion成功' % hostname
        salt_accept_key(hostname)
    else:
        print '%s安装salt-minion失败' % hostname


def salt_reload_minion(hostname):  # 重启salt-minion
    try:
        obj = models.Servers.objects.get(hostname=hostname)  # 2是saltstack服务端主机在表中的id
        # hostname = str(obj.ip)    # 默认是unicode需要转换
        webssh.hostname = str(obj.hostname)  # 主机名，没有做dns解析或修改/etc/hosts文件，则需要使用主机IP
        webssh.port = obj.serverpassword.port  # 查看类型是int，不需要转换
        webssh.username = str(obj.serverpassword.username)
        webssh.password = str(obj.serverpassword.password)
        command = 'systemctl restart salt-minion'
        ret = webssh.ssh_command(command)
        time.sleep(1)
        command1 = 'ps -ef|grep salt-minion|wc -l'
        result = webssh.ssh_command(command1)
        time.sleep(2)
        # print result
        if result >= 3:
            return True
        else:
            print '%s重启salt-minion失败。' % hostname
            return False
    except:
        print '%s重启salt-minion失败。' % hostname
        return False


def salt_delete_key(hostname):  # 删除minion认证
    result = salt.delete_key(hostname)
    if result:
        server_data = models.Servers.objects.get(hostname=hostname)
        server_data.is_connect = 0
        server_data.save()
        print '删除%s的minion认证成功' % hostname
    else:
        print '删除%s的minion认证失败' % hostname


def salt_accept_key(hostname):  # 添加Minion认证
    result = salt.accept_key(hostname)
    if result:
        if hostname in salt.list_all_key()[0]:  # 查看已经accept的列表中是否有此主机   ([u'client1', u'saltstack'], [])
            server_data = models.Servers.objects.get(hostname=hostname)
            server_data.is_connect = 1
            server_data.save()
            print '%s认证成功' % hostname
    else:
        print '%s认证失败' % hostname


@valid_login
def salt_command(request):  # salt命令视图函数
    server_data = models.Servers.objects.all()
    return render(request, 'salt-command.html', locals())


def salt_excute_command(hostname, command):  # 前端发起ajax请求后台执行的salt执行命令函数
    if hostname == '*':
        tgt = '*'
        method = 'cmd.run'
        arg = command
        result = salt.command(tgt, method, arg)
        return result
    else:
        tgt = hostname
        method = 'cmd.run'
        arg = command
        result = salt.command(tgt, method, arg)
        return result


@valid_login
def salt_filesend(request):  # salt文件分发视图函数
    server_data = models.Servers.objects.all()
    result = salt.command('saltstack', 'cmd.run', 'ls -l /srv/salt/data/')  # saltstack是salt服务端的主机名
    file_list = {}
    f = str(result['saltstack']).split('\n')
    # print f
    for i in f[1:]:
        if i[0:1] == 'd':
            # print i.split()[-1]
            dir_name = i.split()[-1]
            file_list[dir_name] = '目录: ' + dir_name
        else:
            file_name = i.split()[-1]
            file_list[file_name] = '文件: ' + file_name
    # file_list = sorted(file_list.iteritems(), key=lambda x:x[0], reverse=False)
    # print file_list
    return render(request, 'salt-filesend.html', locals())


def salt_excute_filesend(hostname, filelist, recvdir=None):  # 前端发起ajax请求后台执行的salt文件分发函数
    method1 = 'cp.get_file'
    method2 = 'cp.get_dir'
    f_list = []
    d_list = []
    for single in filelist:
        # print f
        if single.split(': ')[0] == '文件':
            f_list.append(single.split(': ')[1])
        else:
            d_list.append(single.split(': ')[1])
    if not recvdir:
        recvdir = '/salt/data/'  # 客户端默认接收目录
        for f in f_list:
            arg = ['salt://data/' + f, recvdir + f, 'makedirs=True']
            ret = salt.command(hostname, method1, arg)
            print ret
        for d in d_list:
            arg = ['salt://data/' + d, recvdir, 'makedirs=True']
            ret = salt.command(hostname, method2, arg)
            print ret
        return True
    else:
        if recvdir[-1:] != '/':
            recvdir = recvdir + '/'
        recvdir = recvdir
        for f in f_list:
            arg = ['salt://data/' + f, recvdir + f, 'makedirs=True']
            ret = salt.command(hostname, method1, arg)
            print ret
        for d in d_list:
            arg = ['salt://data/' + d, recvdir, 'makedirs=True']
            ret = salt.command(hostname, method2, arg)
            print ret
        return True


@valid_login
def web_ssh(request):  # webssh视图函数
    server_data = models.Servers.objects.all()
    return render(request, 'web-ssh.html', locals())


def web_ssh_excute(hostname, command):  # paramiko实现远程执行命令，当salt不能使用时备用；前端发起ajax请求后台实现远程执行命令函数
    try:
        obj = models.Servers.objects.get(hostname=hostname)
        # hostname = str(obj.ip)    # 默认是unicode需要转换
        webssh.hostname = str(obj.hostname)  # 主机名，没有做dns解析或修改/etc/hosts文件，则需要使用主机IP
        webssh.port = obj.serverpassword.port  # 查看类型是int，不需要转换
        webssh.username = str(obj.serverpassword.username)
        webssh.password = str(obj.serverpassword.password)
        command = command
        ret = webssh.ssh_command(command)
        result = {hostname: ret}
        time.sleep(0.5)
        print '%s 执行命令 %s 完毕......' % (hostname, command)
        return result
    except:
        ret = '主机无法连接，执行命令请求已停止。请检查主机连接信息。'
        result = {hostname: ret}
        print '%s 主机无法连接，执行命令请求已停止。请检查主机连接信息。' % hostname
        return result


@valid_login
def saltapi(request):  # 前台页面的salt功能按钮api接口
    if request.method == 'POST' and request.POST:
        # print salt.token
        data = request.POST
        print data
        action = data['action']
        if action == 'update_status':  # 批量更新状态
            salt_update_status('*')
        elif action == 'batch_accept_key':  # 批量认证
            s = models.Servers.objects.values('hostname')
            all_host = [i['hostname'] for i in s]
            for hostname in all_host:
                try:
                    ret = salt_reload_minion(hostname)
                    if ret:
                        salt_accept_key(hostname)
                except:
                    print 'what happend'
        elif action == 'salt_delete_key':  # 删除minion
            hostname = data['hostname']
            result = salt.delete_key(hostname)
            server_data = models.Servers.objects.get(hostname=hostname)
            server_data.is_connect = 0
            server_data.save()
            print '删除%s的minion认证结果是: %s' % (hostname, result)
        elif action == 'salt_minion_accept_key':  # 安装salt-minion及minion认证
            hostname = data['hostname']
            salt_minion_accept_key(hostname)
        elif action == 'salt_accept_key':  # minion认证
            hostname = data['hostname']
            salt_accept_key(hostname)
        elif action == 'batch_salt_minion':  # 批量安装salt-minion
            s = models.Servers.objects.values('hostname')
            all_host = [i['hostname'] for i in s]
            # all_host = ['client1', 'saltstack']
            for hostname in all_host:
                salt_minion_accept_key(hostname)
                time.sleep(1)
        elif action == 'salt_reload_minion':  # 重启salt-minion
            hostname = data['hostname']
            ret = salt_reload_minion(hostname)
            print ret
        elif action == 'reboot_server':  # 重启主机
            hostname = data['hostname']
            reboot_server(hostname)
        elif action == 'shutdown_server':  # 关闭主机
            hostname = data['hostname']
            shutwodn_server(hostname)
        elif action == 'salt_command':  # salt执行命令
            hostname = data['hostname']
            command = data['command']
            print hostname, command
            ret = salt_excute_command(hostname, command)
            print ret
            result = {"status": "success", "result": ret}
            return JsonResponse(result)
        elif action == 'web_ssh':
            hostname = data['hostname']
            command = data['command']
            if hostname == '*':
                s = models.Servers.objects.values('hostname')  # 获得Servers表中字段为hostname的对象集合
                all_host = [i['hostname'] for i in s]  # 获得Servers表中所有的主机名(即key为hostname的值)组成一个列表
                result = {"status": "success", 'result': {}}
                for host in all_host:
                    ret = web_ssh_excute(host, command)
                    result['result'][host] = ret[host]
                # print result
                return JsonResponse(result)
            else:
                ret = web_ssh_excute(hostname, command)
                print ret
                result = {"status": "success", "result": ret}
                return JsonResponse(result)
        elif action == 'salt_filesend':  # salt文件分发
            hostname = data['hostname']
            filelist = [i for i in data['filelist'].split(',')]  # 把前台传来的数组字符串转换成Python列表
            recvdir = data['recvdir']
            ret = salt_excute_filesend(hostname, filelist, recvdir)
            result = {"status": "success", "result": 'success'}
            if ret:
                return JsonResponse(result)
        else:
            print '没有传入正确的指令参数'
        result = {"status": "success"}
    else:
        result = {"status": "error"}
    return JsonResponse(result)


@valid_login
def salt_key(request):  # minion列表视图函数
    server_data = models.Servers.objects.all()
    if request.method == 'POST' and request.POST:
        data = request.POST
        reg = re.compile(r'(\d{2,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})')
        if reg.findall(data['select']):
            server_data = models.Servers.objects.filter(ip=data['select'])
            single_server = models.Servers.objects.get(ip=data['select'])
            return render(request, 'salt-key.html', locals())
        else:
            server_data = models.Servers.objects.filter(hostname=data['select'])
            single_server = models.Servers.objects.get(hostname=data['select'])
            return render(request, 'salt-key.html', locals())
    return render(request, 'salt-key.html', locals())
