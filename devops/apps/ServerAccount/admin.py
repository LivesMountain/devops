
from django.contrib import admin
from .models import *
from .sendmail import sendmail


class accountAdmin(admin.ModelAdmin):
    list_display = ('name','email','ip','user_check')
    list_display_links = ('name',)
    list_filter = ('user_check',)
    # list_editable = ('check',)
    # print(account.objects.all())
    def delete_selected(self, request, queryset):
        queryset.all().update(user_check=1)
        for o in queryset.all():
            o.delete()
            sm = sendmail('您的服务器：%s\n账号已被管理员删除' % (o.ip), o.email, '服务器账号被删除')
            sm.send()
    delete_selected.short_description = '删除用户账号'
    actions = ['delete_selected']


class accountApplyadmin(admin.ModelAdmin):
    list_display = ('name','email','ip','user_check')
    list_display_links = ('name',)
    list_filter = ('user_check',)
    # list_editable = ('check',)
    # print(account.objects.all())
    def delete_selected(self, request, queryset):
        for o in queryset.all():
            o.delete()
            sm = sendmail('您的服务器：%s\n账号申请已被管理员被拒绝' % (o.ip), o.email, '服务器账号申请被拒绝')
            sm.send()
    delete_selected.short_description = '我拒绝'

    def agree(self, request,queryset):
        queryset.all().update(user_check=1)
        for o in queryset.all():
            account.objects.filter(email="%s"%o.email).filter(ip="%s"%o.ip).update(user_check=1)
            sm = sendmail('你的服务器：%s账号申请已通过\n账号会在1分钟内添加成功，若1分钟后登录不了，请联系管理员' % (o.ip), o.email, '服务器账号申请已通过')
            sm.send()
    agree.short_description = '我同意'
    actions = ['delete_selected','agree']

admin.site.register(account_apply,accountApplyadmin)
admin.site.register(account, accountAdmin)





