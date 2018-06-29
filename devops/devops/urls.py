
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^serveraccount/', include('apps.ServerAccount.urls')),
    url(r'^sendmail/', include('apps.sendmail.urls')),

]