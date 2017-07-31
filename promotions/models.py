# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Count


class Stage(models.Model):
    """[FR] Niveau/Degré/Année

        Each education form is subdivided in Stages,
        that cover a single year or several years.

    """
    name = models.CharField("Nom", max_length=255, unique=True)
    """The Stage name"""
    short_name = models.CharField("Nom", max_length=255, unique=True, null=True, blank=True)
    """The Stage name abbreviation"""
    level = models.PositiveSmallIntegerField("Niveau")
    """The level that permits to position Stages from different education forms"""
    previous_stage = models.ForeignKey("promotions.Stage", null=True, blank=True)
    """The Stage that precedes this Stage (in the same education form, if applicable)"""
    skills = models.ManyToManyField("skills.Skill")
    """The Skills that belong to this Stage"""

    def skills_with_exercice_count(self):
        print self, self.skills.count()
        return self.skills.annotate(Count('context'))

    def __unicode__(self):
        return self.name


    class Meta:
        unique_together = ('name', 'level')
        ordering = ['level']


class Lesson(models.Model):
    """[FR] Classe

        A group of Students created and managed
        by (a) Professor(s), with their own tests
        and optionally their own resources.

    """

    name = models.CharField("Nom", max_length=255)
    """The Lesson name"""
    students = models.ManyToManyField("users.Student")
    """The Students belonging to this Lesson"""
    professors = models.ManyToManyField("users.Professor")
    """The Professors managing this Lesson"""
    stage = models.ForeignKey(Stage, verbose_name=u"Année")
    """This Lesson Stage (its "level" in the education)"""

    def stages_in_unchronological_order(self):
        stage = self.stage

        stages = [stage]

        while stage.previous_stage is not None:
            stage = stage.previous_stage
            stages.append(stage)

        return stages