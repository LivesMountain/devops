# -*-coding:utf-8 -*-
from django.db import models

# Create your models here.
class account(models.Model):
    name = models.CharField(max_length=30, verbose_name=u'账户')
    passwd=models.CharField(max_length=100,verbose_name=u'密码')
    email=models.EmailField()
    ip=models.GenericIPAddressField()
    user_check=models.BooleanField()
    class Meta:
        verbose_name = u'服务器账号'
        verbose_name_plural = verbose_name
        unique_together=('ip','email',)
        db_table = "account"
    def __str__(self):
        return self.name

class account_apply(models.Model):
    name = models.CharField(max_length=30, verbose_name=u'账户')
    passwd=models.CharField(max_length=100,verbose_name=u'密码')
    email=models.EmailField()
    ip=models.GenericIPAddressField()
    user_check=models.BooleanField()
    class Meta:
        verbose_name = u'服务器账号申请'
        verbose_name_plural = verbose_name
        unique_together=('ip','email',)
        db_table = "account_apply"
    def __str__(self):
        return self.name