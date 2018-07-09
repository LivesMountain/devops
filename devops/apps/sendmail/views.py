from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import json
import smtplib
import sys
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
# Create your views here.
def send(con,message,header):#发送邮件
    from_addr = 'likun@guoshengtianfeng.com'
    password = 'MImaWANGle632'
    to_addr = [con]
    smtp_server = 'smtp.exmail.qq.com'
    smtp_port = 587
    msg = MIMEText(r'%s'%message, 'plain', 'utf-8')
    msg['From'] = '运维小分队<%s>'%from_addr
    msg['To'] = '%s'%to_addr
    msg['Subject'] = Header(u'%s'%header).encode("utf-8")
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    # server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
def return_mes(code,mes):
    data={'code':'%d'%code,'message':"%s"%mes}
    return data

@csrf_exempt
def apis(request):
    try:
        if request.method=="GET":
            mes=(request.GET['message'])
            con=(request.GET['con'])
            header=(request.GET['header'])
            send(con,mes,header)
            return JsonResponse(return_mes(0,"成功"))
    except Exception as e:
        print(e)
        return JsonResponse(return_mes(1,e))