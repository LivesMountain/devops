from django.conf.urls import url,include
from django.contrib import admin
from user.views import *
urlpatterns = [
    url(r'^login/$', login),
    url(r'^register/$',regist),
    url(r'^logout/$', logout),
]
