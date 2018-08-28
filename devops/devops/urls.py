
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^serveraccount/', include('apps.ServerAccount.urls')),
    url(r'^ansibleControl/', include('apps.ansibleControl.urls')),
    url(r'^nagiosControl/', include('apps.nagiosControl.urls')),
]
