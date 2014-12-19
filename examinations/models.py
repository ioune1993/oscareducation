from django.db import models

from promotions.models import Lesson
from skills.models import Skill


class Test(models.Model):
    name = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson)
    skills = models.ManyToManyField(Skill)
    created_at = models.DateTimeField(auto_now_add=True)


class Exercice(models.Model):
    content = models.TextField()
    answer = models.TextField()
    skill = models.ForeignKey(Skill)
