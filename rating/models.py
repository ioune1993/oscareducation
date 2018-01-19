from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Star_rating(models.Model):
    resource = models.ForeignKey('resources.Resource')
    """The resource linked to this star rating"""

    star = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(5.0)])
    """Number of stars given"""

    rated_by = models.ForeignKey(User)
    """The user that starred the resource"""

    rated_on = models.DateTimeField()
    """The date when the star rating was given"""

    comment = models.CharField(max_length=300,null=True,blank=True)
    """Comment associated with star rating"""

    class Meta:
        unique_together = ('resource','rated_by')


class Rating(models.Model):
    resource = models.ForeignKey('resources.Resource')
    """The Resources linked to this rating. A Resource can be linked to several ratings"""

    question = models.ForeignKey('Question')
    """The Question answered for this rating"""

    value = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(5.0)])
    """The value given to this rating"""

    rated_by = models.ForeignKey(User)
    """The User who rated"""

    rated_on = models.DateTimeField()
    """Date of rating"""


    def number_votes_question(self,resource,question):
        """

        :param resource: teh resource we want the votes from
        :param question: the question we want the votes from
        :return: return the number of people who voted for the question on th reosource
        """
        r = Rating.objects.filter(resource=resource,question=question)
        return r.entry_set.count()

    class Meta:
        unique_together = ('resource','question','rated_by')


class Question(models.Model):
    question_statement = models.TextField()
    """The Question statement"""

    type = models.IntegerField()
    """The type of question (user for prof vs student)"""

    label = models.TextField()
    """The label assigned to a question """