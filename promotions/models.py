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

    def skills_map(self):
        return self.studentskill_set.all().select_related("skill").order_by('-skill__level', '-skill__code')

    def __unicode__(self):
        return ("%s %s" % (self.user.first_name, self.user.last_name)) if self.user.first_name or self.user.last_name else self.user.username

    def generate_new_password(self):
        new_password = "%s%s%s" % (self.user.first_name[0].lower(), self.user.last_name[0].lower(), random.randint(100, 999))
        self.user.set_password(new_password)
        self.user.save()
        return new_password

    class Meta:
        ordering = ['user__last_name']


class Lesson(models.Model):
    name = models.CharField("Nom", max_length=255)
    students = models.ManyToManyField(Student, null=True, blank=True)
    professors = models.ManyToManyField(Professor, null=True, blank=True)

    def __unicode__(self):
        return self.name
