from django.conf.urls import url, include
from django.contrib.auth import urls
from . import views


urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url('^', include(urls)),
]
