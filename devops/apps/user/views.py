# from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django import forms
from devops.settings import *
from django.http import JsonResponse
import re
from django.contrib.auth.decorators import login_required

# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密_码',widget=forms.PasswordInput())
    email=forms.CharField(label='邮箱',max_length=100)

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

@csrf_exempt
def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username=uf.cleaned_data['username']
            password=uf.cleaned_data['password']
            email=uf.cleaned_data['email']
            User_isexist=User.objects.filter(username=username)
            response = {}
            if User_isexist:
                response['msg'] = "你已有账号"
                response['error_num'] = 0
            else:
                if check_password(password):
                    if check_email(email):
                        registAdd = User.objects.create_user(username=username, password=password, email=email)
                        if registAdd == False:
                            return render(request, 'share1.html', {'registAdd': registAdd, 'username': username})
                        else:
                            return render(request, 'share1.html', {'registAdd': registAdd})
                    else:
                        response['msg'] = "请输入公司邮箱方便通知"
                        response['error_num'] = 0
                else:
                    response['msg'] = "请输入包含A-Z，a-z，0-9，位数多于6位的密码"
                    response['error_num'] = 0
            return JsonResponse(response, safe=False)
    else:
        uf=UserForm()
    return render(request,'regist1.html', {'uf': uf})

@csrf_exempt
def login(request):
    if request.method == 'GET':
        global next_to
        next_to = request.GET.get('next',None)
        # print(next_to)
        return render(request, 'user_index.html')
    if request.user:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            # print(next_to)

            re = auth.authenticate(username=username,password=password)  #用户认证
            if re is not None:  #如果数据库里有记录（即与数据库里的数据相匹配或者对应或者符合）
                auth.login(request,re)   #登陆成功
                if next_to:
                    return HttpResponseRedirect(next_to)    #跳转--redirect指从一个旧的url转到一个新的url
                else:
                    return HttpResponseRedirect(LOGIN_URL)
            else:  #数据库里不存在与之对应的数据
                return render(request,'user_index.html',{'login_error':'用户名或密码错误'})  #注册失败


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(LOGIN_URL)
