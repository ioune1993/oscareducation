import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oscar.settings")
django.setup()
import factory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from users.models import Professor
from users.models import Student


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', 'email', 'password')

    # Defaults (can be overridden)
    username = 'username'
    email = 'foo@bar.com'
    password = make_password('password')


class ProfessorFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Professor
        django_get_or_create = ('is_pending', 'code',)

    user = factory.SubFactory(UserFactory)
    is_pending = False
    code = 69


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student
        django_get_or_create = ('is_pending', 'code',)

    user = factory.SubFactory(UserFactory)
    is_pending = False
    code = 96
