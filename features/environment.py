# coding=utf-8
import django
import time

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.test.runner import DiscoverRunner
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.shortcuts import resolve_url
import os
from pages import *
os.environ['DJANGO_SETTINGS_MODULE'] = 'oscar.settings'


def before_all(context):
    django.setup()
    context.test_runner = DiscoverRunner()
    context.old_db_config = context.test_runner.setup_databases()
    context.browser = Browser()

    # Page Objects
    context.login_page = LoginPage()
    context.professor_dashboard_page = ProfessorDashboardPage()
    context.student_dashboard_page = StudentDashboardPage()
    context.create_class_page = CreateClassPage()
    context.add_student_class_page = AddStudentClassPage()
    context.class_page = ClassPage()
    context.add_online_test_page = AddOnlineTestPage()
    context.test_modify_page = TestModifyPage()
    context.generator_page = GeneratorPage()
    context.generated_questions_page = GeneratedQuestionsPage()


class BehaviorDrivenTestCase(StaticLiveServerTestCase):
    """
    Test case attached to the context during behave execution
    This test case prevents the regular tests from running.
    """

    def runTest(*args, **kwargs):
        pass


def before_scenario(context, _):
    context.test = BehaviorDrivenTestCase()
    context.test.setUpClass()
    context.test()  # this starts a transaction
    context.base_url = context.test.live_server_url
    # Fill test database with test data
    populate_db()

    def get_url(to=None, *args, **kwargs):
        return context.base_url + (
            resolve_url(to, *args, **kwargs) if to else '')
    context.get_url = get_url


def after_scenario(context, _):
    pass


def after_all(context):
    # Explicitly quits the browser, otherwise it won't once tests are done
    context.browser.quit()
    context.test_runner.teardown_databases(context.old_db_config)


def before_feature(context, feature):
    # Code to be executed each time a feature is going to be tested
    pass


def before_step(context, step):
    pass


# After a single step
def after_step(context, step):
    if step.status == 'failed':
        context.browser.save_screen_shot(context, step)


def populate_db():
    from test.factories.stage import StageFactory
    from test.factories.skill import SkillFactory
    from test.factories.skill import SectionFactory
    from test.factories.lesson import LessonFactory
    from test.factories.test import TestFactory, QuestionFactory, ListQuestionsFactory, ContextFactory, TestExerciceFactory
    from test.factories.user import ProfessorFactory, StudentFactory
    from test.factories.studentskill import StudentSkillFactory

    SectionFactory.create(id=28, name="UAA5: Deuxième degré").save()

    skilla = SkillFactory.create(id=342, code="T4-U5-A1b",
                        name="Résoudre algébriquement une équation ou une inéquation du 2e degré", description="",
                        image="area-chart", oscar_synthese=None, modified_by_id=None, section_id=28)

    skilla.save()

    StageFactory.create(id=1, name="étape I (1er degré primaire)", short_name="1e", level=1,
                        previous_stage_id=None).save()
    StageFactory.create(id=9, name="étape II (2e et 3e degrés primaire)", short_name="2e", level=2,
                        previous_stage_id=1).save()
    StageFactory.create(id=3, name="étape III (1er degré secondaire)", short_name="3e", level=3,
                        previous_stage_id=9).save()
    StageFactory.create(id=10, name="2e degré professionnel", short_name="2p", level=4,
                        previous_stage_id=3).save()
    StageFactory.create(id=11, name="3e degré professionnel", short_name="3p", level=5,
                        previous_stage_id=10).save()
    StageFactory.create(id=18, name="2e degré technique (2 pér./sem.)", short_name="2d2", level=4,
                        previous_stage_id=3).save()
    StageFactory.create(id=19, name="3e degré technique (2 pér./sem.)", short_name="3d2", level=5,
                        previous_stage_id=18).save()
    StageFactory.create(id=12, name="3e année transition", short_name="3t", level=4,
                        previous_stage_id=3).save()
    mystage = StageFactory.create(id=13, name="4e année transition", short_name="4t", level=5,
                        previous_stage_id=12, skills=(skilla,))
    mystage.save()

    StageFactory.create(id=14, name="5e année transition (mathématiques de base)", short_name="5tb", level=6,
                        previous_stage_id=13).save()
    StageFactory.create(id=15, name="6e année transition (mathématiques de base)", short_name="6tb", level=7,
                        previous_stage_id=14).save()
    StageFactory.create(id=16, name="5e année transition (mathématiques générales)", short_name="5tg", level=6,
                        previous_stage_id=13).save()
    StageFactory.create(id=17, name="6e année transition (mathématiques générales)", short_name="6tg", level=7,
                        previous_stage_id=16).save()

    prof = ProfessorFactory.create(user__username="username", user__password=make_password("password"))
    prof.save()

    studenta = StudentFactory.create(user__username="studenta", user__password=make_password("studenta"))
    studentb = StudentFactory.create(user__username="studentb", user__password=make_password("studentb"))
    studenta.save()
    studentb.save()
    StudentSkillFactory(student=studenta, skill=skilla).save()
    StudentSkillFactory(student=studentb, skill=skilla).save()

    lesson = LessonFactory.create(id=9999, name="Classe fooo", stage_id=mystage.id, students=(studenta, studentb,), professors=(prof,))
    lesson.save()

    test = TestFactory.create(id=35, name="testifoo", lesson_id=lesson.id)
    test.fully_testable_online = True
    test.save()
    test.generate_skills_test()

    question = QuestionFactory.create(description='foooo', answer="kekk")
    question.save()

    context = ContextFactory.create(skill_id=skilla.id)
    context.save()

    testexe = TestExerciceFactory.create(test_id=test.id, exercice=context, skill_id=skilla.id)
    testexe.save()

    list_question = ListQuestionsFactory.create(context_id=testexe.exercice.id, question_id=question.id)
    list_question.save()

    with transaction.atomic():
        testexe.exercice = context
        if context.testable_online:
            testexe.testable_online = True
            testexe.test.fully_testable_online = True
        testexe.save()