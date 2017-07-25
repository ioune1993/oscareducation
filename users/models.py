# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import random
from django.db.models import Count
from django.contrib.auth.models import User


class AuthUserManager(models.Manager):
    def get_queryset(self):
        return super(AuthUserManager, self).get_queryset().select_related('user')


class Professor(models.Model):

    objects = AuthUserManager()
    user = models.OneToOneField(User)
    is_pending = models.BooleanField(default=True)
    code = models.IntegerField(null=True,blank=True)

    def __unicode__(self):
        return ("%s %s" % (
        self.user.first_name, self.user.last_name)) if self.user.first_name or self.user.last_name else self.user.username

    class Meta:
        ordering = ['user__last_name', 'user__first_name']


class Student(models.Model):

    objects = AuthUserManager()

    user = models.OneToOneField(User)
    is_pending = models.BooleanField(default=True)
    code = models.IntegerField(null=True,blank=True)
    code_created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return ("%s %s" % (
        self.user.first_name, self.user.last_name)) if self.user.first_name or self.user.last_name else self.user.username

    class Meta:
        ordering = ['user__last_name']
