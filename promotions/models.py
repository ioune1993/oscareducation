from django.db import models
from django.contrib.auth.models import User


class Professor(models.Model):
    user = models.OneToOneField(User)


class Student(models.Model):
    user = models.OneToOneField(User)


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(Student)
    professors = models.ManyToManyField(Professor)
