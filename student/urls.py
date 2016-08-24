from django.conf.urls import patterns, url
from django.views.generic import DetailView, TemplateView

from skills.models import Skill

from utils import user_is_student


urlpatterns = patterns('student.views',
    url(r'^dashboard/$', 'dashboard', name='student_dashboard'),
    url(r'^test/finished/$', TemplateView.as_view(template_name="student/test/list_finished.haml"), name='student_test_finished'),
    url(r'^test/(?P<pk>\d+)/$', 'pass_test', name='student_pass_test'),
    url(r'^test/(?P<pk>\d+)/start/$', 'start_test', name='student_start_test'),
    url(r'^skill/(?P<slug>[a-zA-Z0-9_-]+)/$', user_is_student(DetailView.as_view(model=Skill, slug_field="code", template_name="skills/skills_detail.haml")), name='student_skill_pedagogic_ressources'),
)
