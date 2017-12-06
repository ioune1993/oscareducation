import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oscar.settings")
django.setup()
import factory
from skills.models import Skill, Section


class SkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Skill
        django_get_or_create = ('id', 'code', 'name', 'description', 'image', 'oscar_synthese', 'modified_by_id', 'section_id')


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Section
        django_get_or_create = ('id', 'name')
