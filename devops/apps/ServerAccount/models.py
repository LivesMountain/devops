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
        verbose_name = 'account_information'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

