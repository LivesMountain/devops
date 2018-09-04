from django.db import models

# Create your models here.
class palypath(models.Model):
    path = models.CharField(max_length=100, verbose_name=u'playbook路径')
    func=models.CharField(max_length=100, verbose_name=u'功能')
    class Meta:
        verbose_name = u'func'
        verbose_name_plural = verbose_name
        db_table = "playbook"
    def __str__(self):
        return self.func