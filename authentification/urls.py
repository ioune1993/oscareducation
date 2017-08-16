from django.conf.urls import url, include
from django.contrib.auth import urls
from . import views


urlpatterns = [
#    url(r'^login/$', views.login, name='login'),
    url(r'^usernamelogin/$', views.username, name='username_login'),
    url(r'^passwordlogin/$', views.password, name='password_login'),
    url(r'^codelogin/$', views.code, name='code_login'),
    url(r'^createpassword/$', views.create_password, name="create_password"),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^subscribe/$', views.subscribe_teacher, name='subscribe_teacher'),
    url('^', include(urls)),
]
