from django.conf.urls import url

from promotions.utils import user_is_professor

import views

from .cbgv import TestDetailView


urlpatterns = [
    url(r'^lesson/(?P<pk>\d+)/test/online/add/$', views.lesson_test_online_add, name='lesson_test_online_add'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/online/(?P<pk>\d+)/$', user_is_professor(TestDetailView.as_view()), name='lesson_test_online_detail'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/online/(?P<pk>\d+)/close/$', views.lesson_test_online_close_open, name='lesson_test_online_close_open'),
    url(r'^add_test_for_lesson/$', views.lesson_test_add_json, name='lesson_test_add'),
]
