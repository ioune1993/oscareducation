from django.db import models

from promotions.models import Lesson


class RevisionPlanning(models.Model):
    lesson = models.ForeignKey(Lesson)
