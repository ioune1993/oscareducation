import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oscar.settings")
django.setup()
import factory
from examinations.models import Test, Context, List_question, Question, TestExercice


class TestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Test
        django_get_or_create = ('id', 'name', 'lesson_id')


class ContextFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Context
        django_get_or_create = ('skill_id',)


class ListQuestionsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = List_question
        django_get_or_create = ('context_id', 'question_id')


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question
        django_get_or_create = ('description', 'answer')


class TestExerciceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TestExercice
        django_get_or_create = ('test_id', 'exercice', 'skill_id')

