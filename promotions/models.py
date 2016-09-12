# encoding: utf-8

import random
from django.db import models
from django.contrib.auth.models import User


class AuthUserManager(models.Manager):
    def get_queryset(self):
        return super(AuthUserManager, self).get_queryset().select_related('user')


class Professor(models.Model):
    objects = AuthUserManager()

    user = models.OneToOneField(User)

    def __unicode__(self):
        return ("%s %s" % (self.user.first_name, self.user.last_name)) if self.user.first_name or self.user.last_name else self.user.username


class Student(models.Model):
    objects = AuthUserManager()

    user = models.OneToOneField(User)

    def get_email(self):
        if self.user.email.endswith("@example.com"):
            return ""
        return self.user.email

    def __unicode__(self):
        return ("%s %s" % (self.user.first_name, self.user.last_name)) if self.user.first_name or self.user.last_name else self.user.username

    def generate_new_password(self):
        new_password = "%s%s%s" % (self.user.first_name[0].lower(), self.user.last_name[0].lower(), random.randint(100, 999))
        self.user.set_password(new_password)
        self.user.save()
        return new_password

    def done_tests(self):
        return self.teststudent_set.filter(finished_at__isnull=False)

    def todo_tests(self):
        return self.teststudent_set.filter(finished_at__isnull=True)

    def get_last_test(self):
        return self.teststudent_set.order_by('-test__created_at').first()

    def has_recommanded_skills(self):
        for student_skill in self.studentskill_set.all():
            if student_skill.recommanded_to_learn():
                return True

        return False

    class Meta:
        ordering = ['user__last_name']


class Stage(models.Model):
    name = models.CharField("Nom", max_length=255, unique=True)
    level = models.PositiveSmallIntegerField("Niveau")
    previous_stage = models.ForeignKey("promotions.Stage", null=True, blank=True)

    skills = models.ManyToManyField("skills.Skill")

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'level')
        ordering = ['level']


class Lesson(models.Model):
    name = models.CharField("Nom", max_length=255)
    students = models.ManyToManyField(Student)
    professors = models.ManyToManyField(Professor)

    stage = models.ForeignKey(Stage, verbose_name=u"Année")

    def stages_in_unchronological_order(self):
        stage = self.stage

        stages = [stage]

        while stage.previous_stage is not None:
            stage = stage.previous_stage
            stages.append(stage)

        return stages

    def __unicode__(self):
        return self.name
