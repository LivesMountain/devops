from django.conf.urls import url
from .views import apis
urlpatterns=[
    url(r'^api',apis),
]