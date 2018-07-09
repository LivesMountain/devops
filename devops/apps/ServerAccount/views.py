from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import *
import json
import hashlib
import base64
from django.http import HttpResponse
from decimal import Decimal
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.views.decorators.cache import cache_page
import requests

# Create your views here
def index(request):
    return render(request, "base.html")
def Application_account(request):
    account_name=request.GET['name']
    account_email=request.GET['email']
    account_passwd=request.GET['passwd']
    application_ip=request.GET['ip']

    informations=account.objects.filter(email="%s"%account_email).filter(ip="%s"%application_ip)
    print(account.objects.all())
    response={}
    if informations:
        response['msg']="你已有账号在该机器"
        response['error_num'] = 0
    else:
        account.objects.create(name="%s" % account_name, passwd="%s" % account_passwd, email="%s" % account_email,ip="%s" % application_ip, user_check=0)
        url = 'http://127.0.0.1:8080/sendmail/api/?message=%s申请%s&con=likun@guoshengtianfeng.com&header=服务器账号申请'%(account_email,application_ip)
        s = requests.session()
        s.get(url=url)
        response['msg']="申请成功,申请信息会发送给管理员"
        response['error_num'] = 0
    return JsonResponse(response,safe=False)