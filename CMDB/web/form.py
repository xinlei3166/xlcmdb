#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

from django import forms
from . import models
from django.contrib.admin import widgets


class ServersFront(forms.ModelForm):

    class Meta:
        exclude = ()
        model = models.Servers
        widget = {
            'name': forms.DateTimeField(widget=widgets.AdminDateWidget, label=u'时间')
        }