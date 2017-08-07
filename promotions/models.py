# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Count

# Create your models here.

#stage
class Stage(models.Model):
    name = models.CharField("Nom", max_length=255, unique=True)
    short_name = models.CharField("Nom", max_length=255, unique=True, null=True, blank=True)
    level = models.PositiveSmallIntegerField("Niveau")
    previous_stage = models.ForeignKey("promotions.Stage", null=True, blank=True)
    skills = models.ManyToManyField("skills.Skill")

    def skills_with_exercice_count(self):
        """ count Context in relation with the current Skills """
        #print self, self.skills.count()
        return self.skills.annotate(Count('context'))




    def __unicode__(self):
        return self.name


    class Meta:
        unique_together = ('name', 'level')
        ordering = ['level']



#lesson
class Lesson(models.Model):

    name = models.CharField("Nom", max_length=255)
    students = models.ManyToManyField("users.Student")
    professors = models.ManyToManyField("users.Professor")
    stage = models.ForeignKey(Stage, verbose_name=u"Année")

    def stages_in_unchronological_order(self):
        stage = self.stage

        stages = [stage]

        while stage.previous_stage is not None:
            stage = stage.previous_stage
            stages.append(stage)

        return stages