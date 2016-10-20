from django.test import TestCase, Client
from django.contrib.auth.models import User
from promotions.models import Professor, Student


class PermissionsTest(TestCase):
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
