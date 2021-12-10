#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
import smtplib
import time
from email.message import Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.utils
import base64



website = 'www.yasn.com'
error_website = 'cms.yasn.com'
four_website = 'www.yasn.com/err'
from_addr = 'yunwei@yasn.com.cn'
username = 'yunwei@yasn.com.cn'
password = 'Yasn-+*@2016'
smtp_server = 'smtp.yasn.com.cn'
to_addr = 'zhengxinlei@yasn.com.cn'
cc_addr = 'yunwei@yasn.com.cn'
# content = 'python 发送邮件测试'

def send_mail(from_addr,username,password,smtp_server,to_addr,content):

    msg = MIMEMultipart()
    txt = MIMEText(content,'plain','utf-8')    
    msg.attach(txt)

    msg['to'] = to_addr
    msg['from'] = from_addr
    msg['subject'] = 'website_yasn'

    try:
        server = smtplib.SMTP()
        server.connect(smtp_server)
        server.starttls()
        server.login(username,password)
        server.sendmail(msg['from'],msg['to'],msg.as_string())
        time.sleep(5)
        server.quit()
        print('发送成功')

    except Exception as e:
        print(str(e))
 
# send_mail(from_addr,username,password,smtp_server,to_addr,content)

# 访问 yasn 站点，正常为200，404 文件找不到，000 站点挂了
# site_access = os.popen("curl -o /dev/null -s -w %{http_code} 'www.yasn.com/err'")
# site_access = os.popen("curl -o /dev/null -s -w %{http_code} 'cms.yasn.com'")
site_access = os.popen("curl --connect-timeout 60 -o /dev/null -s -w %{http_code} 'www.yasn.com'")
access_result = site_access.read()


if access_result == '000':
    content = ('%s 站点打不开了，请及时处理.' % website)
    # print(content)
    send_mail(from_addr,username,password,smtp_server,to_addr,content)

elif access_result == '404':
    content = ('%s 站点%s，请及时处理.' % (website,access_result))
    # print(content)
    send_mail(from_addr,username,password,smtp_server,to_addr,content)

elif access_result == '200':
    content = ('%s 站点状态%s正常.' % (website,access_result))
    #print(content)
    #send_mail(from_addr,username,password,smtp_server,to_addr,content)

else:
    content = ('%s 站点状态%s，请确认.' % (website,access_result))
    # print(content)
    send_mail(from_addr,username,password,smtp_server,to_addr,content)    



