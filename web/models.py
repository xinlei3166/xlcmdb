#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import sys

reload(sys)

sys.setdefaultencoding('utf8')

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import hashlib


class UserProfile(models.Model):
    """定义用户信息表"""
    username = models.CharField(max_length=32, verbose_name="账户名", unique=True)
    password = models.CharField(max_length=100, verbose_name="密码", help_text='请注意，输入明文密码自动保存为加密后的密码。不要轻易点击保存会改掉密码的。')
    nickname = models.CharField(max_length=32, verbose_name="昵称")
    email = models.EmailField(verbose_name="邮箱", null=True)
    phone = models.CharField(max_length=32, verbose_name="电话", null=True)
    headimg = models.ImageField(upload_to='upload/headimg/0', verbose_name='用户头像', default='upload/headimg/0/default.jpg', help_text='可选项，不填使用默认图片。')
    departments = models.ForeignKey('Departments', verbose_name="部门", blank=True)
    group = models.ForeignKey('GroupProfile', verbose_name='组名', blank=True, null=True)
    permission = models.ManyToManyField('Permission', verbose_name='可用权限', blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username

    # def save(self, *args, **kwargs):  # 明文密码自动加密
    #     sha256 = hashlib.sha256()
    #     sha256.update((self.password + self.username).encode('utf-8'))
    #     self.password = sha256.hexdigest()
    #     super(UserProfile, self).save(*args, **kwargs)


class GroupProfile(models.Model):
    """定义组信息表"""
    name = models.CharField(max_length=64, verbose_name="组名")
    description = models.TextField(max_length=500, verbose_name="组描述")
    permission = models.ManyToManyField('Permission', verbose_name='可用权限')

    class Meta:
        verbose_name = '组'
        verbose_name_plural = '组'

    def __str__(self):
        return self.name


class Departments(models.Model):
    """定义部门信息表"""
    name = models.CharField(max_length=32, verbose_name="部门名称")
    description = models.TextField(max_length=500, verbose_name="部门描述")

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return self.name


class Permission(models.Model):
    """自定义权限表"""
    name = models.CharField(max_length=64, verbose_name="可用权限")
    codename = models.CharField(max_length=64)
    content_type_id = models.IntegerField(verbose_name='类型ID', help_text='同一角色下的权限, '
                                                                                  '类型ID设置一样')

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = '权限'

    def __str__(self):
        return self.name


class Servers(models.Model):
    """定义主机信息表"""
    active_choice = (
        (1, u'启用'),
        (0, u'未启用'),
    )
    status_choice = (
         (1, u'已连接'),
         (0, u'未连接'),
    )
    salt_minion_choice = (  # 客户端是否安装salt-minion
         (1, u'已安装'),
         (0, u'未安装'),
    )

    hostname = models.CharField(max_length=255, verbose_name="主机名", unique=True)
    ip = models.GenericIPAddressField(max_length=32, verbose_name="ip地址", unique=True)
    mac = models.CharField(max_length=255, verbose_name="物理地址")
    cpu = models.CharField(max_length=255, verbose_name="cpu")
    mainboard = models.CharField(max_length=255, verbose_name="主板")
    mem = models.CharField(max_length=255, verbose_name="内存")
    disk = models.CharField(max_length=255, verbose_name="磁盘")
    system = models.CharField(max_length=255, verbose_name="系统信息")
    is_connect = models.IntegerField(choices=status_choice, verbose_name='认证状态', default=0)
    exist_salt_minion = models.IntegerField(choices=salt_minion_choice, verbose_name='salt-minion', default=0)
    create_date = models.DateTimeField(blank=True, auto_now_add=True, verbose_name='创建时间')
    update_date = models.DateTimeField(blank=True, auto_now=True, verbose_name='修改时间')
    is_active = models.BooleanField(choices=active_choice, verbose_name="启用状态", help_text='主机是否启用', default=1)
    departments = models.ForeignKey('Departments', verbose_name="部门", blank=True, null=True)

    class Meta:
        verbose_name = '主机管理'
        verbose_name_plural = '主机管理'

    def __str__(self):
        return self.hostname


class ServerPassword(models.Model):
    hostname = models.OneToOneField('Servers', verbose_name='主机名')
    port = models.IntegerField(verbose_name='端口')
    username = models.CharField(max_length=64, verbose_name='用户名', null=True, blank=True)
    password = models.CharField(max_length=64, verbose_name='密码', null=True, blank=True)
    ssh_key = models.CharField(max_length=64, verbose_name='秘钥', null=True, blank=True)

    class Meta:
        verbose_name = '主机秘钥'
        verbose_name_plural = '主机秘钥'

    def __str__(self):
        return self.hostname.hostname


class CpuUse(models.Model):
    """改模型用于存储指定时间段服务器cpu用户使用量"""
    data = models.CharField(max_length=32, verbose_name="cpu使用率")
    time = models.CharField(max_length=32, verbose_name="时间")

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = 'CPU'

    def __str__(self):
        return "<%s, %s>" % (self.data, self.time)


class UserAudit(models.Model):
    """用户操作审计表"""
    username = models.OneToOneField('UserProfile', verbose_name='用户名', blank=True)
    doing_date = models.DateTimeField(blank=True, auto_now=True, verbose_name='事件时间')
    doing_name = models.CharField(max_length=64, verbose_name='事件名称')
    doing_type = models.CharField(max_length=64, verbose_name='事件类型')
    doing = models.TextField(max_length=1000, verbose_name='事件详情')

    class Meta:
        verbose_name = '用户操作'
        verbose_name_plural = '用户操作'

    def __str__(self):
        return self.doing_name

