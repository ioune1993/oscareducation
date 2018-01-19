# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import models
import random
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from interface import Status
from django.db.models import Count
from django.db.models import Max


class AuthUserManager(models.Manager):
    def get_queryset(self):
        return super(AuthUserManager, self).get_queryset().select_related('user')


class Professor(models.Model):

    objects = AuthUserManager()
    user = models.OneToOneField(User)
    is_pending = models.BooleanField(default=True)
    code = models.BigIntegerField(null=True,blank=True)
    nbr_4_star_res = models.IntegerField(null=True)
    status = JSONField(null=True,blank=True)
    status_changed = models.IntegerField(default=0)

    def print_something(self):
        print(self.nbr_4_star_res)

    def __unicode__(self):
        return ("%s %s" % (
        self.user.first_name, self.user.last_name)) if self.user.first_name or self.user.last_name else self.user.username

    def update_status(self):

        res = resources.models.Resource.objects.filter(added_by=self.user)
        nb_4 = 0
        for r in res:
            avg = r.weighted_average()
            print(avg)
            if avg >= 4:
                nb_4 += 1
        if nb_4 > self.nbr_4_star_res:
            self.nbr_4_star_res = nb_4
            self.save()

        if self.status is not None:
            obj_status = json.loads(self.status)
        else:
            obj_status = None
        is_top = False
        top = None
        if Top_contributor.objects.count() != 0:
            top = Top_contributor.objects.get(pk=1)

        if (top is None):
            if self.nbr_4_star_res > 19:
                top = Top_contributor.objects.create(professor=self)
                self.status = json.dumps(Status("Top Contributor", "/static/img/status5.png").__dict__)
                self.status_changed = 1
                is_top = True
                self.save()
        else:
            top_prof = top.professor

            if top_prof.nbr_4_star_res < self.nbr_4_star_res:
                prof = Professor.objects.get(id=top.professor_id)
                prof.status_changed = -1
                prof.status = json.dumps(Status("Super Contributor", "/static/img/status4.png").__dict__)
                prof.save()

                self.status = json.dumps(Status("Top Contributor", "/static/img/status5.png").__dict__)
                top.professor = self
                top.save()
                is_top = True
                self.save()
            if self == top.professor:
                is_top = True

        if not is_top:
            if self.nbr_4_star_res >= 1 and self.nbr_4_star_res < 4:
                if obj_status is None or obj_status['name'] != 'Contributor':
                    self.status = json.dumps(Status("Contributor", "/static/img/status1.png").__dict__)
                    self.status_changed = 1
            elif self.nbr_4_star_res >= 4 and self.nbr_4_star_res < 9:
                if obj_status is None or obj_status['name'] != 'Motivated Contributor':
                    self.status = json.dumps(Status("Motivated Contributor", "/static/img/status2.png").__dict__)
                    self.status_changed = 1
            elif self.nbr_4_star_res >= 9 and self.nbr_4_star_res < 19:
                if obj_status is None or obj_status['name'] != 'Advanced Contributor':
                    self.status = json.dumps(Status("Advanced Contributor", "/static/img/status3.png").__dict__)
                    self.status_changed = 1
            elif self.nbr_4_star_res >= 19:
                if obj_status is None or obj_status['name'] != 'Super Contributor':
                    self.status = json.dumps(Status("Super Contributor", "/static/img/status4.png").__dict__)
                    self.status_changed = 1
            self.save()

    class Meta:
        ordering = ['user__last_name', 'user__first_name']



class Student(models.Model):

    objects = AuthUserManager()

    user = models.OneToOneField(User)
    is_pending = models.BooleanField(default=True)
    code = models.IntegerField(null=True, blank=True)
    code_created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return ("%s %s" % (
        self.user.first_name, self.user.last_name)) if self.user.first_name or self.user.last_name else self.user.username


    def generate_new_code(self):
        """Generate studenty password"""
        new_code = "%s" % (random.randint(1000, 9999))
        self.code = new_code
        self.is_pending = True
        self.save()
        return new_code

    class Meta:
        ordering = ['user__last_name']

    def get_email(self):
        if self.user.email.endswith("@example.com"):
            return ""
        return self.user.email

    def done_tests(self):
        return self.teststudent_set.filter(finished_at__isnull=False)

    def todo_tests(self):
        return self.teststudent_set.filter(finished_at__isnull=True)

    def get_last_test(self):
        return self.teststudent_set.order_by('-test__created_at').first()

    def has_recommended_skills(self):
        for student_skill in self.studentskill_set.all():
            if student_skill.recommended_to_learn():
                return True

        return False

class Top_contributor(models.Model):

    #status = models.ForeignKey(Professor_status,null=True)
    professor = models.ForeignKey(Professor,null=True)


"""class Professor_status(models.Model):

    name = models.CharField(max_length=100,unique=True)
    icon = models.CharField(max_length=300)
    min_contrib = models.PositiveIntegerField(null=True)

    class Meta:
        ordering = ['min_contrib',"name"]"""


import resources.models