from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .sendmail import sendmail
import re

def check_password(passwd):
    if re.match(r'^(?=.*[A-Za-z])(?=.*[0-9])\w{6,}$',passwd):
        print("password %s correct"%passwd)
        return True
    else:
        print("password %s is invalid"%passwd)
        return False


def check_email(mail):
    import re
    text = mail
    if re.match(r'[0-9a-zA-Z_]{0,19}@guoshengtianfeng.com', text):
        return True
    else:
        return False
# Create your views here
def index(request):
    return render(request, "base.html")

def Application_account(request):
    account_name=request.GET['name']
    account_email=request.GET['email']
    account_passwd=request.GET['passwd']
    application_ip=request.GET['ip']
    check_password(account_passwd)
    informations=account.objects.filter(email="%s"%account_email).filter(ip="%s"%application_ip)
    print(account.objects.all())
    response={}
    if informations:
        response['msg']="你已有账号或已申请在该机器"
        response['error_num'] = 0
    else:
        if check_password(account_passwd):
            if check_email(account_email):

                account.objects.create(name="%s" % account_name, passwd="%s" % account_passwd, email="%s" % account_email,ip="%s" % application_ip, user_check=0)
                account_apply.objects.create(name="%s" % account_name, passwd="%s" % account_passwd, email="%s" % account_email,ip="%s" % application_ip, user_check=0)
                sm = sendmail("%s申请%s"%(account_email,application_ip), "likun@guoshengtianfeng.com", "服务器账号申请")
                sm.send()
                response['msg']="申请成功,申请信息会发送给管理员"
                response['error_num'] = 0
            else:
                response['msg'] = "请输入公司邮箱方便通知"
                response['error_num'] = 0
        else:
            response['msg'] = "请输入包含A-Z，a-z，0-9，位数多于6位的密码"
            response['error_num'] = 0
    return JsonResponse(response,safe=False)