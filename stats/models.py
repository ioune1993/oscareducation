# encoding: utf-8

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class LoginStats(models.Model):
    user = models.ForeignKey(User)
    user_kind = models.CharField(max_length=255, choices=(('student', 'étudiant·e'), ('professor', 'Professeur'), ('admin', 'Admin')))
    when = models.DateTimeField(auto_now_add=True)
