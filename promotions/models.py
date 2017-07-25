# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#stage
class Stage(models.Model):
    name = models.CharField("Nom", max_length=255, unique=True)
    short_name = models.CharField("Nom", max_length=255, unique=True, null=True, blank=True)
    level = models.PositiveSmallIntegerField("Niveau")
    previous_stage = models.ForeignKey("promotions.Stage", null=True, blank=True)

    skills = models.ManyToManyField("skills.Skill")
#lesson
class Lesson(models.Model):

    name = models.CharField("Nom", max_length=255)
    students = models.ManyToManyField("users.Student")
    professors = models.ManyToManyField("users.Professor")
    stage = models.ForeignKey(Stage, verbose_name=u"Année")
