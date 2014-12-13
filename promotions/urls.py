from django.conf.urls import patterns, url
from django.views.generic import DetailView

from skills.models import Skill


urlpatterns = patterns('promotions.views',
    url(r'^dashboard/$', 'dashboard', name='professor_dashboard'),
    url(r'^lesson/(?P<pk>\d+)/$', 'lesson_detail_view', name='professor_lesson_detail_view'),
    url(r'^student/(?P<pk>\d+)/$', 'student_detail_view', name='professor_student_detail_view'),
    url(r'^skill/(?P<slug>\w+)/$', DetailView.as_view(model=Skill, slug_field="code", template_name="professor/skill_detail.haml"), name='professor_skill_detail_view'),
    url(r'^regenerate_student_password/$', 'regenerate_student_password', name='professor_regenerate_student_password'),

    url(r'^validate_skill/(?P<student_skill>\d+)/$', 'validate_student_skill', name='professor_validate_student_skill'),
    url(r'^unvalidate_skill/(?P<student_skill>\d+)/$', 'unvalidate_student_skill', name='professor_unvalidate_student_skill'),
)
