from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from utils import user_is_student

from . import views

urlpatterns = patterns('student.views',
    url(r'^dashboard/$', 'dashboard', name='student_dashboard'),
    url(r'^test/finished/$', TemplateView.as_view(template_name="student/test/list_finished.haml"), name='student_test_finished'),
    url(r'^test/(?P<pk>\d+)/$', 'pass_test', name='student_pass_test'),
    url(r'^test/(?P<pk>\d+)/start/$', 'start_test', name='student_start_test'),
    url(r'^skill/(?P<slug>[a-zA-Z0-9_-]+)/$', user_is_student(views.skill_pedagogic_ressources), name='student_skill_pedagogic_ressources'),

    # url(r'^test_poll/$', 'test_poll'),
)
