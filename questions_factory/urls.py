from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^generator/(?P<lesson_id>\d+)/(?P<skill_id>\d+)/(?P<test_id>\d+)/submit/$', views.generator_submit,
        name='generator_submit'),
    url(r'^generator/(?P<lesson_id>\d+)/(?P<skill_id>\d+)/(?P<test_id>\d+)/form/(?P<generator_name>\w+)/$',
        views.generator_choice, name='generator_choice'),
    url(r'^generator/(?P<lesson_id>\d+)/(?P<skill_id>\d+)/(?P<test_id>\d+)/$', views.generator, name='generator')
]
