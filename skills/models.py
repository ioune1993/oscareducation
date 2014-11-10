from django.db import models

from promotions.models import Student


class Skill(models.Model):
    name = models.CharField(max_length=255)
    depend = models.ManyToManyField('Skill')
    year = models.CharField(max_length=255)


class StudentSkill(models.Model):
    student = models.ForeignKey(Student)
    skill = models.ForeignKey(Skill)
    tested = models.DateTimeField(default=None)
    acquired = models.DateTimeField(default=None)
    # bad: doesn't support regression
