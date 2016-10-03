from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView

from skills.models import Skill
from examinations.models import Exercice
from .models import Stage

from .utils import user_is_professor

from .cbgv import LessonStudentListView, StudentDelete, LessonDelete, BaseTestDelete, TestDetailView, TestFromClassDetailView


urlpatterns = patterns('promotions.views',
    url(r'^dashboard/$', 'dashboard', name='dashboard'),

    url(r'^lesson/add/$', 'lesson_add', name='lesson_add'),
    url(r'^lesson/(?P<pk>\d+)/$', 'lesson_detail', name='lesson_detail'),
    url(r'^lesson/(?P<pk>\d+)/update/$', 'lesson_update', name='lesson_update'),
    url(r'^lesson/(?P<pk>\d+)/delete/$', user_is_professor(LessonDelete.as_view()), name='lesson_delete'),

    url(r'^lesson/(?P<pk>\d+)/student/$', user_is_professor(LessonStudentListView.as_view()), name='lesson_student_list'),
    url(r'^lesson/(?P<pk>\d+)/student/add/$', 'lesson_student_add', name='lesson_student_add'),
    url(r'^lesson/(?P<lesson_pk>\d+)/student/(?P<pk>\d+)/$', 'lesson_student_detail', name='lesson_student_detail'),
    url(r'^lesson/(?P<lesson_pk>\d+)/student/(?P<pk>\d+)/update/$', 'lesson_student_update', name='lesson_student_update'),
    url(r'^lesson/(?P<lesson_pk>\d+)/student/(?P<pk>\d+)/delete/$', user_is_professor(StudentDelete.as_view()), name='lesson_student_delete'),
    url(r'^lesson/(?P<lesson_pk>\d+)/student/(?P<pk>\d+)/test/(?P<test_pk>\d+?)/$', 'lesson_student_test_detail', name='lesson_student_test'),

    url(r'^lesson/(?P<pk>\d+)/test/$', 'lesson_test_list', name='lesson_test_list'),
    url(r'^lesson/(?P<pk>\d+)/test/add/$', 'lesson_test_add', name='lesson_test_add'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/(?P<pk>\d+)/update/$', 'lesson_test_update', name='lesson_test_update'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/(?P<pk>\d+)/delete/$', user_is_professor(BaseTestDelete.as_view()), name='lesson_test_delete'),

    # TODO: professor can only see his tests
    url(r'^lesson/(?P<pk>\d+)/test/online/add/$', 'lesson_test_online_add', name='lesson_test_online_add'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/online/(?P<pk>\d+)/$', user_is_professor(TestDetailView.as_view()), name='lesson_test_online_detail'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/online/(?P<pk>\d+)/close/$', 'lesson_test_online_close_open', name='lesson_test_online_close_open'),
    url(r'^add_test_for_lesson/$', 'lesson_test_add_json', name='lesson_test_add'),

    url(r'^lesson/(?P<pk>\d+)/test/from-class/add/$', 'lesson_test_from_class_add', name='lesson_test_from_class_add'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/from-class/(?P<pk>\d+)/fill/$', 'lesson_test_from_class_fill', name='lesson_test_from_class_fill'),
    url(r'^lesson/(?P<lesson_pk>\d+)/test/from-class/(?P<pk>\d+)/$', user_is_professor(TestFromClassDetailView.as_view()), name='lesson_test_from_class_detail'),
    url(r'^add_test_from_class_for_lesson/$', 'lesson_test_from_class_add_json', name='lesson_test_from_class_add_json'),


    url(r'^lesson/(?P<lesson_pk>\d+)/skill/(?P<skill_code>.+)/$', 'lesson_skill_detail', name='lesson_skill_detail'),

    url(r'^regenerate_student_password/$', 'regenerate_student_password', name='regenerate_student_password'),

    url(r'^skill/$', 'contribute_page', name='skill_list'),
    url(r'^skill/(?P<slug>.+)/$', user_is_professor(DetailView.as_view(model=Skill, slug_field="code", template_name="professor/skill/detail.haml")), name='skill_detail'),
    url(r'^pedagogical/(?P<slug>.+)/$', 'update_pedagogical_ressources', name='skill_update_pedagogical_ressources'),
    url(r'^skill_tree/$', user_is_professor(ListView.as_view(model=Skill, template_name="professor/skill/tree.haml")), name='skill_tree'),

    url(r'^lesson/(?P<lesson_pk>\d+)/validate_skill/(?P<student_skill>\d+)/$', 'validate_student_skill', name='validate_student_skill'),
    url(r'^lesson/(?P<lesson_pk>\d+)/unvalidate_skill/(?P<student_skill>\d+)/$', 'unvalidate_student_skill', name='unvalidate_student_skill'),
    url(r'^lesson/(?P<lesson_pk>\d+)/default_skill/(?P<student_skill>\d+)/$', 'default_student_skill', name='default_student_skill'),

    url(r'^lesson_tests_and_skills/(?P<lesson_id>\d+).json$', 'lesson_tests_and_skills', name='lesson_tests_and_skills'),

    url(r'^exercices/$', 'exercice_list', name='exercice_list'),
    url(r'^exercices/(?P<pk>\d+)/$', user_is_professor(DetailView.as_view(model=Exercice, template_name="professor/exercice/detail.haml")), name='exercice_detail'),
    url(r'^exercices/validation_form/$', user_is_professor(ListView.as_view(model=Stage, template_name="professor/exercice/validation_form.haml")), name='exercice_validation_form'),
    url(r'^exercices/validation_form/validate/$', 'exercice_validation_form_validate_exercice', name='exercice_validation_form_validate_exercice'),
    url(r'^exercices/validation_form/pull-request/$', 'exercice_validation_form_pull_request', name='exercice_validation_form_pull_request'),

    url(r'^lesson/(?P<pk>\d+)/students_password_page/$', 'students_password_page', name='lesson_student_password_page'),
)
