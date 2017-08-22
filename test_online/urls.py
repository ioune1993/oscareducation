from django.conf.urls import url

from promotions.utils import user_is_professor

import views

from .cbgv import TestDetailView


urlpatterns = [
    url(r'^lesson/(?P<pk>\d+)/test/online/add/$', views.lesson_test_online_add, name='lesson_test_online_add'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/online/(?P<pk>\d+)/$', user_is_professor(TestDetailView.as_view()), name='lesson_test_online_detail'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/online/(?P<pk>\d+)/modify/$', user_is_professor(TestDetailView.as_view(template_name="professor/lesson/test/online/exercices.haml")), name='lesson_test_online_exercices'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/online/(?P<test_pk>\d+)/change/(?P<test_exercice_pk>\d+)/$', user_is_professor(views.lesson_test_online_change_exercice), name='lesson_test_online_change_exercice'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/online/(?P<pk>\d+)/print/$', user_is_professor(TestDetailView.as_view(template_name="professor/lesson/test/online/print.haml")), name='lesson_test_online_print'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/online/(?P<pk>\d+)/insert_results/$', views.lesson_test_online_insert_results, name='lesson_test_online_insert_results'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/online/(?P<pk>\d+)/close/$', views.lesson_test_online_close_open, name='lesson_test_online_close_open'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/online/(?P<pk>\d+)/enable/$', views.lesson_test_online_enable, name='lesson_test_online_enable'),
    url(r'^add_test_for_lesson/$', views.lesson_test_add_json, name='lesson_test_add'),
]
