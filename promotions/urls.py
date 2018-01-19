from django.conf.urls import url, include
from django.views.generic import DetailView, ListView

from skills.models import Skill
from examinations.models import Context

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

    # TODO : Delete lesson_student_list and its template
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
    url(r'^global_resources/(?P<pk>\d+)/delete/$', views.global_resources_delete, name='global_resources_delete'),
    url(r'^skill/(?P<slug>.+)/$', user_is_professor(DetailView.as_view(model=Skill, slug_field="code", template_name="professor/skill/detail.haml")), name='skill_detail'),
    url(r'^pedagogical/(?P<type>.+)/(?P<id_type>.+)/(?P<kind>.+)/resource/remove/(?P<id>\d+)/$', views.remove_pedagogical_ressources, name='remove_pedagogical_ressources'),
    url(r'^pedagogical/(?P<type>.+)/(?P<id>.+)/rate/$', views.create_rate,name='create_rate'),
    url(r'^pedagogical/(?P<type>.+)/(?P<id>.+)/makerating/$', views.get_rate_vote,name='get_rate_vote'),
    url(r'^pedagogical/(?P<type>.+)/(?P<id>.+)/average/$', views.get_average,name='get_average'),
    url(r'^pedagogical/(?P<type>.+)/(?P<id>.+)/$', views.update_pedagogical_ressources, name='update_pedagogical_ressources'),
    url(r'^skill_tree/$', user_is_professor(ListView.as_view(model=Skill, template_name="professor/skill/tree.haml")), name='skill_tree'),

    url(r'^lesson/(?P<lesson_pk>\d+)/validate_skill/(?P<student_skill>\d+)/$', views.validate_student_skill, name='validate_student_skill'),
    url(r'^lesson/(?P<lesson_pk>\d+)/unvalidate_skill/(?P<student_skill>\d+)/$', views.unvalidate_student_skill, name='unvalidate_student_skill'),
    url(r'^lesson/(?P<lesson_pk>\d+)/default_skill/(?P<student_skill>\d+)/$', views.default_student_skill, name='default_student_skill'),

    url(r'^lesson_tests_and_skills/(?P<lesson_id>\d+).json$', views.lesson_tests_and_skills, name='lesson_tests_and_skills'),

    # TODO "exercices" -> "question"
    url(r'^exercices/$', views.exercice_list, name='exercice_list'),
    url(r'^exercices/to_approve/$', views.exercice_to_approve_list, name='exercice_to_approve_list'),
    url(r'^exercices/(?P<pk>\d+)/$', user_is_professor(DetailView.as_view(model=Context, template_name="professor/exercice/detail.haml")), name='exercice_detail'),
    url(r'^exercices/(?P<pk>\d+)/test/$', views.exercice_test, name='exercice_test'),
    url(r'^exercices/(?P<pk>\d+)/update/$', views.exercice_update, name='exercice_update'),
    url(r'^exercices/(?P<pk>\d+)/update/json/$', views.exercice_update_json, name='exercice_update_json'),
    url(r'^exercices/(?P<pk>\d+)/update/submit/$', views.exercice_validation_form_submit, name='exercice_update_submit'),
    url(r'^exercices/\d+/update/validate/$', views.exercice_validation_form_validate_exercice, name='exercice_update_validate'),
    url(r'^exercices/validation_form/$', user_is_professor(ListView.as_view(model=Stage, template_name="professor/exercice/validation_form.haml")), name='exercice_validation_form'),
    url(r'^exercices/validation_form/validate/$', views.exercice_validation_form_validate_exercice, name='exercice_validation_form_validate_exercice'),
    url(r'^exercices/validation_form/submit/$', views.exercice_validation_form_submit, name='exercice_validation_form_pull_request'),
    url(r'^exercices/(?P<exercice_pk>\d+)/for_test_exercice/(?P<test_exercice_pk>\d+)/$', views.exercice_for_test_exercice, name='exercice_for_test_exercice'),
    url(r'^exercices/adapt_exercice/(?P<test_exercice_pk>\d+)/$', views.exercice_adapt_test_exercice, name='exercice_adapt_test_exercice'),
    url(r'^exercices/remove_exercice/(?P<test_exercice_pk>\d+)/$', views.exercice_remove_test_exercice, name='exercice_remove_test_exercice'),

    url(r'^lesson/(?P<pk>\d+)/students_password_page/$', views.students_password_page, name='lesson_student_password_page'),
    url(r'^lesson/(?P<lesson_pk>\d+)/students_password_page/(?P<student_pk>\d+)/$', views.single_student_password_page,
        name='single_student_password_page'),

    url(r'^education/$', views.main_education, name ='main-education'),
    url(r'^education/socles-competences/$', views.socles_competence, name='socles-competence'),
    url(r'^education/enseignement-professionnel/$', views.enseign_pro, name='enseign-pro'),
    url(r'^education/enseignement-tech-art/$', views.enseign_techart, name='enseign-techart'),
    url(r'^education/enseignement-transition/$', views.enseign_trans, name='enseign-trans'),

    url(r'^professor_correct/$', views.professor_correct, name='professor_correct'),
    url(r'^professor_iscorrect/$', views.professor_iscorrect, name='professor_iscorrect'),
    url(r'^professor_rename_test/$', views.professor_rename_test, name='professor_rename_test'),
    url(r'^professor_test_add_question/$', views.professor_test_add_question, name='professor_test_add_question'),
    url(r'^professor_test_delete_question/$', views.professor_test_delete_question, name='professor_test_delete_question'),
    url(r'^professor_test_add_skill/$', views.professor_test_add_skill, name='professor_test_add_skill'),
    url(r'^professor_test_delete_skill/$', views.professor_test_delete_skill, name='professor_test_delete_skill'),

	url(r'^train/', include('train.urls')),

]
