from django.db import models

# Create your models here.

class nagios_log(models.Model):
    Responsible = models.CharField(max_length=100, verbose_name=u'业务负责人')
    Business_name=models.CharField(max_length=100, verbose_name=u'业务名称')
    url = models.CharField(max_length=100, verbose_name=u'访问地址')
    class Meta:
        verbose_name = u'Business_name'
        verbose_name_plural = verbose_name
        db_table = "nagioslog"
    def __str__(self):
        return self.Business_name