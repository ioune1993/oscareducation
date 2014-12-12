from django.conf.urls import patterns, url
from django.views.generic import DetailView

from skills.models import Skill


urlpatterns = patterns('promotions.views',
    url(r'^dashboard/$', 'dashboard', name='professor_dashboard'),
    url(r'^lesson/(?P<pk>\d+)/$', 'lesson_detail_view', name='professor_lesson_detail_view'),
    url(r'^student/(?P<pk>\d+)/$', 'student_detail_view', name='professor_student_detail_view'),
    url(r'^skill/(?P<slug>\w+)/$', DetailView.as_view(model=Skill, slug_field="code", template_name="professor/skill_detail.haml"), name='professor_skill_detail_view'),
)
