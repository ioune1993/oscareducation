from django.db import models

from promotions.models import Lesson
from skills.models import Skill


class Test(models.Model):
    name = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson)
    skills = models.ManyToManyField(Skill)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['created_at']


class Exercice(models.Model):
    content = models.TextField()
    answer = models.TextField()
    skill = models.ForeignKey(Skill)


class TestExercice(models.Model):
    test = models.ForeignKey(Test)
    # it can happen that we need to test something but that we don't have an
    # exercice ready for it
    exercice = models.ForeignKey(Exercice, null=True)
    # therefor we need to remember which skill we are testing
    skill = models.ForeignKey(Skill)
    created_at = models.DateTimeField(auto_now_add=True)


class TestStudent(models.Model):
    student = models.ForeignKey("promotions.Student")
    test = models.ForeignKey(Test)
    finished = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)


class Answer(models.Model):
    raw_answer = models.TextField()  # let's store json

    # we might no know the answer if we want the teacher to correct the test by
    # hand
    correct = models.NullBooleanField()

    test_student = models.ForeignKey(TestStudent)
    test_exercice = models.ForeignKey(TestExercice)

    answer_datetime = models.DateTimeField(auto_now_add=True)
