from django.conf.urls import url, include
from django.views.generic import DetailView, ListView

from skills.models import Skill
from examinations.models import Exercice

import views

from .models import Stage

from .utils import user_is_professor

from .cbgv import LessonStudentListView, StudentDelete, LessonDelete, BaseTestDelete


urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name='dashboard'),

    url(r'^lesson/add/$', views.lesson_add, name='lesson_add'),
    url(r'^lesson/(?P<pk>\d+)/$', views.lesson_detail, name='lesson_detail'),
    url(r'^lesson/(?P<pk>\d+)/update/$', views.lesson_update, name='lesson_update'),
    url(r'^lesson/(?P<pk>\d+)/delete/$', user_is_professor(LessonDelete.as_view()), name='lesson_delete'),

    url(r'^lesson/(?P<pk>\d+)/student/$', user_is_professor(LessonStudentListView.as_view()), name='lesson_student_list'),
    url(r'^lesson/(?P<pk>\d+)/student/add/$', views.lesson_student_add, name='lesson_student_add'),
    url(r'^lesson/(?P<lesson_pk>\d+)/student/(?P<pk>\d+)/$', views.lesson_student_detail, name='lesson_student_detail'),
    url(r'^lesson/(?P<lesson_pk>\d+)/student/(?P<pk>\d+)/update/$', views.lesson_student_update, name='lesson_student_update'),
    url(r'^lesson/(?P<lesson_pk>\d+)/student/(?P<pk>\d+)/delete/$', user_is_professor(StudentDelete.as_view()), name='lesson_student_delete'),
    url(r'^lesson/(?P<lesson_pk>\d+)/student/(?P<pk>\d+)/test/(?P<test_pk>\d+?)/$', views.lesson_student_test_detail, name='lesson_student_test'),

    url(r'^lesson/(?P<pk>\d+)/test/$', views.lesson_test_list, name='lesson_test_list'),
    url(r'^lesson/(?P<pk>\d+)/test/add/$', views.lesson_test_add, name='lesson_test_add'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/(?P<pk>\d+)/update/$', views.lesson_test_update, name='lesson_test_update'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/(?P<pk>\d+)/delete/$', user_is_professor(BaseTestDelete.as_view()), name='lesson_test_delete'),

    # TODO: professor can only see his tests
    url(r'^', include('test_online.urls')),
    url(r'^', include('test_from_class.urls')),

    url(r'^lesson/(?P<lesson_pk>\d+)/skill/(?P<skill_code>.+)/$', views.lesson_skill_detail, name='lesson_skill_detail'),

    url(r'^regenerate_student_password/$', views.regenerate_student_password, name='regenerate_student_password'),

    url(r'^skill/$', views.contribute_page, name='skill_list'),
    url(r'^global_resources/(?P<pk>\d+)/delete/$', views.global_resources_delete, name='global_resources_delete'),
    url(r'^skill/(?P<slug>.+)/$', user_is_professor(DetailView.as_view(model=Skill, slug_field="code", template_name="professor/skill/detail.haml")), name='skill_detail'),
    url(r'^pedagogical/resource/remove/(?P<kind>\w+)/(?P<id>\d+)/$', views.remove_pedagogical_ressources, name='skill_remove_pedagogical_ressources'),
    url(r'^pedagogical/(?P<slug>.+)/$', views.update_pedagogical_ressources, name='skill_update_pedagogical_ressources'),
    url(r'^skill_tree/$', user_is_professor(ListView.as_view(model=Skill, template_name="professor/skill/tree.haml")), name='skill_tree'),

    url(r'^lesson/(?P<lesson_pk>\d+)/validate_skill/(?P<student_skill>\d+)/$', views.validate_student_skill, name='validate_student_skill'),
    url(r'^lesson/(?P<lesson_pk>\d+)/unvalidate_skill/(?P<student_skill>\d+)/$', views.unvalidate_student_skill, name='unvalidate_student_skill'),
    url(r'^lesson/(?P<lesson_pk>\d+)/default_skill/(?P<student_skill>\d+)/$', views.default_student_skill, name='default_student_skill'),

    url(r'^lesson_tests_and_skills/(?P<lesson_id>\d+).json$', views.lesson_tests_and_skills, name='lesson_tests_and_skills'),

    url(r'^exercices/$', views.exercice_list, name='exercice_list'),
    url(r'^exercices/to_approve/$', views.exercice_to_approve_list, name='exercice_list'),
    url(r'^exercices/(?P<pk>\d+)/$', user_is_professor(DetailView.as_view(model=Exercice, template_name="professor/exercice/detail.haml")), name='exercice_detail'),
    url(r'^exercices/validation_form/$', user_is_professor(ListView.as_view(model=Stage, template_name="professor/exercice/validation_form.haml")), name='exercice_validation_form'),
    url(r'^exercices/validation_form/validate/$', views.exercice_validation_form_validate_exercice, name='exercice_validation_form_validate_exercice'),
    url(r'^exercices/validation_form/pull-request/$', views.exercice_validation_form_pull_request, name='exercice_validation_form_pull_request'),

    url(r'^lesson/(?P<pk>\d+)/students_password_page/$', views.students_password_page, name='lesson_student_password_page'),
]
