from django.test import TestCase, Client
from django.contrib.auth.models import User
from users.models import Professor, Student
from django.core.urlresolvers import reverse

from hamcrest import *
import unittest

from django.test import Client



login = "prof"
pwd = "prof"





"""class PermissionsTest(TestCase):
    def setUp(self):
        prof = User.objects.create(username="professor")
        prof.set_password("1234")
        prof.save()
        self.prof = Professor.objects.create(user=prof)

        student = User.objects.create(username="student")
        student.set_password("1234")
        student.save()
        self.prof = Student.objects.create(user=student)

    def test_unlogged_go_to_homepage(self):
        c = Client()

        response = c.get("/")
        self.assertEqual(response.url, 'http://testserver/accounts/login/')
        self.assertEqual(response.status_code, 302)

    def test_redirect_professor(self):
        c = Client()
        c.login(username="professor", password="1234")

        response = c.get("/")
        self.assertEqual(response.url, 'http://testserver/professor/dashboard/')

    def test_redirect_student(self):
        c = Client()
        c.login(username="student", password="1234")

        response = c.get("/")
        self.assertEqual(response.url, 'http://testserver/student/dashboard/')


class PageLoadTest(TestCase):
    def setUp(self):
        prof = User.objects.create(username="professor")
        prof.set_password("1234")
        prof.save()
        self.prof = Professor.objects.create(user=prof)

        self.c = Client()
        self.c.login(username="professor", password="1234")

    def test_static_pages_load(self):
        self.assertEqual(self.c.get(reverse("professor:dashboard")).status_code, 200)"""


# exercice_validation_form_validate_exercice

class ExerciceFromExerciceTest(TestCase):
    # We set up the paramters of login
    def setUp(self):
        self.c = Client()
        self.c.login(username="prof", password="prof")

    # We test a text question
    """def testText(self):
        request = {"questions" : [
        {"type" = "text","instructions":"2+2 = ?","answers"="4"}
        ]}
        self.assertEqual(self.c.exercice_validation_form_validate_exercice(request).yaml.result,'success')

    def testMath(self):

    def testGraph(self):"""


# exercice_validation_form_submit

class ExerciceSubmitTest(TestCase):
    # We set up the paramters of login
    def setUp(self):
        self.c = Client()
        self.c.login(username="prof", password="prof")

    def testText(self):
        self.c = Client()
        self.c.login(username="prof", password="prof")

    #def testGraph():


class PromotionsTest(TestCase):

    """def testWithoutLog(self):
        c = Client()
        response = c.get("/test/21/start/")
            #self.assertEqual(response.status_code, 404)
        assert_that(response.status_code,404)"""

    def testWithoutLogging(self):
        d = Client()
        response = d.get("/professor/dashboard/")
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, '/accounts/login/?next=/professor/dashboard/')

    def testLogging(self):
        e = Client()
        e.login(usernmae=login,password=pwd)
        response = e.get("/professor/dashboard/")
        self.assertEqual(response.status_code,302)

    def test(self):
        c = Client()
        c.login(username=login, password=pwd)
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.haml')

        #print(response)
        #assert_that(response, assert_that(equal_to('examinations/test_closed.haml')))

    def testLesson(self):
        c = Client()
        c.login(username=login, password=pwd)
        response = c.get("/professor/lesson/134/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/professor/lesson/' + "134" + '/')
        #self.assertRedirects(response, 'examinations/test_finished.haml')
        #self.assertTemplateUsed(response,'professor/lesson/detail.haml')

