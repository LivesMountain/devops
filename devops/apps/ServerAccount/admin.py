
from django.contrib import admin
from .models import *
import requests
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name','email','ip','user_check')
    list_display_links = ('name',)
    list_filter = ('user_check',)
    # list_editable = ('check',)
    # print(account.objects.all())
    def delete_selected(self, request, queryset):
        for o in queryset.all():
            o.delete()
            s = requests.session()
            url="http://127.0.0.1:8080/sendmail/api/?message=你的服务器：%s账号申请被拒绝&con=%s&header=请查收"%(o.ip,o.email)
            response = s.get(url=url)

    delete_selected.short_description = '我拒绝'

    def agree(self, request,queryset):
        queryset.all().update(user_check=1)
        for o in queryset.all():
            url='http://127.0.0.1:8080/sendmail/api/?message=你的服务器：%s账号申请已通过\n账号会在1分钟内添加成功&con=%s&header=请查收'%(o.ip,o.email)
            s = requests.session()
            response = s.get(url=url)
    agree.short_description = '我同意'
    actions = ['delete_selected','agree']

admin.site.register(account, ArticleAdmin)


