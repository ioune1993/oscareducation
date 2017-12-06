import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oscar.settings")
django.setup()
import factory
from skills.models import StudentSkill


class StudentSkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StudentSkill
        django_get_or_create = ('student', 'skill')
