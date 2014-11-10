from django.db import models
from django.contrib.auth.models import User


class Professor(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return ("%s %s" % (self.user.first_name, self.user.last_name)) if self.user.first_name or self.user.last_name else self.user.username


class Student(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return ("%s %s" % (self.first_name, self.last_name)) if self.first_name or self.last_name else self.username

class Lesson(models.Model):
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(Student, null=True, blank=True)
    professors = models.ManyToManyField(Professor, null=True, blank=True)

    def __unicode__(self):
        return self.name
