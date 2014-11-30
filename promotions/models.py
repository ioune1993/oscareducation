from django.db import models
from django.contrib.auth.models import User


class Professor(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return ("%s %s" % (self.user.first_name, self.user.last_name)) if self.user.first_name or self.user.last_name else self.user.username


class Student(models.Model):
    user = models.OneToOneField(User)

    def get_email(self):
        if self.user.email.endswith("@example.com"):
            return ""
        return self.user.email

    def __unicode__(self):
        return ("%s %s" % (self.user.first_name, self.user.last_name)) if self.user.first_name or self.user.last_name else self.user.username


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(Student, null=True, blank=True)
    professors = models.ManyToManyField(Professor, null=True, blank=True)

    def __unicode__(self):
        return self.name
