from django.db import models

from promotions.models import Student


class Skill(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    level = models.PositiveIntegerField()
    stage = models.CharField(max_length=255)
    section = models.CharField(max_length=255)

    depend = models.ManyToManyField('Skill')


class StudentSkill(models.Model):
    student = models.ForeignKey(Student)
    skill = models.ForeignKey(Skill)
    tested = models.DateTimeField(default=None)
    acquired = models.DateTimeField(default=None)
    # bad: doesn't support regression
