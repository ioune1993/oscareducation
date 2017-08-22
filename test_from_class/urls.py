from django.conf.urls import url

from promotions.utils import user_is_professor

import views

from .cbgv import TestFromClassDetailView


urlpatterns = [
    url(r'^lesson/(?P<pk>\d+)/test/from-class/add/$', views.lesson_test_from_class_add, name='lesson_test_from_class_add'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/from-class/(?P<pk>\d+)/fill/$', views.lesson_test_from_class_fill, name='lesson_test_from_class_fill'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/from-class/(?P<pk>\d+)/$', user_is_professor(TestFromClassDetailView.as_view()), name='lesson_test_from_class_detail'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/from-class/(?P<pk>\d+)/modify/$',
        user_is_professor(TestFromClassDetailView.as_view(template_name="professor/lesson/test/from-class/exercices.haml")),
        name='lesson_test_from_class_modify'),
    url(r'^add_test_from_class_for_lesson/$', views.lesson_test_from_class_add_json, name='lesson_test_from_class_add_json'),

]
